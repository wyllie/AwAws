import pytest

from AwAws.SharedResources.parameters import Parameters


def test_fully_qualified_parameter_name():
    env = 'test'
    service = 'database'
    name = 'hostname'

    params = Parameters(env, service, name)
    assert params._fully_qualified_parameter_name() == 'test.database.hostname'

    new_params = Parameters(env, None, name)
    with pytest.raises(TypeError):
        new_params._fully_qualified_parameter_name()
