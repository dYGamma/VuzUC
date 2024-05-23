package com.example.lab5

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.compose.LocalOnBackPressedDispatcherOwner
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.lab5.ui.theme.Lab5Theme

class MainActivity4 : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            Lab5Theme {
                // A surface container using the 'background' color from the theme
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = Color.White // Установка белого цвета фона
                ) {
                    GreetingWithButton("Дмитрий")
                }
            }
        }
    }
}

@Composable
fun GreetingWithButton(name: String) {
    var showNews by remember { mutableStateOf(false) }
    val backDispatcher = LocalOnBackPressedDispatcherOwner.current?.onBackPressedDispatcher

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.Top
    ) {
        if (showNews) {
            NewsList()
        } else {
            Text(
                text = "Привет $name!",
                modifier = Modifier.padding(bottom = 8.dp)
            )
            OutlinedButton(onClick = { showNews = true }) { // Замена на квадратную кнопку
                Text(text = "Посмотреть новости")
            }
        }
        Spacer(modifier = Modifier.height(16.dp))
        TextButton(onClick = { backDispatcher?.onBackPressed() }) { // Замена на квадратную кнопку
            Text(text = "Назад")
        }
    }
}

@Composable
fun NewsList() {
    val newsItems = listOf(
        "Новость 1: Новые технологические инновации",
        "Новость 2: Обновления на глобальных рынках",
        "Новость 3: Основные спортивные события",
        "Новость 4: Советы по здоровью и благополучию",
        "Новость 5: Новости мира развлечений",
        "Новость 6: Политические события и решения",
        "Новость 7: Научные прорывы и открытия",
        "Новость 8: Популярные туристические направления",
        "Новость 9: Советы по финансам и инвестициям",
        "Новость 10: Тенденции в образовании и обучении"
    )

    LazyColumn {
        items(newsItems) { newsItem ->
            Text(text = newsItem, modifier = Modifier.padding(8.dp))
        }
    }
}

@Preview(showBackground = true)
@Composable
fun GreetingWithButtonPreview() {
    Lab5Theme {
        GreetingWithButton("Дмитрий")
    }
}
