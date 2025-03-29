#include <Servo.h>

Servo myServo;            // Create a servo object

const int servoPin = 9;   // Connect the servo signal wire to digital pin 9
// led is on digital pin 12

void setup() {
  // Initialize the serial communication at 9600 baud.
  Serial.begin(115200);

  myServo.attach(servoPin); // Associate the servo with the pin

  // Set the LED pin as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(12, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
}

void loop() {
  // Check if a serial command is available.
  if (Serial.available() > 0) {
    // Read the incoming byte.
    char command = Serial.read();

    // Process the command.
    if (command == '1') {
      digitalWrite(12, HIGH);
      myServo.write(180);
      // Set LED to full brightness (255 out of 255).
      Serial.println("Setting servo to 180");
    } 
    else if (command == '0') {
      digitalWrite(12, LOW);
      myServo.write(0);
      // Set LED to a dim value (e.g., 50 out of 255).
      Serial.println("Setting servo to 0");
    } 
    else if (command == '2') {
      digitalWrite(LED_BUILTIN, LOW);
      // Print exit message and "halt" the program.
      Serial.println("Exiting program...");
      // Stop further processing with an infinite loop.
      while (true) {
        ; // Do nothing forever.
      }
    }
  }
}
