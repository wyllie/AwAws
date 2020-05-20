import inspect
from mock import patch
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


@patch('AwAws.Session.sts.Sts.get_account_id')
def test_get_account_id(sts):
    sts.return_value = '123451234598'
    sts = Sts()
    assert sts.get_account_id() == '123451234598'

