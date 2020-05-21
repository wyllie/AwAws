
from AwAws.Session.session import Session
from AwAws.Session.sts import Sts
from AwAws.Utils.env import Env


class Accounts:
    def __init__(self, role_arn=None, region_name=None):
        self.master_account = None
        self.org_root = None
        self.org_unit = None
        self.org_units = {}
        self.accounts = {}
        self.org = Session(role_arn=role_arn, region_name=region_name).get_client('organizations')


    def list_accounts(self):
        'get a listing of all accounts - index by account id'
        try:
            self._set_master_account()
        except Exception as e:
            raise Exception('Could not establish account root', e)

        res = self.org.list_accounts()
        for acc in res['Accounts']:
            self.accounts[acc['Id']] = acc

        return self.accounts


    def list_ous(self):
        'get a list of top level organizational units (OUs)'
        try:
            self._set_root()
        except Exception as e:
            raise Exception('Unable to find organization root', e)

        res = self.org.list_organizational_units_for_parent(ParentId=self.org_root)
        for ou in res['OrganizationalUnits']:
            self.org_units[ou['Name']] = ou


    def list_ou_accounts(self, ou_name):
        'get a list of accounts for an organizational unit'
        try:
            self.list_accounts()
            self.list_ous()
            parent_id = self.org_units[ou_name]['Id']
            res = self.org.list_children(ParentId=parent_id,
                                         ChildType='ACCOUNT')
        except Exception as e:
            raise Exception('Could not find OU:', ou_name, e)

        accs = []
        for acc in res['Children']:
            accs.append(self.accounts[acc['Id']])

        return accs


    '''This works but I'm not sure how useful it is
       to have in here - probably better to just do
       this from the CLI or in the console'''
#    def create_account(self, account_name, account_email,
#                       account_role='OrganizationAccountAccessRole'):
#        'create a new account and assign it to an ou'
#
#        try:
#            res = self.org.create_account(Email=account_email,
#                                          AccountName=account_name,
#                                          RoleName=account_role)
#        except Exception as e:
#            raise Exception('Error initializing create account', e)
#
#        # Now we are going to hang out and wait for the account to
#        # be created - takes a few minutes...
#
#        request_id = res.get('CreateAccountStatus').get('Id')
#        print('Account creation started, request_id:', request_id)
#        status = 'IN_PROGRESS'
#        status_response = None
#        while status == 'IN_PROGRESS':
#            status_response = self.org.describe_create_account_status(
#                CreateAccountRequestId=request_id)
#            status = status_response.get('CreateAccountStatus').get('State')
#            print('Create account status', status)
#            time.sleep(10)
#
#        if status == 'SUCCEEDED':
#            acc_id = status_response.get('CreateAccountStatus').get('AccountId')
#            self.account_id = acc_id
#        else:
#            reason = status_response.get('CreateAccountStatus').get('FailureReason')
#            print('Account creation failed', reason)


    def _set_master_account(self, account_number=None):
        'set the AWS Organization master account number'
        try:
            env = Env()
            sts = Sts()
            acc_num = sts.get_account_id()
            self.master_account = acc_num or account_number or env.get_env('AW_MASTER')
        except Exception as e:
            raise Exception('Could not find master account info', e)

        if self.master_account is None:
            raise Exception('Master Account not set, check AW_MASTER')


    def _set_root(self):
        'get the root identifier for this account'

        # if org_root is not set, try setting it
        if self.org_root is None:
            res = self.org.list_roots()
            self.org_root = res['Roots'][0]['Id']
