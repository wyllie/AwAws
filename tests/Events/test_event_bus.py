import inspect
from AwAws.Events.event_bus import EventsBus


def test_init():
    eb = EventsBus()
    assert eb.event_bus == 'event-bus/default'
    assert inspect.isclass(EventsBus)
    assert isinstance(eb, EventsBus)
    print(eb.events)
    assert str(type(eb.events)) == "<class 'botocore.client.EventBridge'>"


def test_create_event():
    assert True
