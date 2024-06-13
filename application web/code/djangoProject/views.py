from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from ultralytics import YOLO
import cv2
import pyttsx3
import speech_recognition as sr
import argparse
import os
import numpy as np
from keras.models import load_model
from matplotlib import pyplot as plt
import subprocess
from google.cloud import vision
from gtts import gTTS
import pygame
import tempfile
from google.cloud import translate_v2 as translate
import time




def LandingPage_view(request):
    return render(request, 'LandingPage.html')

def home_view(request):
    return render(request, 'home.html')
def thanks_view(request):
    return render(request, 'thanks.html')
def map_view(request):
    return render(request, 'map.html')
def bye_view(request):
    return render(request, 'bye.html')


def indoor(request):
    # Initialize the YOLO model
    model = YOLO(r"C:\Users\routa\OneDrive\Bureau\djangoProject\djangoProject\djangoProject\models\best.pt")

    # Try opening the webcam
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise IOError("Erreur: Impossible d'ouvrir la webcam.")
    except IOError as e:
        print(e)
        exit(1)

    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Configure speech rate
    engine.setProperty('rate', 150)  # Speech rate, adjust as necessary

    # Find and set a French voice
    voices = engine.getProperty('voices')
    french_voice = next((voice for voice in voices if 'french' in voice.languages), None)
    if french_voice:
        engine.setProperty('voice', french_voice.id)
    else:
        print("French voice not found, using default.")

    # Define class mapping
    class_mapping = {
        # Your class mapping here
        0: 'Apple-Pencil',
        1: 'Sac',
        2: 'Calculatrice',
        3: 'Cable de charge',
        4: 'Écouteurs',
        5: 'Lunettes',
        6: 'Clavier',
        7: 'Clés',
        8: 'Ordinateur portable',
        9: 'Notes de cours',
        10: 'Marqueurs',
        11: 'Téléphone portable',
        12: 'Souris',
        13: 'PC',
        14: 'Stylo',
        15: 'Écran',
        16: 'Carte',
        17: 'Portefeuille',
        18: 'Montre',
        19: 'Bouteille d\'eau',
        20: 'iPad-Air',
        21: 'iPad-Pro',
        22: 'Sac',
        23: 'Toilette',
        24: 'Lit',
        25: 'Livre',
        26: 'Porte de placard',
        27: 'Poignée',
        28: 'Chat',
        29: 'T-shirt',
        30: 'Robe',
        31: 'Veste',
        32: 'Pantalon',
        33: 'Chemise',
        34: 'Short',
        35: 'Jupe',
        36: 'Pull',
        37: 'Chien',
        38: 'Chiens',
        39: 'Porte',
        40: 'En colère',
        41: 'Heureux',
        42: 'Normal',
        43: 'Triste',
        44: 'Couscous',
        45: 'Pastilla',
        46: 'Rfissa',
        47: 'Tanjia',
        48: 'Pomme',
        49: 'Kiwi',
        50: 'Mangue',
        51: 'Orange',
        52: 'Pastèque',
        53: 'Cerise',
        54: 'Clé',
        55: 'Bouteille',
        56: 'Bol',
        57: 'Tasse',
        58: 'Planche à découper',
        59: 'Fourchette',
        60: 'Bouteille pleine',
        61: 'Bol plein',
        62: 'Tasse pleine',
        63: 'Casserole pleine',
        64: 'Pot plein',
        65: 'Couteau',
        66: 'Poêle',
        67: 'Assiette',
        68: 'Pot',
        69: 'Cuillère',
        70: 'Fouet',
        71: 'Ordinateur portable',
        72: 'Téléphone',
        73: 'Canapé en forme de L',
        74: 'Canapé avec accoudoir gauche',
        75: 'Canapé avec accoudoir droit',
        76: 'Canapé en forme de U',
        77: 'Escaliers',
        78: 'Table',
        79: 'Papier toilette',
        80: 'Couteau',
        81: 'Cuillère',
        82: 'Fourchette',
        83: 'Chou',
        84: 'Carotte',
        85: 'Aubergine',
        86: 'Oignon',
        87: 'Verre',
        88: 'Bouteille d\'eau',
        89: 'Fenêtre fixe',
        90: 'Fenêtre coulissante'

    }

    # Initialize speech recognition
    recognizer = sr.Recognizer()

    # Main loop for video capture and object detection
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erreur: Impossible de lire la vidéo de la webcam.")
                break

            # Detect objects in the current frame
            results = model.predict(frame, conf=0.1)

            # Check if there are any detections
            if len(results) == 0:
                print("Aucune détection")
            else:
                for result in results:
                    if hasattr(result, 'boxes'):
                        for box in result.boxes:
                            class_id = int(box.cls)  # Correct attribute for class id
                            class_name = class_mapping.get(class_id, "Inconnu")
                            detection_message = f"Objet détecté: {class_name}"
                            print(detection_message)
                            engine.say(detection_message)
                            engine.runAndWait()  # Process speech immediately

            # Display the frame
            cv2.imshow("Frame", frame)

            # Listen for speech command
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            try:
                command = recognizer.recognize_google(audio, language="fr-FR")
                print("Commande détectée:", command)
                if "stop" in command.lower() or "arrêter" in command.lower():
                    if "stop" in command.lower():
                        # Rediriger vers landingpage.html
                        return render(request, 'bye.html')
                    else:
                        # Rediriger vers thanks.html
                        return render(request, 'thanks.html')
            except sr.UnknownValueError:
                print("Impossible de comprendre la commande.")
            except sr.RequestError as e:
                print("Erreur lors de la demande à l'API Google Speech Recognition:", e)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Release resources
        cap.release()
        cv2.destroyAllWindows()
        engine.stop()  # Properly stop the engine when done



