
struct structMsg {
	void* data;
	int key;
} msg;

class ArduinoNet {
private:
	void establishContact();
public:
	void ArduinoNet();
	void sendData(int data, int key);
	void sendData(float data, int key);
	msg getData();
};

