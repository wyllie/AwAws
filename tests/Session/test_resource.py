import inspect
import os

from unittest.mock import patch, ANY
from AwAws.Session.resource import Resource


def test_resource():
    resource = Resource()
    assert resource.resource is None
    assert resource.region_name is None
    inspect.isclass(Resource)
    assert isinstance(resource, Resource)


def test_init_with_region():
    test_region = 'us-least-6'
    resource = Resource(region_name=test_region)
    assert resource.region_name == 'us-least-6'


def test_set_region():
    test_region = 'us-least-7'
    resource = Resource()
    assert resource.region_name is None
    resource.set_region_name(test_region)
    assert resource.region_name == 'us-least-7'


def test_set_region_env():
    resource = Resource()
    assert resource.region_name is None
    os.environ['AWS_REGION'] = 'us-least-8'
    resource.set_region_name()
    assert resource.region_name == 'us-least-8'
    os.environ.pop('AWS_REGION')


@patch('boto3.session.Session.resource', autospec=True, return_value='boto!')
def test_get_resource(mock_resource):
    resource = Resource(region_name='us-least-9')
    chk = resource.get_resource('project-thunderball')
    assert chk == 'boto!'

    mock_resource.assert_called_with(ANY, 'project-thunderball', region_name='us-least-9')

