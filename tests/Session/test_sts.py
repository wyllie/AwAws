from mock import patch
from AwAws.Session.sts import Sts


def test_sts():
    sts = Sts()
    assert sts.master_account is None
    assert sts.org_root is None
    assert sts.org_unit is None
    assert sts.org_units == {}
    assert sts.accounts == {}
    assert str(type(sts.sts)) == "<class 'botocore.client.STS'>"


@patch('AwAws.Session.sts.Sts.get_account_id')
def test_get_account_id(sts):
    sts.return_value = '123451234598'
    sts = Sts()
    assert sts.get_account_id() == '123451234598'

