import pytest
from AwAws.Exceptions.exceptions import AwAwsException
from AwAws.Exceptions.exceptions import AwAwsConfigurationError
from AwAws.Exceptions.exceptions import AwAwsInvalidHttpMethod
from AwAws.Exceptions.exceptions import AwAwsMissingParameter
from AwAws.Exceptions.exceptions import AwAwsMissingRequirement
from AwAws.Exceptions.exceptions import AwAwsInvalidEvent


def test_init():
    with pytest.raises(AwAwsException):
        AwAwsException('test message')


def test_init_fail():
    some_data = {
        'this': True,
        'that': False,
        'theOther': 'this is the other - this one is really long'
    }
    with pytest.raises(AwAwsMissingParameter):
        AwAwsMissingParameter('something is missing: here is what we got ', some_data)


def test_missing_param():
    some_data = {
        'this': True,
        'that': False,
        'theOther': 'something other - blarghhhhh!'
    }
    with pytest.raises(AwAwsMissingParameter):
        AwAwsMissingParameter('something other - blarghhhhh!', some_data)


def test_configuration_error():
    with pytest.raises(AwAwsConfigurationError, match='Invalid Configuration: ' +
                       'Missing required or expected parameter'):
        raise AwAwsConfigurationError('test it')


def test_invalid_event():
    with pytest.raises(AwAwsInvalidEvent, match='Invalid Event Syntax: test it'):
        raise AwAwsInvalidEvent('test it')


def test_invalid_http_method():
    with pytest.raises(AwAwsInvalidHttpMethod, match='Not a valid http method: test it'):
        raise AwAwsInvalidHttpMethod('test it')


def test_missing_param():
    some_data = {
        'this': True,
        'that': False,
        'theOther': 'this is the other - this one is really long'
    }
    with pytest.raises(AwAwsMissingParameter):
        AwAwsMissingParameter('something is missing: here is what we got ', some_data)


def test_missing_requirements():
    with pytest.raises(AwAwsMissingRequirement, match='Missing Requirement: test it'):
        raise AwAwsMissingRequirement('test it')

