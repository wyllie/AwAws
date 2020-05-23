import json
import pytest

from AwAws.Api.event import Event
from AwAws.Exceptions.exceptions import AwAwsInvalidHttpMethod
from AwAws.Exceptions.exceptions import AwAwsMissingRequirement


def test_init():
    event = Event()
    assert type(event) == Event
    assert event.method == 'ANY'
    assert event.params is None
    assert event.body is None


def test_process_event(datadir):
    apigw_event = json.loads(open(datadir.join('apigw_event.json'), 'rt').read())

    event = Event()
    event.parse_event(apigw_event)

    assert event.event == apigw_event
    assert event.method == 'POST'
    assert event.body['data_stuff'] == 'down is the new up'
    assert event.params['foo'] == 'bar'
    assert event.path == '/the/cool/path'


def test_process_event_fail(datadir):
    apigw_event = json.loads(open(datadir.join('apigw_event_err.json'), 'rt').read())

    event = Event()
    with pytest.raises(Exception):
        event.parse_event(apigw_event)


def test_set_event(datadir):
    apigw_event = json.loads(open(datadir.join('apigw_event.json'), 'rt').read())
    event = Event()
    event.set_event(apigw_event)
    assert event.event['path'] == '/the/cool/path'


def test_set_http_method(datadir):
    apigw_event = json.loads(open(datadir.join('apigw_event.json'), 'rt').read())
    event = Event()
    event.set_event(apigw_event)
    event.set_http_method()
    assert event.method == 'POST'


def test_set_http_method_error_1(datadir):
    event = Event()
    with pytest.raises(AwAwsMissingRequirement, match='Event not set'):
        event.set_http_method()


def test_set_http_method_error_2(datadir):
    apigw_event = json.loads(open(datadir.join('apigw_event_3.json'), 'rt').read())
    event = Event()
    event.set_event(apigw_event)
    with pytest.raises(AwAwsInvalidHttpMethod, match='Not a valid http method: BLARGH'):
        event.set_http_method()


def test_set_body_encoded(datadir):
    apigw_event = json.loads(open(datadir.join('apigw_event.json'), 'rt').read())
    event = Event()
    event.set_event(apigw_event)
    event.set_body()
    print(event.body)
    assert event.body['data_stuff'] == "down is the new up"


def test_set_body_dencoded(datadir):
    apigw_event = json.loads(open(datadir.join('apigw_event_2.json'), 'rt').read())
    event = Event()
    event.set_event(apigw_event)
    event.set_body()
    assert event.body['data_stuff'] == "down is the new up"


def test_set_body_dencoded_error(datadir):
    apigw_event = json.loads(open(datadir.join('apigw_event_4.json'), 'rt').read())
    event = Event()
    event.set_event(apigw_event)
    with pytest.raises(Exception, match=r'Error decoding'):
        event.set_body()


def test_set_body_no_body(datadir):
    apigw_event = json.loads(open(datadir.join('apigw_event_3.json'), 'rt').read())
    event = Event()
    event.set_event(apigw_event)
    event.set_body()
    assert event.body is None


def test_set_body_no_event():
    event = Event()
    with pytest.raises(AwAwsMissingRequirement,
                       match=r'use event.set_event()'
                       ):
        event.set_body()


def test_set_qstring_params(datadir):
    apigw_event = json.loads(open(datadir.join('apigw_event.json'), 'rt').read())
    event = Event()
    event.set_event(apigw_event)
    event.set_qstring_params()
    assert event.params['foo'] == 'bar'


def test_set_qstring_params_error(datadir):
    event = Event()
    with pytest.raises(AwAwsMissingRequirement, match='Event not set'):
        event.set_qstring_params()


def test_set_qstring_params_no_qsring(datadir):
    apigw_event = json.loads(open(datadir.join('apigw_event_4.json'), 'rt').read())
    event = Event()
    event.set_event(apigw_event)
    check = event.set_qstring_params()
    assert check is None


def test_set_path_params(datadir):
    apigw_event = json.loads(open(datadir.join('apigw_event.json'), 'rt').read())
    event = Event()
    event.set_event(apigw_event)
    event.set_path_params()
    assert event.path == '/the/cool/path'


def test_set_path_params_error(datadir):
    event = Event()
    with pytest.raises(AwAwsMissingRequirement, match='Event not set'):
        event.set_path_params()


def test_set_path_missing(datadir):
    apigw_event = json.loads(open(datadir.join('apigw_event_no_path.json'), 'rt').read())
    event = Event()
    event.set_event(apigw_event)
    event.set_path_params()
    assert event.path is None
