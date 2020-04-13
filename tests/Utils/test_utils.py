import os

from AwAws.Utils.env import Env


def test_env_init():
    os.environ['TEST_ENV'] = 'just a test'
    env = Env()
    assert env.env['TEST_ENV'] == 'just a test'
    os.environ.pop('TEST_ENV')


def test_env_get():
    os.environ['TEST_ENV'] = 'just a test'
    env = Env()
    assert env.get_env('TEST_ENV') == 'just a test'
    assert env.get_env('ENV_TEST') is None
    os.environ.pop('TEST_ENV')
