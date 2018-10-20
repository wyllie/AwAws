import pytest

from botocore.stub import Stubber
from AwAws.SharedResources.parameters import Parameters


def test_init():
    params = Parameters(env='test-env', service='test-service', name='test-name')
    assert params.env == 'test-env'
    assert params.service == 'test-service'
    assert params.name == 'test-name'
    assert params.value is None
    assert params.fully_qualified_name == 'test-env.test-service.test-name'


def test_get_client():
    params = Parameters(env='test-env', service='test-service', name='test-name')
    client = params.get_client()
    assert str(type(client)) == "<class 'botocore.client.SSM'>"


def test_set_value():
    params = Parameters(env='test-env', service='test-service', name='test-name')
    assert params.value is None
    params.set_value('test-value')
    assert params.value is 'test-value'


def test_get(ssm_get_response):
    env = 'test'
    service = 'mongo'
    name = 'hostname'

    params = Parameters(env, service, name)
    ssm = params.get_client()
    with Stubber(ssm) as stubber:
        stubber.add_response('get_parameter', ssm_get_response)
        assert params.get() == 'xtest.mongo.com'


def test_get_fail():
    env = 'test'
    service = 'mongo-fail'
    name = 'hostname'

    params = Parameters(env, service, name)
    ssm = params.get_client()
    with Stubber(ssm) as stubber:
        stubber.add_client_error('get_parameter')
        with pytest.raises(RuntimeError):
            params.get()


def test_put(ssm_put_response):
    env = 'test'
    service = 'mongo'
    name = 'hostname'

    params = Parameters(env, service, name)
    ssm = params.get_client()
    with Stubber(ssm) as stubber:
        stubber.add_response('put_parameter', ssm_put_response)
        stubber.add_response('put_parameter', ssm_put_response)
        assert params.put('test.mongo.name') == 1234
        assert params.put('test.mongo.name', True) == 1234


def test_put_fail():
    env = 'test'
    service = 'mongo'
    name = 'hostname'

    params = Parameters(env, service, name)
    ssm = params.get_client()
    with Stubber(ssm) as stubber:
        stubber.add_client_error('put_parameter')
        with pytest.raises(RuntimeError):
            params.put(None)


def test_fully_qualified_parameter_name():
    env = 'test'
    service = 'database'
    name = 'hostname'

    params = Parameters(env, service, name)
    assert params.fully_qualified_parameter_name() == 'test.database.hostname'

    with pytest.raises(TypeError):
        Parameters(env, None, name)
