import pytest
from AwAws.Exceptions.exceptions import AwAwsException, AwAwsMissingParameter


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
