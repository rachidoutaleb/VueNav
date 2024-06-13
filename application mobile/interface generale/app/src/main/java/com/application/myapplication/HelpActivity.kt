package com.application.myapplication

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class HelpActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Vérifier si la permission d'appel est déjà accordée
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CALL_PHONE) != PackageManager.PERMISSION_GRANTED) {
            // Demander la permission d'appel
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.CALL_PHONE), 1)
        } else {
            // Permission déjà accordée
            makeEmergencyCall()
        }
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == 1 && grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            // Permission accordée
            makeEmergencyCall()
        } else {
            // Permission refusée
            finish() // Quitter l'activité si la permission n'est pas accordée
        }
    }

    private fun makeEmergencyCall() {
        val intent = Intent(Intent.ACTION_CALL)  // Utilisez ACTION_CALL pour un appel direct
        intent.data = Uri.parse("tel:111")      // Numéro d'urgence
        startActivity(intent)
    }
}
