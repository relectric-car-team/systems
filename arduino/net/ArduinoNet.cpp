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

/* Sends the integer data to the connected computer. The idenfifier key must be an
	even integer k such that 0 < k <= 65536.

data - The integer value to be sent over the serial connection.
key - The integer key that identifies the meaning of the value. The key must be
	and even integer k such that 0 < k <= 65536.
 */
ArduinoNet::sendData(int data, int key) {
	if (id % 2 == 0) {
		byte * bKey = &key;
		byte * bData = &data;
		Serial.write(bKey, 2);
		Serial.write(bData, 2);
	} else {
		throw ArduinoNetError("Invalid data ID, must be even for integers.");
	}
}

/* Sends the float data to the connected computer. The idenfifier key must be an
	odd integer k such that 0 < k <= 65536.

data - The float value to be sent over the serial connection.
key - The integer key that identifies the meaning of the value. The key must be
	and odd integer k such that 0 < k <= 65536.
 */
ArduinoNet::sendData(float data, int key) {
	if (id % 2 == 1) {
		byte * bKey = &key;
		byte * bData = &data;
		Serial.write(bKey, 2);
		Serial.write(bData, 4);
	} else {
		throw ArduinoNetError("Invalid data ID, must be odd for floats.");
	}
}

/* Retrieves the most recently recieved data from the connected computer as an
	msg struct.
 */
ArduinoNet::getData() {
	if (Serial.available() == 2) {
		byte bKey[2];
		Serial.readbytes(bKey, 2);
		msg inPayload;
		inPayload.key = key;
		int key = (bKey[1] << 8) + bKey[0];
		if (key % 2 == 0) { // Int
			byte bData[2];
			Serial.readbytes(bData, 2);
			inPayload.data = (void *) &bData;
		} else { // Float
			byte bData[4];
			Serial.readbytes(bData, 4);
			inPayload.data = (void *) &bData;
		}
	}
}