###################################################################################################

def load_models():
    """Load the pre-trained models for age, gender, and emotion prediction."""
    age_model_path = r'C:\Users\routa\OneDrive\Bureau\djangoProject\djangoProject\djangoProject\emotionDect\model\age_model.h5'
    gender_model_path = r'C:\Users\routa\OneDrive\Bureau\djangoProject\djangoProject\djangoProject\emotionDect\model\gender_model.h5'
    emotion_model_path = r'C:\Users\routa\OneDrive\Bureau\djangoProject\djangoProject\djangoProject\emotionDect\model\emotion_model.h5'

    age_model = load_model(age_model_path)
    gender_model = load_model(gender_model_path)
    emotion_model = load_model(emotion_model_path)

    return age_model, gender_model, emotion_model

def predict(image, age_model, gender_model, emotion_model, engine):
    """Predict the age, gender, and emotion for the given image."""
    age_ranges = ['1-2', '3-9', '13-20', '21-27', '28-45', '46-65', '66-116']
    gender_ranges = ['male', 'female']
    emotion_ranges = ['happy', 'sad', 'neutral']

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        print("No faces detected.")
        return

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (203, 12, 255), 3)
        img_gray = gray[y:y + h, x:x + w]

        emotion_img = cv2.resize(img_gray, (48, 48))
        emotion_input = emotion_img.reshape(1, 48, 48, 1)
        output_emotion = emotion_ranges[np.argmax(emotion_model.predict(emotion_input))]

        gender_img = cv2.resize(img_gray, (100, 100))
        gender_input = gender_img.reshape(1, 100, 100, 1)
        output_gender = gender_ranges[np.argmax(gender_model.predict(gender_input))]

        age_img = cv2.resize(img_gray, (200, 200))
        age_input = age_img.reshape(1, 200, 200, 1)
        output_age = age_ranges[np.argmax(age_model.predict(age_input))]

        output_str = f"objet detecte : {output_gender} age de {output_age}, qui est {output_emotion}"
        print(output_str)
        engine.say(output_str)
        engine.runAndWait()

        text_col = (255, 255, 255)
        box_col = (203, 12, 255)
        y0, dy = y, 30
        for j, line in enumerate(output_str.split('\n')):
            yj = y0 + j * dy
            cv2.rectangle(image, (x, yj - dy), (x + w, yj), box_col, -1)
            cv2.putText(image, line, (x, yj), cv2.FONT_HERSHEY_SIMPLEX, 1, text_col, 2)

    cv2.imshow('Real-Time Face Detection', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


def main(request):
    """Main function to execute the script."""
    age_model, gender_model, emotion_model = load_models()
    engine = pyttsx3.init()
    cap = cv2.VideoCapture(0)

    recognizer = sr.Recognizer()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        predict(frame, age_model, gender_model, emotion_model, engine)

        # Listen for voice command
        with sr.Microphone() as source:
            print("Say 'stop' to end the detection.")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            print("User said:", command)
            if 'stop' in command:
                cap.release()
                cv2.destroyAllWindows()
                return render(request, 'thanks.html')
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

    cap.release()
    cv2.destroyAllWindows()


###########################################################################################################
def shop(request):
    # Initialize the YOLO model
    model = YOLO(r"C:\Users\routa\OneDrive\Bureau\djangoProject\djangoProject\djangoProject\models\shop.pt")

    # Try opening the webcam
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise IOError("Erreur: Impossible d'ouvrir la webcam.")
    except IOError as e:
        print(e)
        exit(1)

    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Configure speech rate
    engine.setProperty('rate', 150)  # Speech rate, adjust as necessary

    # Find and set a French voice
    voices = engine.getProperty('voices')
    french_voice = next((voice for voice in voices if 'french' in voice.languages), None)
    if french_voice:
        engine.setProperty('voice', french_voice.id)
    else:
        print("French voice not found, using default.")

    # Define class mapping
    class_mapping = {
        # Your class mapping here
        0: 'Albane Lait',
        1: 'Albane Moniich Fraise',
        2: 'Albane Moniich Fruits Exotiques',
        3: 'Centrale Lait',
        4: 'Chergui Creme Cerise',
        5: 'Chergui Creme Citrone',
        6: 'Chergui Creme Fruits desbois',
        7: 'Chergui Creme Mangue',
        8: 'Chergui Daya Ananas Coco',
        9: 'Chergui Daya Ananas Coco 900ml',
        10: 'Chergui Daya Avocat',
        11: 'Chergui Daya Fraise',
        12: 'Chergui Jnane Coco',
        13: 'Chergui Jnane Fraise',
        14: 'Chergui Jnane Nature Sucre',
        15: 'Chergui Jnane Peche',
        16: 'Chergui Jnane vanille',
        17: 'Chergui Lait',
        18: 'Chergui Lait 900 ml',
        19: 'Chergui Lait 900ml',
        20: 'Chergui Lben',
        21: 'Chergui Lben Beldi',
        22: 'Chergui Mini Daya Fraise',
        23: 'Chergui Mini Daya Peche',
        24: 'Chergui Mini Daya Vanille',
        25: 'Dan - up Fraise',
        26: 'Dan - up Peche',
        27: 'Dan - up Vanille',
        28: 'Danone Assil Banane',
        29: 'Danone Assil Fraise',
        30: 'Danone Assil Vanille',
        31: 'Danone Lait',
        32: 'Danone Lben',
        33: 'Danone Max Fraise',
        34: 'Danone Max Vanille',
        35: 'Danone Veloute Fraise',
        36: 'Danone Veloute Fruits Exotiques',
        37: 'Danone Veloute Pistache',
        38: 'Danone Veloute Vanille',
        39: 'Gervais Fromage Frais',
        40: 'Jaouda Cremy Fraise',
        41: 'Jaouda Cremy Pistache',
        42: 'Jaouda Cremy Vanille',
        43: 'Jaouda Drink Happy Fraise',
        44: 'Jaouda Drink Happy Vanille',
        45: 'Jaouda Ghilal Cereales',
        46: 'Jaouda Ghilal Fruits Rouges',
        47: 'Jaouda Lait',
        48: 'Jaouda Lben',
        49: 'Jaouda Lben 950g',
        50: 'Jaouda Perly Nature',
        51: 'Jaouda Perly Nature Sucre',
        52: 'Jaouda Tendre Citrone',
        53: 'Jibal Brasse Banane',
        54: 'Jibal Brasse Fraise',
        55: 'Jibal Brasse Mangue',
        56: 'Jibal Brasse Vanille',
        57: 'Jibal Ferme Banane',
        58: 'Jibal Ferme Vanille',
        59: 'Jibal Fraise',
        60: 'Jibal Fruits Fruits Rouges Granola',
        61: 'Jibal Fruits Muesli et Noix',
        62: 'Jibal Lait',
        63: 'Jibal Lben',
        64: 'Jibal Mangue',
        65: 'Jibal Panache',
        66: 'Kiri Brasse Fraise',
        67: 'Kiri Brasse Pistache',
        68: 'Kiri Brasse Vanille',
        69: 'Kiri Nature Sucre',
        70: 'Kiri Yaourt Ferme Banane',
        71: 'Kiri Yaourt Ferme Fraise',
        72: 'Kiri Yaourt Ferme Vanille',
        73: 'Pack Chergui Creme',
        74: 'Pack Chergui Creme Cerise',
        75: 'Pack Chergui Creme Citrone',
        76: 'Pack Chergui Creme Fruits des bois',
        77: 'Pack Chergui Creme Mangue',
        78: 'Pack Chergui Jnane',
        79: 'Pack Chergui Jnane Coco',
        80: 'Pack Chergui Jnane Fraise',
        81: 'Pack Chergui Jnane Nature',
        82: 'Pack Chergui Jnane Nature Sucre',
        83: 'Pack Chergui Jnane Peche',
        84: 'Pack Chergui Jnane Vanille',
        85: 'Pack Chergui Mini Daya Fraise',
        86: 'Pack Chergui Mini Daya Peche',
        87: 'Pack Chergui Mini Daya Vanille',
        88: 'Pack Dan - up Fraise',
        89: 'Pack Dan - up Peche',
        90: 'Pack Dan - up Vanille',
        91: 'Pack Danone Assil Banane',
        92: 'Pack Danone Assil Vanille',
        93: 'Pack Danone Veloute Vanille',
        94: 'Pack Danone Veloute Fraise',
        95: 'Pack Danone Veloute Fruits Exotiques',
        96: 'Pack Danone Veloute Pistache',
        97: 'Pack GervaisFromage Frais',
        98: 'Pack Jaouda Cremy Vanille',
        99: 'Pack Jaouda Ghilal Cereales',
        100: 'Pack Jaouda Perly Nature',
        101: 'Pack Jaouda Perly Nature Sucre',
        102: 'Pack Jaouda Tendre Citrone',
        103: 'Pack Jibal Brasse Fraise',
        104: 'Pack Jibal Brasse Mangue',
        105: 'Pack Jibal Brasse Vanille',
        106: 'Pack JibalFerme Banane',
        107: 'Pack Jibal Ferme Vanille',
        108: 'Pack Jibal Fruits Fruits Rouges Granola',
        109: 'Pack Jibal Fruits Muesli et Noix',
        110: 'Pack Kiri Brasse Fraise',
        111: 'Pack Kiri Brasse Pistache',
        112: 'Pack Kiri Brasse Vanille',
        113: 'Pack Kiri Yaourt Ferme Banane',
        114: 'Pack Kiri Yaourt Ferme Frais',
        115: 'Pack Kiri Yaourt Ferme Vanille',
        116: 'Pack Tom Milk',
        117: 'Tom Milk Banane',
        118: 'Tom Milk Coco',
        119: 'Tom Milk Fraise',
        120: 'Tom Milk Peche',
        121: 'TomMilk Vanille',
        122: 'Yoplait Petits Filous Banane',
        123: 'Yoplait PetitsFilous Pomme',
        124: 'Yoplait Yop Fraise',
        125: 'Yoplait Yop Vanille',
        126: 'Apple Fresh',
        127: 'Apple Rotten',
        128: 'Apple Semifresh',
        129: 'Apple Semirotten',
        130: 'Banana Fresh',
        131: 'Banana Rotten',
        132: 'Banana Semifresh',
        133: 'Banana Semirotten',
        134: 'Mango Fresh',
        135: 'Mango Rotten',
        136: 'Mango Semifresh',
        137: 'Mango Semirotten',
        138: 'Melon Fresh',
        139: 'Melon Rotten',
        140: 'Melon Semifresh',
        141: 'Melon Semirotten',
        142: 'Orange Fresh',
        143: 'Orange Rotten',
        144: 'Orange Semifresh',
        145: 'Orange Semirotten',
        146: 'Peach Fresh',
        147: 'Peach Rotten',
        148: 'Peach Semifresh',
        149: 'Peach Semirotten',
        150: 'Pear Fresh',
        151: 'Pear Rotten',
        152: 'Pear Semifresh',
        153: 'Pear Semirotten',
        154: 'PearSemifresh',
        155: 'Fresh_Carrot',
        156: 'Fresh_Cucumber',
        157: 'Fresh_Pepper',
        158: 'Fresh_Potato',
        159: 'Fresh_Tomato',
        160: 'Rotten_Carrot',
        161: 'Rotten_Cucumber',
        162: 'Rotten_Pepper',
        163: 'Rotten_Potato',
        164: 'Rotten_Tomato',
        165: 'Shin',
        166: 'Strips',
        167: 'tenderloin',
        168: 'tenderloin_steak',
        169: 'egg',
        170: 'chicken',
        171: 'couscous_dari',

    }

    # Initialize speech recognition
    recognizer = sr.Recognizer()

    # Main loop for video capture and object detection
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erreur: Impossible de lire la vidéo de la webcam.")
                break

            # Detect objects in the current frame
            results = model.predict(frame, conf=0.1)

            # Check if there are any detections
            if len(results) == 0:
                print("Aucune détection")
            else:
                for result in results:
                    if hasattr(result, 'boxes'):
                        for box in result.boxes:
                            class_id = int(box.cls)  # Correct attribute for class id
                            class_name = class_mapping.get(class_id, "Inconnu")
                            detection_message = f"Objet détecté: {class_name}"
                            print(detection_message)
                            engine.say(detection_message)
                            engine.runAndWait()  # Process speech immediately

            # Display the frame
            cv2.imshow("Frame", frame)

            # Listen for speech command
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            try:
                command = recognizer.recognize_google(audio, language="fr-FR")
                print("Commande détectée:", command)
                if "stop" in command.lower() or "arrêter" in command.lower():
                    if "stop" in command.lower():
                        # Rediriger vers landingpage.html
                        return render(request, 'bye.html')
                    else:
                        # Rediriger vers thanks.html
                        return render(request, 'thanks.html')
            except sr.UnknownValueError:
                print("Impossible de comprendre la commande.")
            except sr.RequestError as e:
                print("Erreur lors de la demande à l'API Google Speech Recognition:", e)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Release resources
        cap.release()
        cv2.destroyAllWindows()
        engine.stop()  # Properly stop the engine when done





##############################################################################

def outdoor(request):
    # Initialize the YOLO model
    model = YOLO(r"C:\Users\routa\OneDrive\Bureau\djangoProject\djangoProject\djangoProject\models\outdoor.pt")

    # Try opening the webcam
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise IOError("Erreur: Impossible d'ouvrir la webcam.")
    except IOError as e:
        print(e)
        exit(1)

    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Configure speech rate
    engine.setProperty('rate', 150)  # Speech rate, adjust as necessary

    # Find and set a French voice
    voices = engine.getProperty('voices')
    french_voice = next((voice for voice in voices if 'french' in voice.languages), None)
    if french_voice:
        engine.setProperty('voice', french_voice.id)
    else:
        print("French voice not found, using default.")

    # Define class mapping
    class_mapping = {
        # Your class mapping here
        0: 'arbres',
        1: 'ATM',
        2: 'bus station',
        3: 'passage piéton',
        4: 'Distributeurs automatiques',
        5: 'porte',
        6: 'Escaliers',
        7: 'feu vert',
        8: 'feu jaune',
        9: 'feu rouge',
        10: 'Lampadaire',
        11: 'Les chaises public',
        12: 'panneau de danger',
        13: 'panneau sortie',
        14: 'Velo',
        15: 'bus',
        16: 'voiture',
        17: 'Hiace',
        18: 'taxi',
        19: 'tracteur',
        20: 'camion',
        21: 'fenetre',


    }

    # Initialize speech recognition
    recognizer = sr.Recognizer()

    # Main loop for video capture and object detection
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erreur: Impossible de lire la vidéo de la webcam.")
                break

            # Detect objects in the current frame
            results = model.predict(frame, conf=0.1)

            # Check if there are any detections
            if len(results) == 0:
                print("Aucune détection")
            else:
                for result in results:
                    if hasattr(result, 'boxes'):
                        for box in result.boxes:
                            class_id = int(box.cls)  # Correct attribute for class id
                            class_name = class_mapping.get(class_id, "Inconnu")
                            detection_message = f"Objet détecté: {class_name}"
                            print(detection_message)
                            engine.say(detection_message)
                            engine.runAndWait()  # Process speech immediately

            # Display the frame
            cv2.imshow("Frame", frame)

            # Listen for speech command
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            try:
                command = recognizer.recognize_google(audio, language="fr-FR")
                print("Commande détectée:", command)
                if "stop" in command.lower() or "arrêter" in command.lower():
                    if "stop" in command.lower():
                        # Rediriger vers landingpage.html
                        return render(request, 'bye.html')
                    else:
                        # Rediriger vers thanks.html
                        return render(request, 'thanks.html')
            except sr.UnknownValueError:
                print("Impossible de comprendre la commande.")
            except sr.RequestError as e:
                print("Erreur lors de la demande à l'API Google Speech Recognition:", e)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Release resources
        cap.release()
        cv2.destroyAllWindows()
        engine.stop()  # Properly stop the engine when done


#####################################################################################################################

# Fonction pour détecter le texte dans une image en utilisant l'API Vision de Google Cloud
def detect_text(image):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\routa\OneDrive\Bureau\Projet ensa\Ai Projet\final\texte\aiprj-420118-f4f146438097.json'
        client = vision.ImageAnnotatorClient()
        _, img_encoded = cv2.imencode('.jpg', image)
        img_bytes = img_encoded.tobytes()
        image = vision.Image(content=img_bytes)
        response = client.text_detection(image=image)
        time.sleep(3)
        texts = response.text_annotations
        ocr_text = [text.description for text in texts]
        return ocr_text



def lire_texte(texte, langue):
    output = gTTS(text=texte, lang=langue, slow=False)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_filename = temp_file.name
        output.save(temp_filename)
    pygame.init()
    pygame.mixer.music.load(temp_filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()
    pygame.quit()
    os.remove(temp_filename)




def listen_for_response():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, phrase_time_limit=5)
            try:
                response = r.recognize_google(audio, language="fr-FR").lower()
                if response.startswith("oui"):
                    return True
                elif response.startswith("non"):
                    return False
                elif response.startswith("stop"):
                    return 1
                else:
                    lire_texte("Désolé, je n'ai pas compris. Veuillez répondre par 'oui' ou 'non'.",'fr')
                    print("Désolé, je n'ai pas compris. Veuillez répondre par 'oui' ou 'non'.")
            except sr.UnknownValueError:
                lire_texte("Désolé, je n'ai pas compris. Veuillez répéter.",'fr')
                print("Désolé, je n'ai pas compris. Veuillez répéter.")
            except sr.RequestError as e:
                print("Impossible de demander des résultats au service de reconnaissance vocale de Google ; {0}".format(
                    e))
                return None


def detect_language(text):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\routa\OneDrive\Bureau\Projet ensa\Ai Projet\final\texte\translate_key.json'
    client = translate.Client()
    result = client.detect_language(text)
    detected_language = result[0]['language']
    print(f"Langue détectée : {detected_language}")
    return detected_language



def translate_text(text, target_language):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\routa\OneDrive\Bureau\Projet ensa\Ai Projet\final\texte\translate_key.json'
    detected_language = detect_language(text)
    client = translate.Client()
    result = client.translate(text, target_language=target_language, source_language=detected_language)
    translated_text = result[0]['translatedText']  # Accéder au premier élément de la liste
    print(f"Texte traduit : {translated_text}")
    if target_language == "en":
        lire_texte(translated_text, langue='en')
    elif target_language == "fr":
        lire_texte(translated_text, langue='fr')
    elif target_language == "es":
        lire_texte(translated_text, langue='es')
    elif target_language == "ar":
        lire_texte(translated_text, langue='ar')
    else:
        lire_texte("choix invalide", "fr")




def vice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, phrase_time_limit=7)  # Augmenter le temps d'écoute
            try:
                response = r.recognize_google(audio, language="fr-FR").lower()
                languages = {
                    1: 'en',
                    2: 'fr',
                    3: 'es',
                    4: 'ar'
                }
                if response.isdigit():
                    language_num = int(response)
                    if language_num in languages:
                        return languages[language_num]
                lire_texte("Désolé, je n'ai pas compris. Veuillez choisir un numéro correspondant à la langue cible.",
                           'fr')
                print("Désolé, je n'ai pas compris. Veuillez choisir un numéro correspondant à la langue cible.")
            except sr.UnknownValueError:
                lire_texte("Désolé, je n'ai pas compris. Veuillez répéter.", 'fr')
                print("Désolé, je n'ai pas compris. Veuillez répéter.")
            except sr.RequestError as e:
                print("Impossible de demander des résultats au service de reconnaissance vocale de Google ; {0}".format(
                    e))
                return None


