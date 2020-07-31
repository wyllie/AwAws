from AwAws.Session.session import Session


class Parameters:
    'parameters are store as <service>.<param> = value'
    def __init__(self, service, region_name=None, role_arn=None):
        self.service = service
        self.ssm = Session(region_name, role_arn).get_client('ssm')

    def get_param(self, name=None):
        'returns a specific parameter from service'
        fqn = self.fully_qualified_parameter_name(name)
        try:
            response = self.ssm.get_parameter(
                Name=fqn,
                WithDecryption=True
            )
        except Exception as e:
            raise RuntimeError('Could not find: ', fqn, e)
        return response['Parameter']

    def get_param_value(self, name=None):
        return self.get_param(name)['Value']

    def get_all(self):
        'returns all of the params related to this service'
        service_root = self.fully_qualified_parameter_name('')
        try:
            response = self.ssm.get_parameters_by_path(
                Path=service_root,
                WithDecryption=True
            )
        except Exception as e:
            raise RuntimeError('Could not find: ', service_root, e)

        # return a hash so they are easy to lookup
        ret_params = {}
        for param in response['Parameters']:
            name = param['Name'].split('/')[2]
            ret_params[name] = param
        return ret_params

    def put_param(self, name, value, secure=None):
        'stores a parameter in the SSM parameter store'
        fqn = self.fully_qualified_parameter_name(name)
        param_type = 'String'
        if secure == 'True':
            param_type = 'SecureString'
        elif isinstance(value, list):
            param_type = 'StringList'

        try:
            response = self.ssm.put_parameter(
                Name=fqn,
                Value=value,
                Type=param_type,
                Overwrite=True
            )
        except Exception as e:
            raise RuntimeError('Could not set: ', fqn, e)
        return response['Version']

    def fully_qualified_parameter_name(self, name):
        return '/'.join(['', self.service, name])
