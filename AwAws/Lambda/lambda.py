import os
import sys
import time

# The goal here is to provide common lambda functionality
# including logging and metrics tools.  We also want to
# incorporate a mechanism to 'keep the lambdas warm' which is
# just a bit of logic that shortcircuts the actual lambda
# function code and just returns a success


class Lambda():
    def __init__(self):
        # the lambda env uses /var/task/lib to store code
        sys.path.append('/var/task/lib')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        sys.path.append(os.path.join(dir_path, 'lib'))
        self.status = 'ok'


    def do_something(self):
        return 'ok'

    def get_region(self):
        return os.environ.get('AWS_REGION')

    def get_aw_env(self):
        return os.environ.get('AW_ENV')

    def get_aw_account(self):
        return os.environ.get('AW_ACCT')

    def get_env(self, var_name):
        return os.environ.get(var_name)

    @classmethod
    def get_handler(cls, *args, **kwargs):
        def handler(event, context):
            if 'whipit' in event:
                print('WHIP IT GOOD') # stay awake
                time.sleep(0.5)
                return 'whipped'
            return cls(*args, **kwargs).handle(event, context)
        return handler

    def handle(self, event, context):
        raise NotImplementedError
