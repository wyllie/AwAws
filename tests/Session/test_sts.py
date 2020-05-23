import datetime
import inspect

from botocore.stub import Stubber
from AwAws.Session.sts import Sts

test_role_arn = 'arn:aws:iam::111111111:role/net.dilex.some.test.role'


def test_init():
    sts = Sts(role_arn=test_role_arn)
    inspect.isclass(Sts)
    assert isinstance(sts, Sts)
    assert sts.role_arn == test_role_arn
    assert sts.aws_access_key_id is None
    assert sts.aws_secret_access_key is None
    assert sts.aws_session_token is None


def test_get_account_id():
    response = {
        'Account': '123451234598',
        'Arn': 'arn:aws:iam::123456789012:user/BillyBob',
        'UserId': 'AKIAI44QH8DHBEXAMPLE',
    }
    sts = Sts()
    with Stubber(sts.sts) as sts_stub:
        sts_stub.add_response('get_caller_identity', response, {})
        assert sts.get_account_id() == '123451234598'


def test_assume_role():
    params = {
        'RoleArn': test_role_arn,
        'RoleSessionName': 'AwAwsSession'
    }
    response = {
        'AssumedRoleUser': {
            'Arn': 'arn:aws:sts::123456789012:assumed-role/demo/Bob',
            'AssumedRoleId': 'ARO123EXAMPLE123:Bob',
        },
        'Credentials': {
            'AccessKeyId': 'AKIAIOSFODNN7EXAMPLE',
            'Expiration': datetime.datetime(2011, 7, 15, 23, 28, 33),
            'SecretAccessKey': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYzEXAMPLEKEY',
            'SessionToken': 'AQoDYXdzEPT//////////wEXAMPLEtc764bNrC9SAPBS',
        },
        'PackedPolicySize': 6,
        'ResponseMetadata': {
            '...': '...',
        }
    }

    sts = Sts(role_arn=test_role_arn)
    with Stubber(sts.sts) as sts_stub:
        sts_stub.add_response('assume_role', response, params)
        sts.assume_role()
        assert sts.aws_access_key_id == 'AKIAIOSFODNN7EXAMPLE'
        assert sts.aws_secret_access_key == 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYzEXAMPLEKEY'
        assert sts.aws_session_token == 'AQoDYXdzEPT//////////wEXAMPLEtc764bNrC9SAPBS'

