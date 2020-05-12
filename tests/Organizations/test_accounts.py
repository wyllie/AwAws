import os
import pytest

from botocore.stub import Stubber
from unittest.mock import patch
from AwAws.Organizations.accounts import Accounts

mock_acc = 'AwAws.Organizations.accounts.Accounts'


@pytest.fixture
def env():
    os.environ['AW_MASTER'] = '987659876512'

    yield
    os.environ.pop('AW_MASTER')


def test_init():
    accounts = Accounts()
    assert accounts.master_account is None
    assert accounts.org_root is None
    assert accounts.org_unit is None
    assert accounts.org_units == {}
    assert accounts.accounts == {}
    assert str(type(accounts.org)) == "<class 'botocore.client.Organizations'>"


@patch('AwAws.Session.sts.Sts.get_account_id')
def test_list_accounts(sts, env):
    sts.return_value = '111'
    response = {
        'Accounts': [
            {
                'Id': '123451234598',
                'Arn': 'string',
                'Email': 'string',
                'Name': 'Billy-Bob',
                'Status': 'ACTIVE',
                'JoinedMethod': 'CREATED',
            },
        ],
    }
    accounts = Accounts()
    with Stubber(accounts.org) as stub_org:
        stub_org.add_response('list_accounts', response, {})
        accounts.list_accounts()
        assert accounts.accounts['123451234598']['Name'] == 'Billy-Bob'
        assert accounts.accounts['123451234598']['Status'] == 'ACTIVE'


def test_list_account_fail():
    accounts = Accounts()
    with pytest.raises(Exception, match=r'Could not establish account root'):
        accounts.list_accounts()


@patch(mock_acc + '._set_root', autospec=True, return_value=None)
def test_list_ous(set_root):
    response = {
        'OrganizationalUnits': [
            {
                'Id': 'r-orga-somestuff',
                'Arn': 'arn::stuff',
                'Name': 'Org Unit A'
            },
        ],
        'NextToken': 'string'
    }
    accounts = Accounts()
    accounts.org_root = 'r-rootid'
    with Stubber(accounts.org) as stubber:
        stubber.add_response('list_organizational_units_for_parent', response,
                             {'ParentId': 'r-rootid'})
        accounts.list_ous()
        assert accounts.org_units['Org Unit A']['Id'] == 'r-orga-somestuff'
        assert accounts.org_units['Org Unit A']['Arn'] == 'arn::stuff'
        set_root.assert_called_once()


@patch(mock_acc + '._set_root', autospec=True)
def test_list_ous_fail(set_root):
    accounts = Accounts()
    set_root.side_effect = Exception()
    with pytest.raises(Exception, match=r'Unable to find organization root'):
        accounts.list_ous()
        set_root.assert_called_once()


@patch(mock_acc + '.list_accounts', autospec=True, return_value=None)
@patch(mock_acc + '.list_ous', autospec=True, return_value=None)
def test_list_ous_accounts(list_ous, list_accounts):
    response = {
        'Children': [
            {
                'Id': '987659876512',
                'Type': 'ACCOUNT'
            },
        ],
        'NextToken': 'string'
    }

    accounts = Accounts()
    accounts.org_root = 'r-rootid'
    accounts.org_units = {'DevSecOps42': {'Id': 'r-some-stuff'}}
    accounts.accounts['987659876512'] = {'Id': '987659876512', 'Name': 'The Cool Account'}

    with Stubber(accounts.org) as stubber:
        stubber.add_response('list_children', response,
                             {
                                 'ParentId': 'r-some-stuff',
                                 'ChildType': 'ACCOUNT'
                             })
        res = accounts.list_ou_accounts('DevSecOps42')
        print(res)
        assert res[0]['Id'] == '987659876512'
        assert res[0]['Name'] == 'The Cool Account'
        list_accounts.assert_called_once()
        list_ous.assert_called_once()


@patch(mock_acc + '.list_accounts', autospec=True, return_value=None)
@patch(mock_acc + '.list_ous', autospec=True, return_value=None)
def test_list_ous_accounts_fail(list_ous, list_accounts):
    accounts = Accounts()
    with pytest.raises(Exception, match=r"'Could not find OU:', 'Not the OU'"):
        accounts.list_ou_accounts('Not the OU')


@patch('AwAws.Session.sts.Sts.get_account_id')
def test_set_master_account(sts):
    sts.return_value = None
    accounts = Accounts()
    accounts._set_master_account(account_number='123451234512')
    assert accounts.master_account == '123451234512'


@patch('AwAws.Session.sts.Sts.get_account_id')
def test_set_master_account_env(sts, env):
    sts.return_value = None
    accounts = Accounts()
    accounts._set_master_account()
    assert accounts.master_account == '987659876512'


def test_set_master_account_fail():
    accounts = Accounts()
    with pytest.raises(Exception, match=r'Could not find master account info'):
        accounts._set_master_account()


def test_set_root():
    response = {
        'Roots': [
            {
                'Id': 'r-rootid',
                'Arn': 'string',
                'Name': 'string',
                'PolicyTypes': [
                    {
                        'Type': 'SERVICE_CONTROL_POLICY',
                        'Status': 'ENABLED'
                    },
                ]
            },
        ],
    }
    accounts = Accounts()
    with Stubber(accounts.org) as stubber:
        stubber.add_response('list_roots', response, {})
        accounts._set_root()
        assert accounts.org_root == 'r-rootid'
