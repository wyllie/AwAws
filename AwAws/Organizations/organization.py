from AwAws.Session.session import Session


class Organizations:
    def __init__(self, role_arn=None, region_name=None):
        self.org_id = None
        self.org_arn = None
        self.master_acct_arn = None
        self.master_acct_email = None
        self.master_acct_id = None
        self.org = Session(role_arn=role_arn, region_name=region_name).get_client('organizations')

    def get_organization_info(self):
        try:
            org_details = self.org.describe_organization()['Organization']
        except Exception as e:
            raise Exception('Could not get organization details', e)

        self.org_id = org_details['Id']
        self.org_arn = org_details['Arn']
        self.master_acct_arn = org_details['MasterAccountArn']
        self.master_acct_email = org_details['MasterAccountEmail']
        self.master_acct_id = org_details['MasterAccountId']