def select_language(text,choice):
    if choice == "en":
        translate_text(text, 'en')
    elif choice == "fr":
        translate_text(text, 'fr')
    elif choice == "es":
        translate_text(text, 'es')
    elif choice == "ar":
        translate_text(text, 'ar')
    else :
        lire_texte("le choix invalide","fr")


def text_to_speech(text,lang):
    full_text = ' '.join(text)
    if lang == "en":
        lire_texte(full_text, langue='en')
    elif lang == "fr":
        lire_texte(full_text, langue='fr')
    elif lang == "es":
        lire_texte(full_text, langue='es')
    elif lang == "ar":
        lire_texte(full_text, langue='ar')
    else :
        lire_texte("choix invalide","fr")



def stop_execute():
    lire_texte("Veuillez taper 'stop' pour arrêter la fonctionnalité.", 'fr')
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, phrase_time_limit=5)
            try:
                response = r.recognize_google(audio, language="fr-FR").lower()
                if response.startswith("stop"):
                    break
                else:
                    lire_texte("Désolé, je n'ai pas compris.", 'fr')
                    print("Désolé, je n'ai pas compris.")
            except sr.UnknownValueError:
                lire_texte("Désolé, je n'ai pas compris. Veuillez répéter.", 'fr')
                print("Désolé, je n'ai pas compris. Veuillez répéter.")
            except sr.RequestError as e:
                print("Impossible de demander des résultats au service de reconnaissance vocale de Google ; {0}".format(
                    e))
                return None



