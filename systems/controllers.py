from __future__ import annotations

from typing import Literal, TypedDict

import attr


class ControllerDecorator:
    """Utility decorator for attr.attrs and dict-like properties.

    Allows us to do things like::

        @Controller
        class DummyController:
            variable: int = 0

        dummy = DummyController()
        dummy['variable'] = 4
        variable = dummy['variable]
    ::
    """

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __call__(self, class_):
        class_.__getitem__ = ControllerDecorator.__getitem__
        class_.__setitem__ = ControllerDecorator.__setitem__
        class_ = attr.attrs(class_, slots=True, auto_attribs=True, eq=False)
        return class_


Controller = ControllerDecorator()


@Controller
class BackupController:
    """Controller class for backup sensors.

    Attributes:
        speed (int): Defaults to 0.
        distance (int): Defaults to 0.
    """
    speed: int = 0
    distance: int = 0


@Controller
class BatteryController:
    """Controller class for battery sensors.

    Attributes:
        percentage (int): Defaults to 0.
        voltage (int): Defaults to 0.
        distance (int): Defaults to 0.
    """
    percentage: int = 0
    voltage: int = 0
    temperature: int = 0


@Controller
class ClimateController:
    """Controller class for climate sensors.

    Attributes:
        outsideTemperature (int): Defaults to 0.
        insideTemperature (int): Defaults to 0.
        fanPower (int): Defaults to 0.
        temperatureSetting (int): Defaults to 0.
    """
    outsideTemperature: int = 0
    insideTemperature: int = 0
    fanPower: int = 0
    temperatureSetting: int = 0


@Controller
class MotorController:
    """Controller class for motor sensors.

    Attributes:
        speed (int): Defaults to 0.
        voltage (int): Defaults to 0.
        temperature (int): Defaults to 0.
        rpm (int): Defaults to 0.
    """
    speed: int = 0
    voltage: int = 0
    temperature: int = 0
    rpm: int = 0


@Controller
class SensorController:
    """Controller class for distance sensors.

    Attributes:
        distanceFront (int): Defaults to 0.
        distanceBack (int): Defaults to 0.
    """
    distanceFront: int = 0
    distanceBack: int = 0


controllers = {
    "BackupController": BackupController(),
    "BatteryController": BatteryController(),
    "ClimateController": ClimateController(),
    "MotorController": MotorController(),
    "SensorController": SensorController()
}


class Message(TypedDict):
    controller: Literal["BackupController", "BatteryController",
                        "ClimateController", "MotorController",
                        "SensorController"]
    data: dict
    sender: list[bytes] | None
    # str before parsed to JSON
    destinations: list[list[bytes]] | list[list[str]]
