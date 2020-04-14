/* Wrapper to contain the data returned by ArduinoNet.getData().
 */
struct structMsg {
	void* data;
	int key;
} msg;

/* Serial communication library object, see ArduinoNet.cpp.
 */
class ArduinoNet {
private:
	void establishContact();
public:
	ArduinoNet();
	void sendData(int data, int key);
	void sendData(float data, int key);
	msg getData();
};

