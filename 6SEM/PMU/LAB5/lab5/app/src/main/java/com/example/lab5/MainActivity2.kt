package com.example.lab5
import com.example.lab5.FlashlightHelper
import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.ToggleButton
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.lab5.ui.theme.Lab5Theme


class MainActivity2 : ComponentActivity() {

    private lateinit var flashlightHelper: FlashlightHelper

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main2)

        findViewById<Button>(R.id.buttonBack).setOnClickListener {
            finish()
        }

        findViewById<ToggleButton>(R.id.button4).setOnClickListener {
            if ((it as ToggleButton).isChecked) {
                flashlightHelper.turnOn()
            } else {
                flashlightHelper.turnOff()
            }
        }

        flashlightHelper = FlashlightHelper(this)
    }

    override fun onDestroy() {
        super.onDestroy()

        flashlightHelper.turnOff()
    }
}
