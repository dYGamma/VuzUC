package com.example.lab3

import android.graphics.drawable.AnimatedImageDrawable
import android.os.Bundle
import android.widget.Button
import android.widget.ImageView
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import com.example.lab3.ui.theme.LAB3Theme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            LAB3Theme {
                // A surface container using the 'background' color from the theme
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    setContentView(R.layout.activity_main)

                    val button3 = findViewById<Button>(R.id.button3)
                    val imageView4 = findViewById<ImageView>(R.id.imageView4)
                    val buttonExit = findViewById<Button>(R.id.button_exit)
                    button3.setOnClickListener {
                        val drawable = imageView4.drawable
                        if (drawable is AnimatedImageDrawable) {
                            drawable.start()
                        }
                    }
                    buttonExit.setOnClickListener {
                        finish()
                    }
                }
            }
        }
    }
}
