import boto3


class Sts:
    def __init__(self, role_arn=None):
        self.role_arn = role_arn
        self.aws_access_key_id = None
        self.aws_secret_access_key = None
        self.aws_session_token = None

    def get_account_id(self):
        sts = boto3.client('sts')
        return sts.get_caller_identity()['Account']

    def assume_role(self):
        '''assume a different (remote) role than the one we are currently running in'''
        sts = boto3.client('sts')
        account = sts.assume_role(
            RoleArn=self.role_arn,
            RoleSessionName="AwAwsSession"
        )
        self.aws_access_key_id = account['Credentials']['AccessKeyId']
        self.aws_secret_access_key = account['Credentials']['SecretAccessKey']
        self.aws_session_token = account['Credentials']['SessionToken']

