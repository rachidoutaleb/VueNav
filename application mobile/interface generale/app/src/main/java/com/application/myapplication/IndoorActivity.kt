package com.application.myapplication

import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.util.Log
import android.widget.Toast
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

class IndoorActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MyApplicationTheme {
                Column(
                    modifier = Modifier.fillMaxSize().padding(16.dp),
                    verticalArrangement = Arrangement.Center,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(text = "Welcome to Indoor Activity", style = MaterialTheme.typography.headlineMedium)
                    Spacer(modifier = Modifier.height(16.dp))
                    Button(onClick = { findAndOpenApp("Bemyeye") }) {
                        Text("Open Bemyeye App")
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                    Button(onClick = { finish() }) {
                        Text("Return")
                    }
                }
            }
        }
    }

    private fun findAndOpenApp(appName: String) {
        val pm = packageManager
        val packages = pm.getInstalledApplications(PackageManager.GET_META_DATA)
        var appFound = false
        for (packageInfo in packages) {
            val label = pm.getApplicationLabel(packageInfo) as String
            if (label.equals(appName, ignoreCase = true)) {
                appFound = true
                val launchIntent = pm.getLaunchIntentForPackage(packageInfo.packageName)
                if (launchIntent != null) {
                    startActivity(launchIntent)
                    break
                } else {
                    Toast.makeText(this, "$appName found, but no launch intent available.", Toast.LENGTH_LONG).show()
                }
            }
        }
        if (!appFound) {
            Toast.makeText(this, "$appName not found.", Toast.LENGTH_LONG).show()
        }
    }
}
