// Pi to Arduino Serial Communication Test
#include <AFMotor.h>
#include "config.h"

int count=0;
  char first_var;
  char last_var;

void setup() {
// initialize both serial ports:
	Serial.begin(9600);
	Serial3.begin(9600);
}
void loop() {
    char command[10];  // Change this size as needed
    int index = 0;

    // Check if there are any characters available to read
    while (Serial3.available() > 0 && index < sizeof(command) - 1) {
        char ch = Serial3.read();

        // If this character is a newline or carriage return, this is the end of the command
        if (ch == '\n' || ch == '\r') {
            break;
        }

        // Otherwise, add this character to the command
        command[index++] = ch;
    }

    // Null-terminate the command string
    command[index] = '\0';

    // If a command was read, handle it
    if (index > 0) {
        control(command);
    }
}