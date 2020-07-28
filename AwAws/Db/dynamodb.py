from AwAws.Session.resource import Resource


class DynamoDb():
    def __init__(self, table_name, region_name=None):
        self.table_name = table_name
        self.dynamo = Resource(region_name).get_resource('dynamodb')
        self.table = self._get_table_object(table_name)

    def put_item(self, item):
        'put item in dynamoDb table'
        table = self.table
        res = table.put_item(Item=item)
        return res

    def _get_table_object(self, table_name):
        'gets a dynamodb.Table resource'
        if table_name is not None:
            self.table_name = table_name

        try:
            table = self.dynamo.Table(self.table_name)
        except Exception as e:
            raise Exception('Error on table name', e)
        return table


