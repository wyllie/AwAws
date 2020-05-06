import json

from AwAws.Session.session import Session


class S3():
    def __init__(self, client=None, region_name=None):
        self.bucket_name = None
        self.key_name = None
        self.session = Session(region_name=region_name)
        if client:
            self.s3 = client
        else:
            self.s3 = self.session.get_client('s3')


    def set_key_name(self, key_name):
        """set the key name property (i.e., the s3 'file' name)"""
        self.key_name = key_name


    def set_bucket_name(self, bucket_name):
        """sets the bucket_name property for class. CHecks that bucket exists"""
        try:
            response = self.s3.head_bucket(Bucket=bucket_name)
            print('Response:', response)
        except Exception as e:
            raise Exception("Bucket: " + bucket_name + " not available " + str(e))

        self.bucket_name = bucket_name
        return self.bucket_name


    def put_data_object(self, data):
        """store a data structure - like an array or dict"""
        enc_data = json.dumps(data)

        try:
            res = self.s3.put_object(
                Body=enc_data,
                Bucket=self.bucket_name,
                Key=self.key_name
            )
        except Exception as e:
            raise Exception('Error saving to S3: ' + str(e))

        return res


    def put_file_object(self, data):
        """store binary info - an image, encrypted data, word doc, etc"""

        try:
            res = self.s3.put_object(
                Body=data,
                Bucket=self.bucket_name,
                Key=self.key_name
            )
        except Exception as e:
            raise Exception('Error saving to S3: ' + str(e))

        return res


    def get_data_object(self):
        try:
            obj = self.s3.get_object(
                Bucket=self.bucket_name,
                Key=self.key_name
            )
        except Exception as e:
            raise Exception('Error reading from S3: ' + str(e))

        return json.loads(obj['Body'])


    def get_file_object(self):
        try:
            obj = self.s3.get_object(
                Bucket=self.bucket_name,
                Key=self.key_name
            )
        except Exception as e:
            raise Exception('Error reading from S3: ' + str(e))

        return obj['Body']


    def get_streaming_file_object(self):
        '''
        for reading objects from s3
        retutns a binary object which can be decoded
            with decode('utf-8') for example
        '''

        try:
            obj = self.s3.get_object(
                Bucket=self.bucket_name,
                Key=self.key_name
            )
        except Exception as e:
            raise Exception('Error reading from S3: ' + str(e))

        return obj['Body'].read()



    # bucket properties
    # list buckets
    # list objects
    # download object(s)
    # upload object(s)
    # remove object(s) - maybe
