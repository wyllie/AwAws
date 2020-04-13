from AwAws.Session.session import Session


class Parameters():
    def __init__(self, env=None, service=None, name=None):

        self.env = env
        self.service = service
        self.name = name
        self.value = None
        self.fully_qualified_name = self._fully_qualified_parameter_name()


    def get_client(self, client=None):
        if client:
            self.ssm = client
        else:
            self.ssm = Session().get_client('ssm')
        return self.ssm


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


    def _fully_qualified_parameter_name(self):
        return '.'.join([self.env, self.service, self.name])



