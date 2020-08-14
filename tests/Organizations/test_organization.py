import inspect

from botocore.stub import Stubber
from AwAws.Organizations.organization import Organizations


def test_init():
    org = Organizations()
    assert org.org_id is None
    assert org.org_arn is None
    assert org.master_acct_arn is None
    assert org.master_acct_email is None
    assert org.master_acct_id is None
    inspect.isclass(Organizations)
    assert isinstance(org, Organizations)


def test_get_org_info():
    response = {
        'Organization': {
            'Id': 'o-somestuff',
            'Arn': 'arn:some:string',
            'FeatureSet': 'ALL',
            'MasterAccountArn': 'arn:stuff',
            'MasterAccountId': 'id',
            'MasterAccountEmail': 'email@stuff',
            'AvailablePolicyTypes': []
        }
    }
    org = Organizations()

    with Stubber(org.org) as stub_org:
        stub_org.add_response('describe_organization', response)
        org.get_organization_info()
        assert org.org_id == 'o-somestuff'
        assert org.org_arn == 'arn:some:string'
        assert org.master_acct_arn == 'arn:stuff'
        assert org.master_acct_email == 'email@stuff'
        assert org.master_acct_id == 'id'

