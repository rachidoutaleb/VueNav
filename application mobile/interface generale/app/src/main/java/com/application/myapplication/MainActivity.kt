package com.application.myapplication

import android.content.Intent
import android.os.Bundle
import android.speech.RecognizerIntent
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.application.myapplication.ui.theme.MyApplicationTheme
import java.util.*

class MainActivity : ComponentActivity(), TextToSpeech.OnInitListener {

    private lateinit var textToSpeech: TextToSpeech
    private val voiceRecognitionRequestCode = 100

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        textToSpeech = TextToSpeech(this, this)
        setContent {
            MyApplicationTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    Greeting(this@MainActivity)
                }
            }
        }
    }

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            textToSpeech.language = Locale.getDefault()
            textToSpeech.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
                override fun onStart(utteranceId: String?) {}
                override fun onDone(utteranceId: String?) {
                    if (utteranceId == "Prompt") {
                        startVoiceRecognitionActivity()
                    }
                }
                override fun onError(utteranceId: String?) {}
            })
            startVoiceRecognitionActivity() // Start voice recognition immediately after TTS is initialized
        }
    }

    private fun startVoiceRecognitionActivity() {
        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
        intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Please speak the name of the button to activate")
        startActivityForResult(intent, voiceRecognitionRequestCode)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == voiceRecognitionRequestCode && resultCode == RESULT_OK) {
            val matches = data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
            val command = matches?.get(0)?.toLowerCase(Locale.getDefault())
            when (command) {
                "indoor", "intérieur" -> startActivity(Intent(this, IndoorActivity::class.java))
                "outdoor", "extérieur" -> startActivity(Intent(this, OutdoorActivity::class.java))
                "face" -> startActivity(Intent(this, FaceActivity::class.java))
                "site" -> startActivity(Intent(this, SiteActivity::class.java))
                "map","Maps", "carte" -> startActivity(Intent(this, MapActivity::class.java))
                "help", "aide" -> startActivity(Intent(this, HelpActivity::class.java))
                "settings","setting","seting","paramètres","paramètre" -> startActivity(Intent(this, SettingActivity::class.java))
                else -> {
                    textToSpeech.speak("Il y a 7 fonctionnalités : Indoor, Outdoor, Face, Map, Site, Help et Settings. SVP choisissez une.", TextToSpeech.QUEUE_FLUSH, null, "Prompt")
                }
            }
        } else {
            startVoiceRecognitionActivity() // Restart voice recognition if something went wrong or no result obtained
        }
    }

    override fun onDestroy() {
        if (this::textToSpeech.isInitialized) {
            textToSpeech.stop()
            textToSpeech.shutdown()
        }
        super.onDestroy()
    }

    @Composable
    fun Greeting(activity: ComponentActivity) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalArrangement = Arrangement.SpaceEvenly,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Row(horizontalArrangement = Arrangement.SpaceEvenly) {
                CircularButton("Indoor", activity, IndoorActivity::class.java)
                CircularButton("Outdoor", activity, OutdoorActivity::class.java)
            }
            Row(horizontalArrangement = Arrangement.SpaceEvenly) {
                CircularButton("Face", activity, FaceActivity::class.java)
                CircularButton("Site", activity, SiteActivity::class.java)
            }
            Row(horizontalArrangement = Arrangement.SpaceEvenly) {
                CircularButton("Map", activity, MapActivity::class.java)
                CircularButton("Help", activity, HelpActivity::class.java)
            }
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.Center) {
                CircularButton("Settings", activity, SettingActivity::class.java)
            }
        }
    }

    @Composable
    fun CircularButton(text: String, activity: ComponentActivity, activityClass: Class<*>) {
        Button(
            onClick = { activity.startActivity(Intent(activity, activityClass)) },
            modifier = Modifier
                .size(180.dp)
                .padding(8.dp),
            shape = CircleShape
        ) {
            Text(text)
        }
    }

    @Preview(showBackground = true)
    @Composable
    fun GreetingPreview() {
        MyApplicationTheme {
            Greeting(this@MainActivity)
        }
    }
}
