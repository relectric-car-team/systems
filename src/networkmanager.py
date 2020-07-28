from typing import List, Tuple
import logging as log
from net import PiNet, ArduinoNet, CANBusNet


class NetworkManager:
    """ NetworkManager takes ownership of all networking library objects so
    that instances of controller classes may use them. Passing this class
    down to the controller classes ensures they do not use duplicates of
    these networking interfaces.
    """

    def __init__(self, address: Tuple[str, int],
                 serial_ports: List[str]) -> None:
        """ Initializes NetworkManager and creates and starts all of the network
        interfaces.

        address - A tuple containing a string with the address for the PiNet
            instance to listen to followed by the port. (address: str, port: int)
        serial_ports - A list containing the platform identifiers (strings) for
            the	serial ports to be bound. The index of the identifier is the
            same as the integer used to retrieve a the respective ArduinoNet
            instance with getArduinoNet(). Example identifiers include 'COM3'
            for Windows and '/dev/ttyUSB0' for GNU/Linux.
        """
        log.info("Starting network interfaces...")
        self.__pinet = PiNet(True, address)
        # Assuming we use this port
        self.__arduino_nets = []
        for port in serial_ports:
            self.__arduino_nets.append(ArduinoNet(port))
        self.__canbusnet = CANBusNet()

    def get_pinet(self) -> PiNet:
        """ Returns the active PiNet instance. """
        return self.__pinet

    def get_arduino_net(self, port: int) -> ArduinoNet:
        """ Returns the active ArduinoNet instance.
        port - An integer specifying the serial port tied to the ArduinoNet
            instance being requested. See __init__().
        """
        return self.__arduino_nets[port]

    def get_canbusnet(self) -> CANBusNet:
        """ Returns the active CANBusNet instance. """
        return self.__canbusnet

    def stop(self) -> None:
        """ Safely closes all network interfaces. """
        log.info("Closing network interfaces...")
        self.__pinet.stop()
        for port in self.__arduino_nets:
            port.stop()
