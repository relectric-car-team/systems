import can

class CANBusNet:
    """ The CANBus interface class allows for communication to occur between
    the CANBus and systems project. """

    def __init__(self):
        """ Creates and initializes an instance of the bus object.

        interface - The name of the interface that the bus is using.
        channel - The default channel used.
        bitrate - The bitrate in bits/s to use by default.
        """

        self.bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=50000)

    def send_message(self, a_id, is_extended, dataset):
        """ Creates and sends a CAN message to the CANBus.

        a_id - A frame identifier used by the CANBus for arbitration.
        is_extended - Controls the size of the arbitration_id.
        dataset - This parameter may consist of bytes or a list of integers to be sent.
        """

        message = can.Message(arbitration_id=a_id, is_extended_id=is_extended, data=dataset)
        try:
            self.bus.send(message)
            print("Message sent on {}".format(self.bus.channel_info))
        except can.CanError:
            print("Message not sent")

    def receive_message(self):
        """ Accepts and returns a message that is sent from the CANBus. """

        message = self.bus.recv()
        print(message)
        return message

    def stop(self):
        """ Shuts the bus down and carries out interface clean up. """

        self.bus.shutdown()
