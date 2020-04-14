// Includes
#include <hardwareSerial.h>
#include "ArduinoNet.h"
#include <stdlib.h>
#include <Arduino.h>

// Constants
#define USB_BAUD 19200
#define USB_TIMEOUT = 0.1 

/* Attempts to verify contact with the remote computer, waiting for a response
	to a periodic byte sent over the connection.
 */
void ArduinoNet::establishContact() {
	while (Serial.read() != '$') {
		Serial.write('$');
		delay(100);
	}
}

/* Creates a new instance of the ArduinoNet class. It takes no parameters and
	will block until a connection is achieved.
 */
ArduinoNet::ArduinoNet() {
	Serial.begin(USB_BAUD);
	while (!Serial) {
		// Wait for the serial interface to connect
	}
	ArduinoNet::establishContact();
}

/* Sends the integer data to the connected computer. The idenfifier key must be an
	even integer k such that 0 < k <= 65536.

data - The integer value to be sent over the serial connection.
key - The integer key that identifies the meaning of the value. The key must be
	and even integer k such that 0 < k <= 65536.
 */
void ArduinoNet::sendData(int data, int key) {
	byte * bKey = (byte*) &key;
	byte * bData = (byte*) &data;
	Serial.write(bKey, 2);
	Serial.write(bData, 2);
}

/* Sends the float data to the connected computer. The idenfifier key must be an
	odd integer k such that 0 < k <= 65536.

data - The float value to be sent over the serial connection.
key - The integer key that identifies the meaning of the value. The key must be
	and odd integer k such that 0 < k <= 65536.
 */
void ArduinoNet::sendData(float data, int key) {
	byte * bKey = (byte*) &key;
	byte * bData = (byte*) &data;
	Serial.write(bKey, 2);
	Serial.write(bData, 4);
}

/* Retrieves the most recently recieved data from the connected computer as an
	msg struct. If no such message exists, retruns and msg where key == 0.
 */
msg ArduinoNet::getData() {
  msg inPayload;
  inPayload.key = 0;
  inPayload.iData = 0;
  inPayload.fData = 0.0;
	if (Serial.available() == 2) {
		byte bKey[2];
		Serial.readBytes(bKey, 2);
		inPayload.key = (bKey[1] << 8) + bKey[0];
		if (inPayload.key % 2 == 0) { // Int
			byte bData[2];
			Serial.readBytes(bData, 2);
			inPayload.iData = (int) *bData;
		} else { // Float
			byte bData[4];
			Serial.readBytes(bData, 4);
			inPayload.fData = (float) *bData;
		}
	}
 return inPayload;
}
