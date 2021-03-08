import attr


def _type_validator(instance: object, variable: str, new_value: any):
    """Type validation for @attr.s - on_setattr().

    Args:
        instance (object): Instace attribute is being set on
        variable (str): Instance variable
        new_value (any): New value of instance variable to be set

    Raises:
        TypeError: Thrown if type mismatch

    Returns:
        new_value: Value to be set
    """
    current_variable_type = variable.type
    new_value_type = type(new_value)
    if current_variable_type != new_value_type:
        raise TypeError(f"Trying to set type {new_value_type} on attribute of type {current_variable_type}")
    return new_value

class Subscriptable:
    """Utility base class for name-based getting/setting, and todict conversion.
    """
    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def asdict(self):
        return attr.asdict(self)

controller = lambda cls: attr.s(cls, slots=True, auto_attribs=True, eq=False, on_setattr=_type_validator)

@controller
class BackupController(Subscriptable):
    speed: int = 0
    distance: int = 0

@controller
class BatteryController(Subscriptable):
    voltage: int = 0
    temperature: int = 0

@controller
class ClimateController(Subscriptable):
    weathertemperature: int = 0
    fanpower: int = 0

@controller
class MotorController(Subscriptable):
    speed: int = 0
    voltage: int = 0
    temperature: int = 0
    rpm: int = 0

@controller
class SensorController(Subscriptable):
    distancefront: int = 0
    distanceback: int = 0


controllers = {
    "backup": BackupController(),
    "battery": BatteryController(),
    "climate": ClimateController(),
    "motor": MotorController(),
    "sensor": SensorController()
}

__all__ = [
    'BackupController',
    'BatteryController',
    'ClimateController',
    'MotorController',
    'SensorController',
    'controllers'
]
