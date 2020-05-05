import io
import pytest
import zipfile

from botocore.stub import Stubber
from AwAws.Lambda.tools import LambdaTools

_lambda_region = 'us-west-2'

response_invoke = {
    'FunctionError': 'ok',
    'LogResult': 'ok',
    'Payload': 'some stuff',
    'StatusCode': 202
}

failed_response_invoke = {
    'FunctionError': 'ok',
    'LogResult': 'ok',
    'Payload': 'some stuff',
    'StatusCode': 503
}

expected_invoke = {
    'FunctionName': 'testFunction',
    'InvocationType': 'Event',
    'Payload': '{"whipit": "good"}'
}


def test_init():
    l_tools = LambdaTools(client='bob')
    assert l_tools.lbd == 'bob'


def test_whipit():
    response = create_functions(whipit='3')

    l_tools = LambdaTools()
    with Stubber(l_tools.lbd) as stubber:
        stubber.add_response('list_functions', response)
        stubber.add_response('invoke', response_invoke, expected_invoke)
        stubber.add_response('invoke', response_invoke, expected_invoke)
        stubber.add_response('invoke', response_invoke, expected_invoke)
        stubber.add_response('invoke', response_invoke, expected_invoke)
        results = l_tools.whipit()

    # there are two functions, but we just want to see the ones we work on
    assert results['functions'] == 1

    assert results['status'] == 'ok'
    assert results['testFunction']['arn'] == \
        'arn:aws:lambda:us-west-2:123456789012:function:testFunction:$LATEST'

    assert len(results['testFunction']['response']) == 3
    for res in results['testFunction']['response']:
        assert res['StatusCode'] == 202

    with pytest.raises(KeyError):
        results['testFunction2']


def test_whipit_no_functions():
    l_tools = LambdaTools()
    with pytest.raises(Exception, match=r'Could not get lambda function list'):
        l_tools.whipit()


def test_whipit_key_error():
    response = create_broken_functions(whipit='3')

    l_tools = LambdaTools()
    with Stubber(l_tools.lbd) as stubber:
        stubber.add_response('list_functions', response)
        stubber.add_response('invoke', response_invoke, expected_invoke)
        stubber.add_response('invoke', response_invoke, expected_invoke)
        stubber.add_response('invoke', response_invoke, expected_invoke)
        stubber.add_response('invoke', response_invoke, expected_invoke)
        l_tools.whipit()


def test_whipit_function_error():
    response = create_functions(whipit='3')

    l_tools = LambdaTools()
    with Stubber(l_tools.lbd) as stubber:
        stubber.add_response('list_functions', response)
        stubber.add_response('invoke', failed_response_invoke, expected_invoke)
        stubber.add_response('invoke', failed_response_invoke, expected_invoke)
        message = l_tools.whipit()
        assert message['status'] == 'failed'


def test_whipit_env():
    response = create_functions(whipit='hello')


    l_tools = LambdaTools()
    with Stubber(l_tools.lbd) as stubber:
        stubber.add_response('list_functions', response)
        results = l_tools.whipit()

    assert results['status'] == 'failed'
    assert results['errors'][0] == 'testFunction WHIPIT env variable must be an integer'


def create_functions(whipit):
    response = {
        "Functions": [
            {
                "FunctionArn":
                    'arn:aws:lambda:us-west-2:123456789012:function:testFunction:$LATEST',
                "FunctionName": 'testFunction',
                "Runtime": 'python3.6',
                "Role": 'test-iam-role',
                "Handler": 'lambda_function.lambda_handler',
                "Description": 'test lambda function',
                "Timeout": 3,
                "MemorySize": 128,
                "Environment": {
                    "Variables": {"WHIPIT": whipit}
                }
            },
            {
                "FunctionArn": 'arn::::::*',
                "FunctionName": 'testFunction2',
                "Runtime": 'python3.6',
                "Role": 'test-iam-role',
                "Handler": 'lambda_function.lambda_handler',
                "Description": 'test lambda function',
                "Timeout": 3,
                "MemorySize": 128,
            }
        ]
    }
    return response


def create_broken_functions(whipit):
    response = {
        "Functions": [
            {
                "FunctionArn":
                    'arn:aws:lambda:us-west-2:123456789012:function:testFunction:$LATEST',
                "FunctionName": 'testFunction',
                "Runtime": 'python3.6',
                "Role": 'test-iam-role',
                "Handler": 'lambda_function.lambda_handler',
                "Description": 'test lambda function',
                "Timeout": 3,
                "MemorySize": 128,
                "Environment": {
                    "Variables": {"NOT_WHIPIT": whipit}
                }
            }
        ]
    }
    return response


def get_test_zip_file1():
    pfunc = """
        def lambda_handler(event, context):
            return event
    """
    return _process_lambda(pfunc)


def _process_lambda(func_str):
    zip_output = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED)
    zip_file.writestr('lambda_function.py', func_str)
    zip_file.close()
    zip_output.seek(0)
    return zip_output.read()
