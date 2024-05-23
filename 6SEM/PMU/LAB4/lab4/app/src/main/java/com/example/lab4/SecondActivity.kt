package com.example.lab4
import androidx.compose.material3.Button

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.wrapContentSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.sp
import com.example.lab4.ui.theme.Lab4Theme

class SecondActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val text = intent.getStringExtra("userInput") ?: ""
        setContent {
            Lab4Theme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    Greeting(text)
                    BackButton()
                }
            }
        }
    }

    @Composable
    fun Greeting(name: String, modifier: Modifier = Modifier) {
        Text(
            text = "Привет $name!",
            fontSize = 34.sp,
            modifier = modifier.fillMaxSize()

        )
    }
    @Composable
    fun BackButton() {
        Button(
            onClick = { finish() },
            modifier = Modifier.wrapContentSize()
        ) {
            Text("Back")
        }
    }

    @Preview(showBackground = true)
    @Composable
    fun GreetingPreview() {
        Lab4Theme {
            Greeting("Second Screen")
        }
    }
}
