import pytest

from botocore.stub import Stubber
from AwAws.SharedResources.parameters import Parameters

response = {
    'Parameter': {
        'Type': 'String',
        'Name': 'test.mongo.hostname',
        'Value': 'xtest.mongo.com'
    }
}


def test_fully_qualified_parameter_name():
    env = 'test'
    service = 'database'
    name = 'hostname'

    params = Parameters(env, service, name)
    assert params._fully_qualified_parameter_name() == 'test.database.hostname'

    with pytest.raises(TypeError):
        Parameters(env, None, name)


def test_get():
    env = 'test'
    service = 'mongo'
    name = 'hostname'

    params = Parameters(env, service, name)
    ssm = params.get_client()
    with Stubber(ssm) as stubber:
        stubber.add_response('get_parameter', response)
        assert params.get() == 'xtest.mongo.com'
