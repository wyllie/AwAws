import botocore.session

from AwAws.Utils.env import Env

# When setting the region, the env variable will be the lowest priority
#    + set by caller
#    + set by credentials file
#    + set by env


class Session():
    def __init__(self, region_name=None):
        self.session = None
        self.region_name = region_name
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
        if self.session is None:
            self._get_session()
        return self.session.create_client(service, region_name=self.get_region())


    def _get_session(self):
        self.session = botocore.session.get_session()
        return self.session

