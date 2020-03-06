#include "ArduinoNet.h"
#include <stdlib.h>

/*

 */
ArduinoNet::establishContact() {
	while (Serial.available() <= 0) {
		Serial.print('$');
		delay(100);
	}
	Serial.read();
}

/*

 */
ArduinoNet::init() {
	Serial.begin(19200);
	while (!Serial) {
		// Wait for the serial interface to connect
	}
	ArduinoNet::establishContact();
}
