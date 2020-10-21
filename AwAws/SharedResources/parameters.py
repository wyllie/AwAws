import pickle  # nosec - safe inside lambda environment

from AwAws.Session.session import Session


class Parameters:
    'parameters are store as <service>.<param> = value'
    def __init__(self, service, region_name=None, role_arn=None):
        self.service = service
        self.region_name = region_name
        self.role_arn = role_arn
        self.tmp_file_loc = '/tmp/awaws_ssm_params'
        self.ssm = None

    def get_ssm(self):
        if self.ssm is None:
            self.ssm = Session(self.region_name, self.role_arn).get_client('ssm')
        return self.ssm

    def get_param(self, name=None):
        'returns a specific parameter from service'
        fqn = self.fully_qualified_parameter_name(name)
        try:
            response = self.get_ssm().get_parameter(
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
            response = self.get_ssm().get_parameters_by_path(
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

    def get_param_dictionary(self):
        'returns all the params as key/value pairs'
        params = self.get_all()
        param_dict = {}
        for name in params.keys():
            param_dict[name] = params[name]['Value']
        return param_dict

    def put_param(self, name, value, secure=None):
        'stores a parameter in the SSM parameter store'
        fqn = self.fully_qualified_parameter_name(name)
        param_type = 'String'
        if secure == 'True':
            param_type = 'SecureString'
        elif isinstance(value, list):
            param_type = 'StringList'

        try:
            response = self.get_ssm().put_parameter(
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

    def create_tmp_dict(self):
        'store key/value pairs in a tmp file (for lambda)'
        params = self.get_param_dictionary()
        file = open(self.tmp_file_loc, 'wb')
        pickle.dump(params, file)  # nosec - safe inside a lambda
        file.close()

    def read_tmp_dict(self):
        'read tmp file and return contents'
        file = open(self.tmp_file_loc, 'rb')
        params = pickle.load(file)  # nosec - safe inside a lambda
        return params