def text(request):
    # Capture vidéo depuis la webcam
    cap = cv2.VideoCapture(0)
    lire_texte( "Bonjour !Je suis votre assistant de lecture de texte. Assurez-vous que la caméra est positionnée vers le texte que vous souhaitez lire",'fr')
    while True:
        # Capture d'image par image et Afficher l'image capturée
        ret, frame = cap.read()
        cv2.imshow('Webcam', frame)
        # Vérifier si 'q' est pressé pour quitter
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # Convertir l'image en niveaux de gris pour une meilleure détection de texte
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Vérifier s'il y a du texte dans l'image
        text = detect_text(gray)
        if text:
            lire_texte("Texte détecté ! Voulez-vous le lire ? Dites 'oui' pour lire le texte, ou 'non' pour passer.",'fr')
            print("Texte détecté ! Voulez-vous le lire ? Dites 'oui' pour lire le texte, ou 'non' pour passer.")
            response = listen_for_response()
            if response is True:
                language = detect_language(text)
                lire_texte("la langue de cette text est :", 'fr')
                lire_texte(language, 'fr')
                if language== "en":
                    lire_texte("anglais", 'fr')
                elif language == "fr":
                    lire_texte("francais", 'fr')
                elif language == "es":
                    lire_texte("espagnole", 'fr')
                elif language == "ar":
                    lire_texte("arabe", 'fr')
                print(text)
                text_to_speech(text,language)
                print("Voulez-vous traduire ce texte? Dites 'oui' pour traduire le texte, ou 'non' pour passer ")
                lire_texte("Voulez-vous traduire ce texte? Dites 'oui' pour traduire le texte, ou 'non' pour passer ",'fr')
                resp = listen_for_response()
                if resp is True:
                    lire_texte("Choisissez le nombre correspond la langue cible : 1 pour langue Anglais ,2 pour langue Français , 3 pour langue Espagnol, 4 pour langue Arabe",'fr')
                    print("Choisissez le nombre correspond la langue cible :")
                    print("1. Anglais\n2. Français\n3. Espagnol\n4. Arabe")
                    langue_cible = vice()
                    select_language(text,langue_cible)
                    lire_texte("la lecture est termine.", 'fr')
                    lire_texte("dire 'stop' pour arrêter la fonctionnalité ou non pour passer a autre lecture.", 'fr')
                    res = listen_for_response()
                    if res == 1 :
                        break
                    elif res is False:
                        lire_texte("Passage à la lecture suivante.", 'fr')
                        print("Passage à la lecture suivante.")
                        break
                elif resp is False:
                    lire_texte("Passage à la lecture suivante.",'fr')
                    print("Passage à la lecture suivante.")
                    break
            elif response is False:
                lire_texte("Passage à la lecture suivante.",'fr')
                print("Passage à la lecture suivante.")
                break

    cap.release()
    cv2.destroyAllWindows()
    return render(request, 'thanks.html')








