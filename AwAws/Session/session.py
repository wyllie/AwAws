import botocore.session

from AwAws.Session.sts import Sts
from AwAws.Utils.env import Env

# When setting the region, the env variable will be the lowest priority
#    + set by caller
#    + set by credentials file
#    + set by env


class Session:
    def __init__(self, region_name=None, role_arn=None):
        self.session = None
        self.region_name = region_name
        self.role_arn = role_arn
        return None


    def set_region(self, region_name=None):
        env = Env()

        self.region_name = region_name
        if region_name is None:
            self.region_name = env.get_env('AWS_REGION')

        return self.region_name


    def get_region(self):
        return self.region_name


    def get_client(self, service):
        '''set up a client for an AWS session'''
        if self.session is None:
            self._get_session()
        return self.session.create_client(service, region_name=self.get_region())


    def _get_session(self):
        '''set up an AWS session'''
        if self.role_arn is not None:
            sts = Sts(role_arn=self.role_arn)
            credentials = sts.assume_role()
            self.session = botocore.session.get_session(
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken']
            )
        else:
            self.session = botocore.session.get_session()

        return self.session

