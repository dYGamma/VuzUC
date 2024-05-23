package com.example.lab3calc
import android.widget.TextView
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.lab3calc.ui.theme.LAB3calcTheme
import net.objecthunter.exp4j.ExpressionBuilder


class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        findViewById<TextView>(R.id.btn_0).setOnClickListener{setTextFields("0")}
        findViewById<TextView>(R.id.btn_AC).setOnClickListener {
            findViewById<TextView>(R.id.math_operation).text = ""
            findViewById<TextView>(R.id.math_operation).text = ""
        }
        findViewById<TextView>(R.id.btn_right).setOnClickListener { setTextFields("(") }
        findViewById<TextView>(R.id.btn_left).setOnClickListener { setTextFields(")") }
        findViewById<TextView>(R.id.btn_palka).setOnClickListener { setTextFields("/") }
        findViewById<TextView>(R.id.btn_7).setOnClickListener { setTextFields("7") }
        findViewById<TextView>(R.id.btn_8).setOnClickListener { setTextFields("8") }
        findViewById<TextView>(R.id.btn_9).setOnClickListener { setTextFields("9") }
        findViewById<TextView>(R.id.btn_zvezda).setOnClickListener { setTextFields("*") }
        findViewById<TextView>(R.id.btn_4).setOnClickListener { setTextFields("4") }
        findViewById<TextView>(R.id.btn_5).setOnClickListener { setTextFields("5") }
        findViewById<TextView>(R.id.btn_6).setOnClickListener { setTextFields("6") }
        findViewById<TextView>(R.id.btn_plus).setOnClickListener { setTextFields("+") }
        findViewById<TextView>(R.id.btn_1).setOnClickListener { setTextFields("1") }
        findViewById<TextView>(R.id.btn_2).setOnClickListener { setTextFields("2") }
        findViewById<TextView>(R.id.btn_3).setOnClickListener { setTextFields("3") }
        findViewById<TextView>(R.id.btn_minus).setOnClickListener { setTextFields("-") }
        findViewById<TextView>(R.id.btn_t).setOnClickListener { setTextFields(".") }
        findViewById<TextView>(R.id.btn_C).setOnClickListener {
            val str = findViewById<TextView>(R.id.math_operation).text.toString()
            if (str.isNotEmpty()) {
                findViewById<TextView>(R.id.math_operation).text = str.substring(0, str.length - 1)

            }
        }
        findViewById<TextView>(R.id.btn_ravno).setOnClickListener {
            val str = findViewById<TextView>(R.id.math_operation).text.toString()
            try {
                val result = ExpressionBuilder(str).build().evaluate()
                findViewById<TextView>(R.id.math_operation).text = result.toString()
            } catch (e: Exception) {
                findViewById<TextView>(R.id.math_operation).text = "Ошибка"
            }
        }

    }
    fun setTextFields(str: String) {
        findViewById<TextView>(R.id.math_operation).append(str)
    }
}

