import os
from moto import mock_ssm
from AwAws.Session.session import Session


@mock_ssm
def test_session():
    session = Session()
    assert str(type(session)) == "<class 'AwAws.Session.session.Session'>"


@mock_ssm
def test_session_region():
    session = Session(region_name='us-least-9')
    assert session.region_name == 'us-least-9'


@mock_ssm
def test_session_region_env():
    session = Session()
    assert session.region_name == 'us-least-7'

    os.environ['AWS_REGION'] = 'us-least-7'
    session = Session()
    assert session.region_name == 'us-least-7'
    os.environ.pop('AWS_REGION')


@mock_ssm
def test_client():
    session = Session()
    client = session.get_client('ssm')
    assert str(type(client)) == "<class 'botocore.client.SSM'>"
