from AwAws.Session.session import Session

# https://youtu.be/RidtrSCogg0
# the whipit function is used to keep lambdas warm.
# setup and environment variable called 'WHIPIT' with the number of
# concurent lambdas to 'whip'
#
# the lambda function that calls this should be configured though
# Cloudwatch Events and set up to run every 30 minutes
#
# Hopefully, some day, AWS will fix their cold start issues


class LambdaTools():
    def __init__(self, client=None):
        if client:
            self.lbd = client
        else:
            self.lbd = Session().get_client('lambda')


    def whipit(self):
        'this function can be used to keep lambdas warm'

        # get a list of installed lambda functions
        try:
            functions = self.lbd.list_functions()
        except Exception as e:
            raise Exception('Could not get lambda function list: ' + str(e))

        # loop through all of the functions, and whipit
        mesg = {
            'status': 'ok',
            'functions': 0,
            'errors': []
        }
        for func in functions['Functions']:
            if 'Environment' in func and 'Variables' in func['Environment']:
                func_name = func['FunctionName']

                try:
                    whipping = int(func['Environment']['Variables']['WHIPIT'])
                except KeyError:
                    continue
                except Exception:
                    mesg['status'] = 'failed'
                    mesg['errors'].append(func_name + ' WHIPIT env variable must be an integer')
                    continue

                mesg['functions'] += 1
                mesg[func_name] = {
                    'arn': func['FunctionArn'],
                    'response': [],
                    'status': 'ok'
                }

                mesg[func_name]['whipping'] = str(whipping) + ' Lambdas',

                # now whipit good
                for i in range(whipping):
                    try:
                        response = ''
                        response = self.lbd.invoke(
                            FunctionName=func_name,
                            InvocationType='Event',
                            Payload='{"whipit": "good"}')
                        self.check_status(response['StatusCode'])
                        mesg[func_name]['response'].append(response)
                    except Exception as e:
                        mesg['status'] = 'failed'
                        mesg[func_name]['status'] = 'failed'
                        mesg[func_name]['response'].append('Failed: ' + str(e))
                        pass

        return mesg


    def check_status(self, status):
        if status != 202:
            raise Exception('Execution failed - did not return 202')
