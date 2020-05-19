import boto3


class Sts():
    def __init__(self, role_arn=None):
        self.accounts = {}
        self.master_account = None
        self.org_root = None
        self.org_unit = None
        self.org_units = {}
        self.role = role_arn
        self.sts = boto3.client('sts')


    def get_account_id(self):
        return self.sts.get_caller_identity()['Account']


    def assume_role(self):
        '''assume a different (remote) role than the one we are currently running in'''
        account = self.sts.assume_role(
            RoleArn=self.set_role_arn,
            RoleSessionName="AwAwsSession"
        )
        return account['Credentials']
