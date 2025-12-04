// Include Libraries
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>
#include <DHT.h>

// Initialize the LCD (I2C address 0x27, 16 columns, 2 rows)
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Define pins for DHT22
#define DHTPIN 2       // Pin for DHT22 sensor
#define DHTTYPE DHT22  // Define DHT as DHT22

DHT dht(DHTPIN, DHTTYPE);  // Initialize DHT22 sensor

// Define pins for Ultrasonic Sensor
int trigPin = 9;
int echoPin = 8;

// Define Servo Motor
Servo servo;

// Define Buzzer Pin
int buzzerPin = 10; // Pin for the buzzer

// Variables for ultrasonic sensor and temperature
long duration;
int distance;
float temperature;

void setup() 
{
  // Initialize the LCD
  lcd.begin(16, 2);    // Initialize the LCD with 16 columns and 2 rows
  lcd.backlight();     // Turn on the LCD backlight

  // Initialize the servo motor
  servo.attach(7);
  servo.write(0);  // Close the gate initially
  delay(2000);

  // Set trigPin as OUTPUT and echoPin as INPUT
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Set buzzerPin as OUTPUT
  pinMode(buzzerPin, OUTPUT);
  
  // Initialize Serial Communication
  Serial.begin(9600);
  
  // Initialize DHT22 sensor
  dht.begin();
  
  // Add a delay to allow the DHT sensor to stabilize
  delay(2000);  // Wait for 2 seconds
}

void loop() 
{
  // Measure temperature from DHT22
  temperature = dht.readTemperature(); // Read temperature in Celsius

  // Handle the case where temperature reading is NaN
  if (isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  
  // Display the temperature on the LCD
  lcd.setCursor(0, 0);  // Set cursor to first row
  lcd.print("Temp: ");
  lcd.print(temperature);
  lcd.print(" C  ");  // Print temperature

  // Clear the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  // Trigger ultrasonic pulse for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Read echoPin and calculate distance in cm
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  // Print temperature and distance on Serial Monitor
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" *C");
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  // First check for temperature adequacy
  if (temperature < 40) { // If temperature is adequate
    // Now check for distance adequacy
    if (distance < 25) { // If distance is also adequate
      servo.write(90);  // Open the gate
      Serial.println("Gate is open. You may pass!");
      lcd.setCursor(0, 1);  // Set cursor to second row
      lcd.print("Gate open");
      noTone(buzzerPin);  // Turn off the buzzer
    } 
    else { // If distance is inadequate
      servo.write(0);   // Keep gate closed
      Serial.println("Gate is closed due to insufficient distance.");
      lcd.setCursor(0, 1);  // Set cursor to second row
      lcd.print("Gate Closed");
      
    }
  } 
  else { // If temperature is inadequate
    servo.write(0);   // Keep gate closed
    Serial.println("Gate is closed due to high temperature.");
    lcd.setCursor(0, 1);  // Set cursor to second row
    lcd.print("Gate closed");
    tone(buzzerPin, 1000); // Turn on buzzer at 1000 Hz
  }

  delay(2000);  // Wait for 2 seconds before the next reading
}
