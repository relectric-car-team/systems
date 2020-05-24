import logging as log
from controller import *
from controllers import *
from networkmanager import NetworkManager


class Systems:
    """ The Systems class is the main object that encapsulates the program for
    the electric car central systems. It consists of a set of 'controller'
    modules that each contribute separate functions to control and manage
    different sub-systems in the car (battery, motor, climate control,
    etc). In addition, this class owns an instance of NetworkManager,
    an object containing instances of all the necessary abstracted networking
    interfaces needed to communicate with the aforementioned sub-systems.
    The NetworkManager is passed to each controller upon initialization.
    """

    def __init__(self):
        """ Creates and initializes the network manager and all of the
        controllers.
        """
        self.__controllers = []
        self.__networkManager = NetworkManager([])
        self.__controllers.append(MotorController(self.__networkManager))
        self.__controllers.append(BatteryController(self.__networkManager))
        self.__controllers.append(ClimateController(self.__networkManager))
        self.__controllers.append(SensorController(self.__networkManager))
        self.__controllers.append(BackupController(self.__networkManager))
        self.__loop()  # Note there is currently no end condition.

    def __get_data(self, name: str) -> any:
        """ Finds and returns the value of the specified variable that belongs
        to one	of the controllers.

        name - A string to identify the variable.
        """
        for controller in self.__controllers:
            try:
                return controller.get_variable(name, False)
            except:
                return None

    def __set_data(self, name: str, value: any) -> None:
        """ Finds and sets the value of the specified variable that belongs
        to one of the controllers.

        name - A string to identify the variable.
        value - New value for the specified variable.
        """
        for controller in self.__controllers:
            try:
                controller.set_variable(name, value)
            except:
                pass

    def __send_action(self, name: str, args: Tuple[any]) -> None:
        """ Calls the action specified by a controller with the provided
        arguments.

        name - A string to identify the action.
        args - Tuple of arguments to pass to the function.
        """
        for controller in self.__controllers:
            try:
                controller.perform_action(name, args)
            except:
                pass

    def __loop(self):
        """ The main program loop for the systems computer. Listens for external
         requests and services them accordingly with the actions of controllers.
        The	format of requests directed to the actions of controllers is a
        dictionary with the format {"type": ["action"|"get"|"set"],
        "name": ["name"], ["args": []], ["value": any]}.
        """
        while True:
            request = self.__networkManager.get_pinet().get_request()
            if request is not None:
                response = None
                if request["type"] == "action":
                    response = self.__send_action(request["name"],
                                                 tuple(request["args"]))
                elif request["type"] == "get":
                    response = self.__get_data(request["name"])
                elif request["type"] == "set":
                    try:
                        self.__set_data(request["name"], request["value"])
                        response = True
                    except:
                        response = False
                self.__networkManager.get_pinet().send_response(
                    request["requestKey"],
                    response, request["peer"])

    def shutdown(self) -> None:
        """ Shuts the controllers down. """
        for controller in self.__controllers:
            controller.shutdown()


# Main module entry point.
if __name__ == "__main__":
    log.basicConfig()
    systems = Systems()
