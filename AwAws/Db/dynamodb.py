from boto3.dynamodb.conditions import Key
from AwAws.Session.resource import Resource


class DynamoDb:
    def __init__(self, table_name, region_name=None):
        self.table_name = table_name
        self.dynamo = Resource(region_name).get_resource('dynamodb')
        self.table = self._get_table_object()

    def delete_item(self, primary_key_id):
        'delete an item from a dynamo table by primary key id'
        return self.table.delete_item(Key={'S': primary_key_id})

    def get_item(self, primary_key_id):
        'get an item from a dynamo table by primary key id'
        return self.table.get_item(Key={'S': primary_key_id})

    def put_item(self, item):
        'put item in dynamoDb table'
        return self.table.put_item(Item=item)

    def query_by_partition_key(self, partition_key, partition_key_value=None):
        'get a list of items by primary_key and sort_key'
        query = Key(partition_key).eq(partition_key_value)

        return self.table.query(KeyConditionExpression=query)

    def query_by_partition_and_sort_key(self, partition_key, partition_key_value,
                                        sort_key, sort_key_value):
        'get a list of items by primary_key and sort_key'
        return self.table.query(
            KeyConditionExpression=Key(partition_key).eq(partition_key_value) &
            Key(sort_key).begins_with(sort_key_value)
        )


    def _get_table_object(self):
        'gets a dynamodb.Table resource'
        try:
            table = self.dynamo.Table(self.table_name)
        except Exception as e:
            raise Exception('Error on table name', e)
        return table


