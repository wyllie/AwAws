
from AwAws.Events.events import Events

class EventsBus():
    '''Class to manage EventBridge Events'''

    def __init__(self, region_name=None):
        self.event_bus = 'default'
        self.event = None
        self.session = Session(region_name=region_name)
        self.events = self.session.get_client('events')

    def add_accounts(self, ou=None):
        '''add accounts to the broadcast list'''
        # get the accounts for an ou if ou is defined

    def create_event(self, account, source, detail):
        '''Create an event that cen be written to an event-bus'''

        # account and target can be used to build a resource string
        region = self.events.get_region()
        resource_arn = ':'.join('arn', 'aws', 'events', region, account, self.event_bus)

        event = Event()
        event = {
            'Source': source,
            'Resources': [resource_arn],
            'Detail': detail,
            'EventBusName': event_bus
        }

    def set_event_bus(self, bus_name=default):
        '''describes and event bus'''
        self.event_bus = '/'.join(['event-bus', bus_name])

    def send_event(self, event):
        self.events.put_events(Entries=[event])

    def broadcast_event(self):
        '''Send an event to multiple event buses'''
        for account in self.accounts:
            event = self.create_event(account, detail)


