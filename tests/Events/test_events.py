import inspect
from AwAws.Events.events import Events


def test_init():
    events = Events()
    inspect.isclass(Events)
    assert isinstance(events, Events)


def test_create_event():
    event = Events(region_name='us-least-5')
    event.source = 'test_source'
    event.detail = 'test_detail'
    event.event_bus = 'event-bus/test-bus'

    chk = event.create_event('test_account')
    assert chk['Resources'][0] == "arn:aws:events:us-least-5:test_account:event-bus/test-bus"


def test_set_event_bus_default():
    events = Events()
    events.set_event_bus()
    assert events.event_bus == 'event-bus/default'


def test_set_event_bus_set():
    events = Events()
    events.set_event_bus(bus_name='deploy')
    assert events.event_bus == 'event-bus/deploy'


def test_add_resource():
    events = Events()
    events.add_resource('arn.aws.etc.etc')
    assert events.resources[0] == 'arn.aws.etc.etc'
