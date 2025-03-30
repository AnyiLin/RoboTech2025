#include <Servo.h>

Servo drive1;
Servo drive2;
Servo suspension1;
Servo suspension2;
Servo armRotate;
Servo armExtension;

const int drive1Pin = 0;
const int drive2Pin = 0;
const int suspension1Pin = 0;
const int suspension2Pin = 0;
const int armRotatePin = 0;
const int armExtensionPin = 0;
const int greenLedPin = 0;
const int redLedPin = 0;
int state = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  drive1.attach(drive1Pin);
  drive2.attach(drive2Pin);
  suspension1.attach(suspension1Pin);
  suspension2.attach(suspension2Pin);
  armRotate.attach(armRotatePin);
  armExtension.attach(armExtensionPin);

  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(greenLedPin, OUTPUT);
  pinMode(redLedPin, OUTPUT);

  digitalWrite(LED_BUILTIN, HIGH);
}

void loop() {
  // Check if a serial command is available.
  if (Serial.available() > 0) {
    char command = Serial.read();
    int oldState = state;
    switch (command) {
      case '0': // exit case
        drive1.detach();
        drive2.detach();
        suspension1.detach();
        suspension2.detach();
        armRotate.detach();
        armExtension.detach();
        digitalWrite(greenLedPin, LOW);
        digitalWrite(redLedPin, LOW);
        digitalWrite(LED_BUILTIN, LOW);
        Serial.println("Exiting program...");
        while (true) {
          ;
        }
      break;
      case '1': // test run drive motors forward
        state = 1;
        if (oldState != state && oldState != 2) {
          drive1.attach(drive1Pin);
          drive2.attach(drive2Pin);
          suspension1.detach();
          suspension2.detach();
          armRotate.detach();
          armExtension.detach();
        }
      break;
      case '2': // test run drive motors backward
        state = 2;
        if (oldState != state && oldState != 1) {
          drive1.attach(drive1Pin);
          drive2.attach(drive2Pin);
          suspension1.detach();
          suspension2.detach();
          armRotate.detach();
          armExtension.detach();
        }
      break;
      case '3': // test run suspension fully retracted
        state = 3;
        if (oldState != state && oldState != 4) {
          drive1.detach();
          drive2.detach();
          suspension1.attach(suspension1Pin);
          suspension2.attach(suspension2Pin);
          armRotate.detach();
          armExtension.detach();
        }
      break;
      case '4': // test run suspension fully extended
        state = 4;
        if (oldState != state && oldState != 3) {
          drive1.detach();
          drive2.detach();
          suspension1.attach(suspension1Pin);
          suspension2.attach(suspension2Pin);
          armRotate.detach();
          armExtension.detach();
        }
      break;
      case '5': // move arm left
        state = 5;
        if (oldState != state && oldState != 6 && oldState != 7) {
          drive1.detach();
          drive2.detach();
          suspension1.detach();
          suspension2.detach();
          armRotate.attach(armRotatePin);
          armExtension.attach(armExtensionPin);
        }
      break;
      case '6': // keep arm still (on target)
        state = 6;
        if (oldState != state && oldState != 5 && oldState != 7) {
          drive1.detach();
          drive2.detach();
          suspension1.detach();
          suspension2.detach();
          armRotate.attach(armRotatePin);
          armExtension.attach(armExtensionPin);
        }
      break;
      case '7': // move arm right
        state = 7;
        if (oldState != state && oldState != 5 && oldState != 6) {
          drive1.detach();
          drive2.detach();
          suspension1.detach();
          suspension2.detach();
          armRotate.attach(armRotatePin);
          armExtension.attach(armExtensionPin);
        }
      break;
      default:
      break;
    }
  }

  switch (state) {
    case 1:
    break;
    case 2:
    break;
    case 3:
    break;
    case 4:
    break;
    case 5:
    break;
    case 6:
    break;
    case 7:
    break;
    default:
    break;
  }
}
