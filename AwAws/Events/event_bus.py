
from AwAws.Events.events import Events
from AwAws.Session.session import Session


class EventsBus:
    '''Class to manage EventBridge Events'''

    def __init__(self, region_name=None, role_arn=None):
        self.accounts = []
        self.event_bus = 'event-bus/default'
        self.events = Session(region_name, role_arn).get_client('events')

    def add_accounts(self, ou=None):
        '''add accounts to the broadcast list'''
        # get the accounts for an ou if ou is defined

    def create_event(self, account, source, detail):
        '''Create an event that cen be written to an event-bus'''

        # account and target can be used to build a resource string
        region = self.events.get_region()
        resource_arn = ':'.join('arn', 'aws', 'events', region, account, self.event_bus)

        event = Events()
        event.add_resources(resource_arn)
        event.create_event(account)

    def set_event_bus(self, bus_name='default'):
        '''describes and event bus'''
        self.event_bus = '/'.join(['event-bus', bus_name])

    def send_event(self, event):
        self.events.put_events(Entries=[event])

    def broadcast_event(self):
        '''Send an event to multiple event buses'''
        for account in self.accounts:
            self.end_event(self.create_event(account))


