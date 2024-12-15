#include <TFT.h>   
#include <SPI.h> 
#include <Adafruit_AMG88xx.h> 
#include <Wire.h> 
#include <Servo.h> // Подключаем библиотеку для управления сервоприводами
 
#define cs   10 
#define dc   9 
#define rst  8 
 
// Создаем объект для экрана TFT
TFT TFTscreen = TFT(cs, dc, rst); 
Adafruit_AMG88xx amg; // Создаем объект для тепловизора AMG8833
 
// Создаем объекты для управления сервоприводами
Servo horizontalServo; // Для горизонтального вращения
Servo verticalServo;   // Для вертикального наклона (не используется в этом коде)
 
// Текущие углы для сервоприводов
int currentHorizontalAngle = 90; // Начальный угол для горизонтального серво (по центру)
int currentVerticalAngle = 90;   // Начальный угол для вертикального серво (по центру)
 
// Функция для преобразования RGB в 16-битный цвет
uint16_t rgbTo565(uint8_t r, uint8_t g, uint8_t b) { 
    return (r >> 3) << 11 | (g >> 2) << 5 | (b >> 3); 
}

// Функция для отображения температуры в виде цвета
uint16_t getColorFromTemperature(float temperature, float mid_temp) { 
    int k = 10; 
    // Если температура больше средней, то используем красные оттенки
    if (temperature > mid_temp) { 
        return rgbTo565(100 + mid_temp * k, 255 - temperature * k, 25); 
    } else { 
        // Если температура ниже средней, то используем холодные оттенки
        return rgbTo565(25, 25 + temperature * k, 255 - mid_temp * k); 
    } 
}

void setup() { 
    // Инициализация последовательного соединения
    Serial.begin(9600); 
 
    // Инициализация экрана TFT
    TFTscreen.begin(); 
    TFTscreen.background(0, 0, 0); // Очищаем экран черным фоном
    TFTscreen.stroke(255, 255, 255); // Устанавливаем белый цвет текста
    TFTscreen.setTextSize(2); // Устанавливаем размер текста
    
    // Инициализация тепловизора AMG8833
    if (!amg.begin()) { 
        Serial.println("AMG ERROR"); 
        TFTscreen.text("AMG ERROR", 12, 10); 
        while (1); // Останавливаем выполнение, если датчик не найден
    } else { 
        Serial.println("AMG OK"); 
        TFTscreen.text("AMG OK", 12, 10); 
    }
 
    // Подключаем сервы к пинам
    horizontalServo.attach(4); // Пин для горизонтального серво
    // verticalServo.attach(5); // Пин для вертикального серво (не используется)

    // Устанавливаем начальные положения серво
    horizontalServo.write(currentHorizontalAngle); 
    // verticalServo.write(currentVerticalAngle); 
}

int rectSize = 10; // Размер каждого прямоугольника (пикселя на экране)
int startX = (128 - (8 * rectSize)) / 2; // Центрируем матрицу по горизонтали
int startY = (160 - (8 * rectSize)) / 2; // Центрируем матрицу по вертикали
 
void loop() { 
    float pixels[64]; // Массив для хранения данных с тепловизора
    amg.readPixels(pixels); // Считываем пиксели с датчика
 
    // Определяем самый горячий пиксель
    int hottestPixelIndex = 0; 
    float maxHeat = pixels[0]; 
    for (int i = 1; i < 64; i++) { 
        if (pixels[i] > maxHeat) { 
            maxHeat = pixels[i]; 
            hottestPixelIndex = i; 
        } 
    }

    // Определяем строку и колонку самого горячего пикселя
    int hottestRow = hottestPixelIndex / 8; // Ряд (0-7) 
    int hottestCol = hottestPixelIndex % 8; // Колонка (0-7) 

    // Преобразуем строку и колонку в углы для сервоприводов
    int targetHorizontalAngle = map(hottestCol, 0, 7, 60, 120); // Угол для горизонтального серво
    int targetVerticalAngle = map(hottestRow, 0, 7, 60, 120);   // Угол для вертикального серво

    // Плавное движение горизонтального серво
    if (currentHorizontalAngle != targetHorizontalAngle) { 
        if (currentHorizontalAngle < targetHorizontalAngle) { 
            currentHorizontalAngle += 2; // Увеличиваем угол для серво
        } else { 
            currentHorizontalAngle -= 2; // Уменьшаем угол для серво
        } 
        horizontalServo.write(currentHorizontalAngle); // Применяем новый угол
    }

    // Плавное движение вертикального серво (этот код не используется, так как вертикальный сервопривод закомментирован)
    // if (currentVerticalAngle != targetVerticalAngle) { 
    //     if (currentVerticalAngle < targetVerticalAngle) { 
    //         currentVerticalAngle += 2; 
    //     } else { 
    //         currentVerticalAngle -= 2; 
    //     } 
    //     verticalServo.write(currentVerticalAngle); 
    // }

    // Отображение тепловой карты на экране
    for (int i = 0; i < 8; i++) { 
        for (int j = 0; j < 8; j++) { 
            int index = i * 8 + j; 
            float temperature = pixels[index]; // Температура на этом пикселе
            uint16_t color = getColorFromTemperature(temperature, 19); // Получаем цвет для пикселя
            TFTscreen.fillRect(startX + j * rectSize, startY + i * rectSize, rectSize, rectSize, color); // Рисуем прямоугольник с цветом
        } 
    }
 
    delay(50); // Задержка для плавности отображения
}
