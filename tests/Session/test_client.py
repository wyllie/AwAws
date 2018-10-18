import os
from AwAws.Session.session import Session


def test_session():
    session = Session()
    assert session.session is None
    assert session.region_name is None
    assert str(type(session)) == "<class 'AwAws.Session.session.Session'>"


def test_session_region():
    session = Session(region_name='us-least-9')
    assert session.region_name == 'us-least-9'


def test_session_region_env():
    session = Session()
    assert session.get_region() == None

    os.environ['AWS_REGION'] = 'us-least-7'
    session.set_region()
    assert session.region_name == 'us-least-7'
    assert session.get_region() == 'us-least-7'
    os.environ.pop('AWS_REGION')


def test_client():
    session = Session()
    client = session.get_client('ssm')
    assert str(type(client)) == "<class 'botocore.client.SSM'>"
