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

    def set_region(self, region_name=None):
        env = Env()

        self.region_name = region_name
        if region_name is None:
            self.region_name = env.get_env('AWS_REGION')

        return self.region_name

    def get_region(self):
        return self.region_name

#    def get_client(self, service):
#        '''set up a client for an AWS session'''
#        if self.session is None:
#            self._get_session()
#        return self.session.create_client(service, region_name=self.get_region())

    def get_client(self, service):
        '''set up an AWS session'''
        access_key = None
        secret_key = None
        session_token = None

        if self.role_arn is not None:
            sts = Sts(role_arn=self.role_arn)
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
            region_name=self.get_region()
        )

        return client

