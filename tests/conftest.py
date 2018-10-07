# this is a configuration file for pytest

# we are keeping fixture definitions in the fixtures directory
# include them here to make them available to the test suite

pytest_plugins = [
    'tests.fixtures.support_dir'
]
