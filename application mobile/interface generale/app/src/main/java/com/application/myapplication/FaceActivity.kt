package com.application.myapplication

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.application.myapplication.ui.theme.MyApplicationTheme
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.Alignment

class FaceActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MyApplicationTheme {
                // Un conteneur Column pour organiser les éléments verticalement
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(16.dp),
                    verticalArrangement = Arrangement.Center,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(text = "Welcome to Indoor Activity", style = MaterialTheme.typography.headlineMedium)
                    Spacer(modifier = Modifier.height(16.dp)) // Espace entre le texte et le bouton
                    Button(onClick = { finish() }) { // Utilisez `finish()` pour fermer cette activité et revenir à la précédente
                        Text("Return")
                    }
                }
            }
        }
    }
}
