from AwAws.Session.session import Session


class Parameters():
    def __init__(self, env=None, service=None, name=None):

        self.env = env
        self.service = service
        self.name = name
        self.value = None
        self.fully_qualified_name = self.fully_qualified_parameter_name()


    def get_client(self, client=None):
        self.ssm = Session().get_client('ssm')
        return self.ssm


    def set_value(self, value):
        self.value = value


    def get(self):
        try:
            response = self.ssm.get_parameter(
                Name=self.fully_qualified_name
            )
            self.value = response['Parameter']['Value']
        except Exception as e:
            raise RuntimeError('Could not find: ' + self.fully_qualified_name +
                               ' ' + str(e))
        return self.value


    def put(self, value, overwrite=False):
        self.set_value(value)
        try:
            response = self.ssm.put_parameter(
                Name=self.fully_qualified_name,
                Value=self.value,
                Type='String',
                Overwrite=overwrite
            )
        except Exception as e:
            raise RuntimeError('Could not set: ' + self.fully_qualified_name +
                               ' ' + str(e))
        return response['Version']


    def fully_qualified_parameter_name(self):
        return '.'.join([self.env, self.service, self.name])



