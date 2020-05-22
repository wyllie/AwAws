import botocore.session

from functools import lru_cache
from AwAws.Session.sts import Sts
from AwAws.Utils.env import Env

# When setting the region, the env variable will be the lowest priority
#    + set by caller
#    + set by credentials file
#    + set by env


class Session:
    def __init__(self, region_name=None, role_arn=None):
        self.session = None
        self.region_name = self.set_region(region_name)
        self.role_arn = role_arn

    def set_region(self, region_name=None):
        '''we need to set a region if it is unset at this point'''
        env = Env()

        self.region_name = region_name
        if region_name is None:
            self.region_name = env.get_env('AWS_REGION')

        return self.region_name

    def get_region(self):
        return self.region_name

    def get_client(self, service):
        '''set up an AWS session'''
        return self._cached_connection(
            service,
            role_arn=self.role_arn,
            region_name=self.get_region()
        )

    @classmethod
    @lru_cache(100)  # potentially cache 100 services??
    def _cached_connection(cls, service, role_arn=None, region_name=None):
        '''set up an AWS session'''
        access_key = None
        secret_key = None
        session_token = None

        if role_arn is not None:
            sts = Sts(role_arn=role_arn)
            sts.assume_role()
            access_key = sts.aws_access_key_id
            secret_key = sts.aws_secret_access_key
            session_token = sts.aws_session_token

        boto_session = botocore.session.get_session()
        client = boto_session.create_client(
            service,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token,
            region_name=region_name
        )

        return client


