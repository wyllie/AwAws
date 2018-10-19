import os
# this is a configuration file for pytest

# pick up the test credentials file
root_dir = os.path.dirname(os.path.abspath(__file__))
creds_file = os.path.join(root_dir, 'etc/credentials')
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = creds_file


# we are keeping fixture definitions in the fixtures directory
# include them here to make them available to the test suite
pytest_plugins = [
    'tests.fixtures.support_dir'
]
