import inspect
import pytest

from botocore.stub import Stubber
from AwAws.SharedResources.parameters import Parameters


# set up some simple responses from SSM
@pytest.fixture
def ssm_get_response():
    response = {
        'Parameter': {
            'Type': 'String',
            'Name': '/alpha/hostname',
            'Value': 'some.hostname.com'
        }
    }
    return response


@pytest.fixture
def ssm_get_all_response():
    response = {
        'Parameters': [
            {
                'Type': 'String',
                'Name': '/alpha/hostname',
                'Value': 'some.hostname.com'
            },
            {
                'Type': 'SecureString',
                'Name': '/alpha/password',
                'Value': 'p@ssw0rd123'
            },
        ]
    }
    return response


@pytest.fixture
def ssm_put_response():
    response = {
        'Version': 1234
    }
    return response


def test_init():
    params = Parameters(service='test_service')
    inspect.isclass(Parameters)
    assert params.service == 'test_service'
    assert params.region_name is None
    assert params.role_arn is None
    assert params.tmp_file_loc == '/tmp/awaws_ssm_params'
    assert params.ssm is None


def test_get_ssm():
    params = Parameters(service='test_service')
    params.get_ssm()
    assert str(type(params.ssm)) == "<class 'botocore.client.SSM'>"


def test_get_param(ssm_get_response):
    params = Parameters(service='alpha')
    params.get_ssm()
    with Stubber(params.ssm) as stubber:
        stubber.add_response('get_parameter', ssm_get_response)
        assert params.get_param('hostname')['Value'] == 'some.hostname.com'


def test_get_param_value(ssm_get_response):
    params = Parameters(service='alpha')
    params.get_ssm()
    with Stubber(params.ssm) as stubber:
        stubber.add_response('get_parameter', ssm_get_response)
        assert params.get_param_value('hostname') == 'some.hostname.com'


def test_get_fail():
    params = Parameters(service='omega')
    params.get_ssm()
    with Stubber(params.ssm) as stubber:
        stubber.add_client_error('get_parameter')
        with pytest.raises(RuntimeError):
            params.get_param('hostname')


def test_get_all(ssm_get_all_response):
    params = Parameters(service='test_service')
    params.get_ssm()
    with Stubber(params.ssm) as stubber:
        stubber.add_response('get_parameters_by_path', ssm_get_all_response)
        my_params = params.get_all()
        assert my_params['hostname']['Value'] == 'some.hostname.com'
        assert my_params['password']['Value'] == 'p@ssw0rd123'


def test_put_param(ssm_put_response):
    params = Parameters(service='alpha')
    params.get_ssm()
    with Stubber(params.ssm) as stubber:
        stubber.add_response('put_parameter', ssm_put_response)
        stubber.add_response('put_parameter', ssm_put_response)
        assert params.put_param('param1', 'test1.mongo.name') == 1234
        assert params.put_param('param2', 'test2.mongo.name', secure=True) == 1234


def test_put_fail():
    params = Parameters(service='omega')
    params.get_ssm()
    with Stubber(params.ssm) as stubber:
        stubber.add_client_error('put_parameter')
        with pytest.raises(RuntimeError):
            params.put_param('a', 'b')


def test_fully_qualified_parameter_name():
    params = Parameters(service='beta')
    assert params.fully_qualified_parameter_name('hello') == '/beta/hello'
