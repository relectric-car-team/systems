// Includes
#include "ArduinoNet.h"
#include <stdlib.h>
#include "ArduinoNetError.h"

// Constants
#define USB_BAUD 19200
#define USB_TIMEOUT = 0.1 

/* Attempts to verify contact with the remote computer, waiting for a response
	to a periodic byte sent over the connection.

 */
ArduinoNet::establishContact() {
	while (Serial.read() != '$') {
		Serial.write('$')
		delay(100)
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

/*

 */
ArduinoNet::sendData(int data, int key) {
	if (id % 2 == 0) {
		byte * bKey = &key;
		byte * bData = &data;
		Serial.write(bKey[0]);
		Serial.write(bKey[1]);
		Serial.write(bData[0]);
		Serial.write(bData[1]);
	} else {
		throw ArduinoNetError("Invalid data ID, must be even for integers.");
	}
}

/*

 */
ArduinoNet::sendData(float data, int key) {
	if (id % 2 == 1) {
		byte * bKey = &key;
		byte * bData = &data;
		Serial.write(bKey[0]);
		Serial.write(bKey[1]);
		for (const byte b : bData) {
			Serial.write(b);
		}
	} else {
		throw ArduinoNetError("Invalid data ID, must be odd for floats.");
	}
}

/*

 */
ArduinoNet::getData() {
	
}
