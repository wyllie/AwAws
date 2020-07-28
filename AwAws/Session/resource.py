import boto3

from functools import lru_cache
from AwAws.Utils.env import Env


class Resource:
    def __init__(self, region_name=None):
        self.resource = None
        self.region_name = None
        self.set_region_name(region_name)

    def set_region_name(self, region_name=None):
        'we need to set a region name if it is not set yet'
        env = Env()

        self.region_name = region_name
        if self.region_name is None:
            self.region_name = env.get_env('AWS_REGION')

    def get_resource(self, resource):
        'set up and AWS resource'
        return self._cached_connection(resource, region_name=self.region_name)

    @classmethod
    @lru_cache(100) # potentially cache 100 resources
    def _cached_connection(cls, resource, region_name=None):
        return boto3.resource(resource, region_name=region_name)