#include <Servo.h>

// For CR servos, 0 is clockwise and 180 is counterclockwise, 90 is middle
Servo drive1;
Servo drive2;
Servo suspension1;
Servo suspension2;
Servo armRotate;
Servo armExtension;

const int drive1Pin = 9;
const int drive1Forward = 0;
const int drive1Backward = 180;
const int drive2Pin = 3;
const int drive2Forward = 0;
const int drive2Backward = 180;
const int suspension1Pin = 11;
const int suspension1Extend = 90;
const int suspension1Retract = 180;
const int suspension2Pin = 10;
const int suspension2Extend = 80;
const int suspension2Retract = 170;
const int armRotatePin = 6;
const int armRotateLeft = 82;
const int armRotateNone = 90;
const int armRotateRight = 104;
const int armExtensionPin = 5;
const int armRetracted = 180;
const int armExtended = 0;
const int greenLedPin = 8;
const int redLedPin = 12;
int state = 1;

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

  // servo commands
  switch (state) {
    case 1:
      drive1.write(drive1Forward);
      drive2.write(drive2Forward);
    break;
    case 2:
      drive1.write(drive1Backward);
      drive2.write(drive2Backward);
    break;
    case 3:
      suspension1.write(suspension1Retract);
      suspension2.write(suspension2Retract);
    break;
    case 4:
      suspension1.write(suspension1Extend);
      suspension2.write(suspension2Extend);
    break;
    case 5:
      armRotate.write(armRotateLeft);
      armExtension.write(armRetracted);
    break;
    case 6:
      armRotate.write(armRotateNone);
      armExtension.write(armExtended);
    break;
    case 7:
      armRotate.write(armRotateRight);
      armExtension.write(armRetracted);
    break;
    default:
    break;
  }

  // light control
  unsigned long seconds = millis() / 1000; 
  if (seconds % 2 == 0 && state != 6) {
    digitalWrite(greenLedPin, HIGH);
  } else {
    digitalWrite(greenLedPin, LOW);
  }
  if (state == 6) {
    digitalWrite(redLedPin, HIGH);
  } else {
    digitalWrite(redLedPin, LOW);
  }
}
