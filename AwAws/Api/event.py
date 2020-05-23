import base64
import json

from AwAws.Exceptions.exceptions import AwAwsInvalidHttpMethod
from AwAws.Exceptions.exceptions import AwAwsMissingRequirement


class Event():
    """
    **Attributes**:
        * **event**: (*dict*), None - the raw incoming event
        * **method**: (*string*), 'ANY' -  http method
        * **params**: (*dict*), {} - qstring params
        * **path**:  (*string*), None - incoming path
        * **body**: (*string*), {} - incoming data

    """
    #: Allowed HTTP Methods
    HTTP_METHODS = ['ANY', 'DELETE', 'GET', 'PATCH', 'POST', 'PUT']

    def __init__(self):
        self.event = None
        self.method = 'ANY'
        self.params = None
        self.path = None
        self.body = None


    def parse_event(self, event):
        """grab the api gateway event and parse out the good bits"""
        try:
            self.set_event(event)
            self.set_http_method()
            self.set_body()
            self.set_qstring_params()
            self.set_path_params()
        except Exception as e:
            raise Exception('Error processing event: ' + str(e))


    def set_event(self, event):
        """load the incoming event"""
        self.event = event


    def set_http_method(self):
        """get the http method on the incoming event"""
        try:
            assert self.event is not None
        except AssertionError:
            raise AwAwsMissingRequirement('Event not set: use event.set_event()')

        try:
            method = str.upper(self.event['httpMethod'])
            assert method in Event.HTTP_METHODS
        except AssertionError:
            raise AwAwsInvalidHttpMethod(method)

        self.method = method


    def set_body(self):
        """grab the body section from the incoming event (if it exists)"""
        try:
            assert self.event is not None
        except AssertionError:
            raise AwAwsMissingRequirement('Event not set: use event.set_event()')

        try:
            self.event['body']
        except KeyError:
            return  # body not set, don't do anything

        try:
            assert self.event['isBase64Encoded'] is True
            self.body = json.loads(base64.b64decode(self.event['body']))
        except AssertionError:
            self.body = self.event['body']
        except Exception as e:
            raise Exception('Error decoding event body' + str(e))


    def set_qstring_params(self):
        """get the query string params from the event"""
        try:
            assert self.event is not None
        except AssertionError:
            raise AwAwsMissingRequirement('Event not set: use event.set_event()')

        try:
            self.params = self.event['queryStringParameters']
        except KeyError:
            return  # no query_string parameters, don't do anything


    def set_path_params(self):
        """get the path parameters from the event"""
        try:
            assert self.event is not None
        except AssertionError:
            raise AwAwsMissingRequirement('Event not set: use event.set_event()')

        try:
            self.path = self.event['pathParameters']
            self.path = self.event['pathParameters']['proxy']
        except KeyError:
            return  # no path parameters, don't do anything
