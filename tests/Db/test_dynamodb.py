import inspect
import pytest

from botocore.stub import Stubber
from AwAws.Db.dynamodb import DynamoDb


def test_init():
    db = DynamoDb('test_table')
    assert inspect.isclass(DynamoDb)
    assert isinstance(db, DynamoDb)
    assert str(type(db.dynamo)) == "<class 'boto3.resources.factory.dynamodb.ServiceResource'>"
    assert str(type(db.table)) == "<class 'boto3.resources.factory.dynamodb.Table'>"


def test_init_fails():
    'fails if we do not specify a table name'
    with pytest.raises(TypeError):
        DynamoDb()


def test_put_item():
    db = DynamoDb('test_table')
    stubber = Stubber(db.table.meta.client)
    stubber.add_response('put_item', {'ConsumedCapacity': {'TableName': 'blargh'}})
    stubber.activate()

    item = {'id': 1, 'this': 'text'}
    chk = db.put_item(item)
    assert chk['ConsumedCapacity']['TableName'] == 'blargh'
