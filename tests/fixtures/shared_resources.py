import pytest

# This fixture provides resources for the SSM module


@pytest.fixture
def ssm_get_response():
    response = {
        'Parameter': {
            'Type': 'String',
            'Name': 'test.mongo.hostname',
            'Value': 'xtest.mongo.com'
        }
    }
    return response


@pytest.fixture
def ssm_put_response():
    response = {
        'Version': 1234
    }
    return response
