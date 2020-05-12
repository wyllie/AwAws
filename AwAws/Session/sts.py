from AwAws.Session.session import Session


class Sts():
    def __init__(self):
        self.master_account = None
        self.org_root = None
        self.org_unit = None
        self.org_units = {}
        self.accounts = {}
        self.sts = Session().get_client('sts')


    def get_account_id(self):
        return self.sts.get_caller_identity()['Account']
