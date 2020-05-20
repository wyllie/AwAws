
class Events:
    '''Class to create and manage EventBridge Events'''

    def __init__(self, region_name=None):
        self.source = None
        self.resources = []
        self.detail = None
        self.event_bus = None
        self.region_name = region_name

    def create_event(self, account):
        '''Create an event that cen be written to an event-bus'''

        # account and target can be used to build a resource string
        resource_arn = ':'.join(['arn', 'aws', 'events', self.region_name, account, self.event_bus])
        event = {
            'Source': self.source,
            'Resources': [resource_arn],
            'Detail': self.detail,
            'EventBusName': self.event_bus
        }
        return event

    def set_event_bus(self, bus_name='default'):
        '''describes and event bus'''
        self.event_bus = '/'.join(['event-bus', bus_name])

    def add_resource(self, resource_arn):
        self.resources.append(resource_arn)


