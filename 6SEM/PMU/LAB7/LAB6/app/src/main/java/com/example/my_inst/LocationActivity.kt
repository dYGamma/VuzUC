package com.example.my_inst

import android.Manifest
import android.annotation.SuppressLint
import android.content.Context.LOCATION_SERVICE
import android.content.Intent
import android.location.LocationManager
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.Toast

import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat.getSystemService
import androidx.core.location.LocationManagerCompat.isLocationEnabled
import com.example.my_inst.databinding.ActivityLocationBinding

import com.example.my_inst.databinding.ActivityMainBinding
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.LocationServices
import com.google.android.gms.location.Priority
import com.google.android.gms.location.LocationSettingsRequest
import com.google.android.gms.location.LocationRequest

import com.google.android.gms.common.api.ResolvableApiException
import com.google.android.gms.tasks.CancellationTokenSource




class LocationActivity : AppCompatActivity() {
    private lateinit var binding: ActivityLocationBinding
    private lateinit var fusedLocationClient: FusedLocationProviderClient

    @SuppressLint("MissingPermission", "MissingInflatedId")
    override fun onCreate(savedInstanceState: Bundle?)
    {


        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_location)

        fun goToFlashlightActivity(view: View) {
            val intent = Intent(this, MainActivity::class.java)
            startActivity(intent)
        }


        binding = ActivityLocationBinding.inflate(layoutInflater)
        val view = binding.root
        setContentView(view)

        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)


        val locationPermissionRequest= registerForActivityResult(
            ActivityResultContracts.RequestMultiplePermissions()
        ) { permissions ->
            when {
                permissions.getOrDefault(
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    false
                ) || permissions.getOrDefault(
                    Manifest.permission
                        .ACCESS_COARSE_LOCATION, false
                ) -> {
                    Toast.makeText(
                        this, "loca access granted", Toast
                            .LENGTH_SHORT
                    ).show()

                    if (isLocationEnabled()) {
                        val result = fusedLocationClient.getCurrentLocation(
                            Priority.PRIORITY_BALANCED_POWER_ACCURACY,
                            CancellationTokenSource().token
                        )
                        result.addOnCompleteListener {
                            val location =
                                "Latitude: " + it.result.latitude + "\n" + "Longitude: " +
                                        it.result.longitude

                            binding.textView.text = location
                        }
                    } else {
                        Toast.makeText(
                            this, "Please turn on locatyion.",
                            Toast.LENGTH_SHORT
                        )
                            .show()
                        createLocationRequest()
                    }


                }

                else -> {
                    Toast.makeText(
                        this, "no loc access", Toast
                            .LENGTH_SHORT
                    ).show()

                }
            }
        }


        binding.btnGetLocation.setOnClickListener {
            locationPermissionRequest.launch(
                arrayOf(
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION
                )
            )
        }
    }








    private fun isLocationEnabled(): Boolean
    {
        val locationManager = getSystemService(LOCATION_SERVICE) as LocationManager

        try
        {
            return locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER)

        } catch (e: Exception)
        {
            e.printStackTrace()
        }
        return false
    }


    private fun createLocationRequest()
    {
        val locationRequest = LocationRequest.Builder(
            Priority.PRIORITY_HIGH_ACCURACY,
            10000
        ).setMinUpdateIntervalMillis(5000).build()

        val builder = LocationSettingsRequest.Builder().addLocationRequest(locationRequest)

        val client = LocationServices.getSettingsClient(this)

        val task = client.checkLocationSettings(builder.build())

        task.addOnCanceledListener {

        }

        task.addOnFailureListener{ e ->
            if(e is ResolvableApiException){
                try {
                    e.startResolutionForResult(
                        this,
                        100
                    )
                }catch (sendEx: java.lang.Exception){
                }
            }
        }

    }
}

