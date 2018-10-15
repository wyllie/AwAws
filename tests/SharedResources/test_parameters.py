import pytest

from AwAws.SharedResources.parameters import Parameters


def test_fully_qualified_parameter_name():
    env = 'test'
    service = 'database'
    name = 'hostname'

    params = Parameters(env, service, name)
    assert params._fully_qualified_parameter_name() == 'test.database.hostname'

    with pytest.raises(TypeError):
        Parameters(env, None, name)


@pytest.mark.skip(reason='this test connects to AWS directly, needs mock')
def test_get():
    env = 'test'
    service = 'mongo'
    name = 'hostname'
    params = Parameters(env, service, name)

    assert params.get() == 'test.mongo.com'
