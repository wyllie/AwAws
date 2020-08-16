===
API
===

.. automodule:: AwAws.Api.api
.. automodule:: AwAws.Api.event
.. automodule:: AwAws.Api.response

ApiGateway
=================

.. autoclass:: AwAws.Api.api.ApiGateway
   :members:
   :inherited-members:


Typically, when processing requests from ApiGateway, both the Event
and Response calsses are required.  This class initiallizes and exposes
both of those classes for easier use.  The Event class is used to prarse
data from the incoming request from Api Gateway while the Response class
offers a bunch of pre-canned responses that are formatted correctly for
ApiGateway.

Typical usage in a Lambda::

    def handle(self, event, context):
        api = ApiGateway()
        api.event.parse_event(event)

        # now api.event contains all of the event's properties
        try:
            assert api.event.method == 'PUT'
        except AssertionError:
            return api.response.error_4XX('PUT method required')

        response_body = {'all_good': 'some data to return}
        response = api.response.ok_200(body=response_body)
        return response

.. note:: Should also include a ``Context`` class

Event
=========

Used from ApiGateway class

.. autoclass:: AwAws.Api.event.Event
   :members:
   :inherited-members:

Response
============

Used from ApiGateway class

.. autoclass:: AwAws.Api.response.Response
   :inherited-members:
