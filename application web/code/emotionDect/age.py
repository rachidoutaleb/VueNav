import argparse
import os
import cv2
import numpy as np
from keras.models import load_model
from matplotlib import pyplot as plt
import pyttsx3

def load_models():
    """Load the pre-trained models for age, gender and emotion prediction."""
    age_model_path = './model/age_model.h5'
    gender_model_path = './model/gender_model.h5'
    emotion_model_path = './model/emotion_model.h5'

    age_model = load_model(age_model_path)
    gender_model = load_model(gender_model_path)
    emotion_model = load_model(emotion_model_path)

    return age_model, gender_model, emotion_model

def predict(image, age_model, gender_model, emotion_model, engine):
    """Predict the age, gender, and emotion for the given image."""
    age_ranges = ['1-2', '3-9', '10-20', '21-27', '28-45', '46-65', '66-116']
    gender_ranges = ['male', 'female']
    emotion_ranges = ['positive', 'negative', 'neutral']

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (203, 12, 255), 3)

        img_gray = gray[y:y + h, x:x + w]

        emotion_img = cv2.resize(img_gray, (48, 48), interpolation=cv2.INTER_AREA)
        emotion_image_array = np.array(emotion_img)
        emotion_input = np.expand_dims(emotion_image_array, axis=0)
        output_emotion = emotion_ranges[np.argmax(emotion_model.predict(emotion_input))]

        gender_img = cv2.resize(img_gray, (100, 100), interpolation=cv2.INTER_AREA)
        gender_image_array = np.array(gender_img)
        gender_input = np.expand_dims(gender_image_array, axis=0)
        output_gender = gender_ranges[np.argmax(gender_model.predict(gender_input))]

        age_image = cv2.resize(img_gray, (200, 200), interpolation=cv2.INTER_AREA)
        age_input = age_image.reshape(-1, 200, 200, 1)
        output_age = age_ranges[np.argmax(age_model.predict(age_input))]

        output_str = output_gender + ', ' + output_age + ', ' + output_emotion
        print(output_str)

        # Speak the prediction
        engine.say(output_str)
        engine.runAndWait()

        text_col = (255, 255, 255)
        box_col = (203, 12, 255)

        y0, dy = y, 30
        for j, line in enumerate(output_str.split('\n')):
            yj = y0 + j * dy
            cv2.rectangle(image, (x, yj - dy), (x + w, yj), box_col, -1)
            cv2.putText(image, line, (x, yj), cv2.FONT_HERSHEY_SIMPLEX, 1, text_col,
                        2)  # Increased font size and thickness

    cv2.imshow('Real-Time Face Detection', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()

def main():
    """Main function to execute the script."""
    age_model, gender_model, emotion_model = load_models()
    engine = pyttsx3.init()

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        predict(frame, age_model, gender_model, emotion_model, engine)

    cap.release()
    cv2.destroyAllWindows()


main()
