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

