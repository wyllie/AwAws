import boto3

from AwAws.Utils.env import Env


class Session(boto3.session.Session):
    def __init__(self, **kwargs):
        env = Env()

        region_name = None
        if 'region_name' in kwargs:
            region_name = str(kwargs['region_name'])
        elif env.get_env('AWS_REGION'):
            region_name = env.get_env('AWS_REGION')

        super().__init__(region_name=region_name)


    def get_client(self, service):
        return self.client(service)

