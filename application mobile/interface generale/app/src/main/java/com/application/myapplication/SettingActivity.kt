package com.application.myapplication

import android.content.Context
import android.content.Intent
import android.media.AudioManager
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Slider
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.application.myapplication.ui.theme.MyApplicationTheme
import java.util.Locale

class SettingActivity : ComponentActivity(), RecognitionListener {
    private lateinit var audioManager: AudioManager
    private lateinit var speechRecognizer: SpeechRecognizer
    private lateinit var recognizerIntent: Intent

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        audioManager = getSystemService(Context.AUDIO_SERVICE) as AudioManager
        initSpeechRecognizer()

        setContent {
            MyApplicationTheme {
                val maxVolume = audioManager.getStreamMaxVolume(AudioManager.STREAM_MUSIC)
                var volume by remember { mutableStateOf(audioManager.getStreamVolume(AudioManager.STREAM_MUSIC).toFloat()) }

                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(16.dp),
                    verticalArrangement = Arrangement.Center,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(text = "Adjust Volume", style = MaterialTheme.typography.headlineMedium)
                    Spacer(modifier = Modifier.height(16.dp))
                    Slider(
                        value = volume,
                        onValueChange = { newVolume ->
                            volume = newVolume
                            audioManager.setStreamVolume(
                                AudioManager.STREAM_MUSIC,
                                newVolume.toInt(),
                                AudioManager.FLAG_SHOW_UI
                            )
                        },
                        valueRange = 0f..maxVolume.toFloat(),
                        steps = maxVolume - 1
                    )
                }
            }
        }
        startVoiceCommand()
    }

    private fun initSpeechRecognizer() {
        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this)
        speechRecognizer.setRecognitionListener(this)
        recognizerIntent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault())
        }
    }

    private fun startVoiceCommand() {
        speechRecognizer.startListening(recognizerIntent)
    }

    override fun onResults(results: Bundle?) {
        results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)?.let { matches ->
            if (matches.isNotEmpty()) {
                when (matches[0].lowercase(Locale.ROOT)) {
                    "up","haut" -> adjustVolume(true)
                    "down","bas"  -> adjustVolume(false)
                    "return" -> navigateToFirstPage()  // Action when "return" is spoken
                }
            }
        }
        // Make sure to restart listening after processing the results
        startVoiceCommand()  // Correct method name
    }


    private fun navigateToFirstPage() {
        // Code to navigate to the first page of your application
        // For example: startActivity(Intent(this, MainActivity::class.java))
        // Add any necessary logic to handle the transition and state reset
        finish()  // Assuming this is not the main activity, finish current activity and return
    }

    override fun onError(error: Int) {
        Handler(Looper.getMainLooper()).postDelayed({
            startVoiceCommand()  // Retry after 1 second
        }, 1000)
    }

    private fun adjustVolume(increase: Boolean) {
        val currentVolume = audioManager.getStreamVolume(AudioManager.STREAM_MUSIC)
        val maxVolume = audioManager.getStreamMaxVolume(AudioManager.STREAM_MUSIC)
        if (increase && currentVolume < maxVolume) {
            audioManager.adjustStreamVolume(AudioManager.STREAM_MUSIC, AudioManager.ADJUST_RAISE, AudioManager.FLAG_SHOW_UI)
        } else if (!increase && currentVolume > 0) {
            audioManager.adjustStreamVolume(AudioManager.STREAM_MUSIC, AudioManager.ADJUST_LOWER, AudioManager.FLAG_SHOW_UI)
        }
    }

    // Implementation of other RecognitionListener methods...
    override fun onReadyForSpeech(params: Bundle?) {}
    override fun onBeginningOfSpeech() {}
    override fun onRmsChanged(rmsdB: Float) {}
    override fun onBufferReceived(buffer: ByteArray?) {}
    override fun onEndOfSpeech() {}
    override fun onPartialResults(partialResults: Bundle?) {}
    override fun onEvent(eventType: Int, params: Bundle?) {}
}
