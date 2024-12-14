#include <TFT.h>   
#include <SPI.h> 
#include <Adafruit_AMG88xx.h> 
#include <Wire.h> 
#include <Servo.h> // Include the Servo library 
 
#define cs   10 
#define dc   9 
#define rst  8 
 
// Create an instance of the library 
TFT TFTscreen = TFT(cs, dc, rst); 
Adafruit_AMG88xx amg; 
 
// Create Servo objects 
Servo horizontalServo; // For horizontal rotation 
Servo verticalServo;   // For vertical tilt 
 
// Current angles of the servos 
int currentHorizontalAngle = 90; // Start at the middle (90 degrees) 
int currentVerticalAngle = 90;   // Start at the middle (90 degrees) 
 
// Function to convert RGB to 16-bit color 
uint16_t rgbTo565(uint8_t r, uint8_t g, uint8_t b) { 
    return (r >> 3) << 11 | (g >> 2) << 5 | (b >> 3); 
} 
 
// Function to map temperature to color 
uint16_t getColorFromTemperature(float temperature, float mid_temp) { 
    int k = 10; 
    if (temperature > mid_temp) { 
        return rgbTo565(100 + mid_temp * k, 255 - temperature * k, 25); 
    } else { 
        return rgbTo565(25, 25 + temperature * k, 255 - mid_temp * k); 
    } 
} 
 
void setup() { 
    // Initialize the Serial communication 
    Serial.begin(9600); 
 
    // Initialize the TFT screen 
    TFTscreen.begin(); 
    TFTscreen.background(0, 0, 0); // Clear the screen with a black background 
    TFTscreen.stroke(255, 255, 255); // Set text color to white 
    TFTscreen.setTextSize(2); // Set text size 
     
    // Initialize the AMG8833 sensor 
    if (!amg.begin()) { 
        Serial.println("AMG ERROR"); 
        TFTscreen.text("AMG ERROR", 12, 10); 
        while (1); // Stop execution if the sensor is not found 
    } else { 
        Serial.println("AMG OK"); 
        TFTscreen.text("AMG OK", 12, 10); 
    } 
 
    // Attach servos to pins 
    horizontalServo.attach(4); // Pin for horizontal servo 
    //verticalServo.attach(5);   // Pin for vertical servo 
 
    // Initialize servos to starting positions 
    horizontalServo.write(currentHorizontalAngle); 
    //verticalServo.write(currentVerticalAngle); 
} 
 
int rectSize = 10; // Size of each rectangle 
int startX = (128 - (8 * rectSize)) / 2; // Center the matrix horizontally 
int startY = (160 - (8 * rectSize)) / 2; // Center the matrix vertically 
 
void loop() { 
    float pixels[64]; 
    amg.readPixels(pixels); 
 
    // Определяем самый горячий пиксель 
    int hottestPixelIndex = 0; 
    float maxHeat = pixels[0]; 
    for (int i = 1; i < 64; i++) { 
        if (pixels[i] > maxHeat) { 
            maxHeat = pixels[i]; 
            hottestPixelIndex = i; 
        } 
    } 
 
    // Определяем строку и колонку горячего пикселя 
    int hottestRow = hottestPixelIndex / 8; // Ряд (0-7) 
    int hottestCol = hottestPixelIndex % 8; // Колонка (0-7) 
 
    // Преобразуем положение пикселя в углы для сервоприводов 
    int targetHorizontalAngle = map(hottestCol, 0, 7, 60, 120); // Угол для горизонтального серво 
    int targetVerticalAngle = map(hottestRow, 0, 7, 60, 120);   // Угол для вертикального серво 
 
    // Плавное движение серводвигателей 
    if (currentHorizontalAngle != targetHorizontalAngle) { 
        if (currentHorizontalAngle < targetHorizontalAngle) { 
            currentHorizontalAngle+=2; 
        } else { 
            currentHorizontalAngle-=2; 
        } 
        horizontalServo.write(currentHorizontalAngle); 
    } 
 
   // if (currentVerticalAngle != targetVerticalAngle) { 
   //    if (currentVerticalAngle  targetVerticalAngle) { 
   //         currentVerticalAngle+=2; 
   //     } else { 
   //         currentVerticalAngle-=2; 
   //     } 
   //     verticalServo.write(currentVerticalAngle); 
   // } 
 
    // Отображение тепловой карты 
    for (int i = 0; i < 8; i++) { 
        for (int j = 0; j < 8; j++) { 
            int index = i * 8 + j; 
            float temperature = pixels[index]; 
            uint16_t color = getColorFromTemperature(temperature, 19); 
            TFTscreen.fillRect(startX + j * rectSize, startY + i * rectSize, rectSize, rectSize, color); 
        } 
    } 
 
    delay(50); // Задержка для плавности 
}