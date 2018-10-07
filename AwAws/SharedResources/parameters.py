import boto3


class Parameters():
    def __init__(self, env=None, service=None, name=None):
        self.client = boto3.client('ssm')

        self.env = env
        self.service = service
        self.name = name
        self.value = None


    def _fully_qualified_parameter_name(self):
        self.fully_qualified_name = '.'.join([self.env, self.service, self.name])
        return self.fully_qualified_name



