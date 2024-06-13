package com.example.maps

import android.Manifest
import android.content.ActivityNotFoundException
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Address
import android.location.Geocoder
import android.location.Location
import android.net.Uri
import android.os.Bundle
import android.speech.RecognitionListener


import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.widget.SearchView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.LocationServices
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.BitmapDescriptorFactory
import com.google.android.gms.maps.model.LatLng
import com.google.android.gms.maps.model.MarkerOptions
import com.google.android.gms.tasks.OnSuccessListener
import com.google.android.gms.tasks.Task
import java.io.IOException


class MainActivity : AppCompatActivity(), OnMapReadyCallback {

    private val FINE_PERMISSION_CODE = 1
    private lateinit var mGoogleMap: GoogleMap
    private lateinit var currentLocation: Location
    private lateinit var fusedLocationProviderClient: FusedLocationProviderClient
    private lateinit var mapSearchView: SearchView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        fusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(this)
        mapSearchView = findViewById(R.id.mapSearch)
        mapSearchView.setOnQueryTextListener(object : SearchView.OnQueryTextListener {
            override fun onQueryTextSubmit(query: String): Boolean {
                val location = mapSearchView.query.toString()
                var addressList: List<Address>? = null
                if (location.isNotBlank()) {
                    val geocoder = Geocoder(this@MainActivity)
                    try {
                        addressList = geocoder.getFromLocationName(location, 1)
                    } catch (e: IOException) {
                        e.printStackTrace()
                    }
                    val address: Address? = addressList?.get(0)
                    val latLng: LatLng? = address?.let {
                        LatLng(it.latitude, it.longitude)
                    }
                    val options = MarkerOptions().position(latLng!!).title(location)
                    options.icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_GREEN))
                    mGoogleMap.addMarker(options)
                    mGoogleMap.animateCamera(CameraUpdateFactory.newLatLngZoom(latLng, 10f))
                    val currentLatLng = LatLng(currentLocation.latitude, currentLocation.longitude)
                    getDirection(currentLatLng, latLng)
                }
                return false
            }

            override fun onQueryTextChange(newText: String): Boolean {
                // Gérer l'événement de changement de texte de recherche ici
                return false
            }
        })

        // Activer la reconnaissance vocale lorsque la carte est chargée
        activateSpeechRecognition()

        getLastLocation()
    }

    private fun getLastLocation() {
        if (ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_COARSE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.ACCESS_FINE_LOCATION),
                FINE_PERMISSION_CODE
            )
            return
        }

        val task: Task<Location> = fusedLocationProviderClient.lastLocation
        task.addOnSuccessListener { location ->
            if (location != null) {
                currentLocation = location
                val mapFragment = supportFragmentManager.findFragmentById(R.id.mapFragment) as SupportMapFragment
                mapFragment.getMapAsync(this)
            }
        }
    }

    override fun onMapReady(googleMap: GoogleMap) {
        mGoogleMap = googleMap
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == FINE_PERMISSION_CODE) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                getLastLocation()
            } else {
                Toast.makeText(this, "Location permission denied", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun activateSpeechRecognition() {
        val speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this)
        val recognizerIntent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        recognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)

        speechRecognizer.setRecognitionListener(object : RecognitionListener {
            override fun onReadyForSpeech(params: Bundle?) {}

            override fun onBeginningOfSpeech() {}

            override fun onRmsChanged(rmsdB: Float) {}

            override fun onBufferReceived(buffer: ByteArray?) {}

            override fun onEndOfSpeech() {}

            override fun onError(error: Int) {}

            override fun onResults(results: Bundle?) {
                val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                if (!matches.isNullOrEmpty()) {
                    val spokenText = matches[0]
                    mapSearchView.setQuery(spokenText, true)
                }
            }

            override fun onPartialResults(partialResults: Bundle?) {}

            override fun onEvent(eventType: Int, params: Bundle?) {}
        })

        try {
            speechRecognizer.startListening(recognizerIntent)
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(this, "Speech recognition failed", Toast.LENGTH_SHORT).show()
        }
    }

    private fun getDirection(from: LatLng, to: LatLng) {
        try {
            Toast.makeText(this, "Im Here!!!", Toast.LENGTH_SHORT).show()
            val uri = Uri.parse("https://www.google.com/maps/dir/?api=1&origin=${from.latitude},${from.longitude}&destination=${to.latitude},${to.longitude}&travelmode=walking&dir_action=navigate")
            Toast.makeText(this, "Im Here TOOOOOOO!!!", Toast.LENGTH_SHORT).show()
            val intent = Intent(Intent.ACTION_VIEW, uri)
            intent.setPackage("com.google.android.apps.maps")
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            startActivity(intent)
        } catch (e: ActivityNotFoundException) {
            Toast.makeText(this, "There is a probleme HERE!!!", Toast.LENGTH_SHORT).show()
            val uri = Uri.parse("https://play.google.com/store/apps/details?id=com.google.android.apps.maps")
            val intent = Intent(Intent.ACTION_VIEW, uri)
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            startActivity(intent)
        }
    }
}