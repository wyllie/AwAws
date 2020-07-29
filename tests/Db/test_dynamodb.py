import inspect
import pytest

from botocore.stub import Stubber
from AwAws.Db.dynamodb import DynamoDb


def test_init():
    db = DynamoDb('test_table')
    assert inspect.isclass(DynamoDb)
    assert isinstance(db, DynamoDb)

    # checking to make sure we got the correct boto classes
    assert str(type(db.dynamo)) == "<class 'boto3.resources.factory.dynamodb.ServiceResource'>"
    assert str(type(db.table)) == "<class 'boto3.resources.factory.dynamodb.Table'>"


def test_init_fails():
    'fails if we do not specify a table name'
    with pytest.raises(TypeError):
        DynamoDb()


def test_delete_item():
    db = DynamoDb('blargh')
    with Stubber(db.table.meta.client) as stubber:
        stubber.add_response('delete_item', {
            'ConsumedCapacity': {'TableName': 'blargh'}
        })

        chk = db.delete_item('some_key')
        assert chk['ConsumedCapacity']['TableName'] == 'blargh'


def test_get_item():
    db = DynamoDb('blargh')
    with Stubber(db.table.meta.client) as stubber:
        item = {'id': {'S': 'some_key_id'}, 'this': {'S': 'some test text'}}
        stubber.add_response('get_item', {
            'Item': item,
            'ConsumedCapacity': {'TableName': 'blargh'}
        })

        chk = db.get_item('some_key')
        assert chk['ConsumedCapacity']['TableName'] == 'blargh'
        assert chk['Item']['id'] == 'some_key_id'
        assert chk['Item']['this'] == 'some test text'


def test_put_item():
    db = DynamoDb('blargh')
    with Stubber(db.table.meta.client) as stubber:
        stubber.add_response('put_item', {'ConsumedCapacity': {'TableName': 'blargh'}})

        item = {'id': 1, 'this': 'text'}
        chk = db.put_item(item)
        assert chk['ConsumedCapacity']['TableName'] == 'blargh'


def test_query_by_partition_key():
    db = DynamoDb('blargh')
    with Stubber(db.table.meta.client) as stubber:
        items = [
            {'id': {'S': 'some_key_id'}, 'this': {'S': 'some test text'}},
            {'id': {'S': 'some_other_key_id'}, 'this': {'S': 'other test text'}}
        ]
        stubber.add_response('query', {'Items': items})

        chk = db.query_by_partition_key('id')
        assert chk['Items'][0]['id'] == 'some_key_id'
        assert chk['Items'][0]['this'] == 'some test text'
        assert chk['Items'][1]['id'] == 'some_other_key_id'
        assert chk['Items'][1]['this'] == 'other test text'


def test_query_by_partition_and_sort_key():
    db = DynamoDb('blargh')
    with Stubber(db.table.meta.client) as stubber:
        items = [
            {'id': {'S': 'some_key_id'}, 'this': {'S': 'some test text'}},
            {'id': {'S': 'some_other_key_id'}, 'this': {'S': 'other test text'}}
        ]
        stubber.add_response('query', {'Items': items})

        chk = db.query_by_partition_and_sort_key('id', None, 'this', None)
        assert chk['Items'][0]['id'] == 'some_key_id'
        assert chk['Items'][0]['this'] == 'some test text'
        assert chk['Items'][1]['id'] == 'some_other_key_id'
        assert chk['Items'][1]['this'] == 'other test text'
