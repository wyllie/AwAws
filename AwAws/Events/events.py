
from AwAws.Session.session import Session

class Events():
    def __init__(self, client=None, region_name=None, event=None):
        self.session = Session(region_name=region_name)
        self.accounts = []
        self.event_bus = 'default'
        self.event=event
        if client:
            self.events = client
        else:
            self.events = self.session.get_client('events')


    def broadcast_event(self):
        '''Send an event to multiple accounts'''

        for account in self.accounts:


    def add_accounts(self, ou=None):
        '''add accounts to the broadcast list'''

        # get the accounts for an ou if ou is defined


    def create_event(self, account, target, detail):
        '''Create an event that cen be written to an event-bus'''

        # account and target can be used to build a resource string
        region = self.events.get_region()
        resource_arn = ':'.join('arn', 'aws', 'events', region, account, self.event_bus)


    def set_event_bus(self, bus_name=default):
        '''describes and event bus'''
        self.event_bus = '/'.join(['event-bus', bus_name])


