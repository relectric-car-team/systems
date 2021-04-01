import pytest

from systems import controllers


@pytest.fixture
def dummy_controller():
    Controller = controllers.ControllerDecorator()

    @Controller
    class DummyController:
        attr1: int = 0
        attr2: str = "attr2"

    return DummyController()


def test_controller_decorator_getters(dummy_controller):
    assert dummy_controller['attr1'] == 0
    assert dummy_controller['attr2'] == "attr2"
    assert dummy_controller.asdict() == {'attr1': 0, 'attr2': "attr2"}


def test_controller_decorator_setters(dummy_controller):
    dummy_controller['attr1'] = 5
    dummy_controller['attr2'] = "second attr"

    assert dummy_controller['attr1'] == 5
    assert dummy_controller['attr2'] == "second attr"
    assert dummy_controller.asdict() == {'attr1': 5, 'attr2': "second attr"}
