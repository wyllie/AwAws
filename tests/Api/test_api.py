from AwAws.Api.api import ApiGateway
from AwAws.Api.event import Event
from AwAws.Api.response import Response


def test_init():
    api = ApiGateway()
    assert type(api) == ApiGateway
    assert type(api.event) == Event
    assert type(api.response) == Response
