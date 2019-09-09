import os
import pytest

from AwAws.Utils.env import Env


@pytest.fixture
def env():
    os.environ['BLARGH'] = 'hello!'

    yield
    try:
        os.environ.pop('BLARGH')
    except KeyError:
        pass


def test_init(env):
    env = Env()
    assert type(env) == Env
    assert env.env['BLARGH'] == 'hello!'


def test_get_env(env):
    env = Env()
    assert env.get_env('BLARGH') == 'hello!'
    assert env.get_env('HGRALB') is None


def test_set_env(env):
    env = Env()
    env.set_env('BLARGH', 'go away!!!')
    assert os.environ['BLARGH'] == 'go away!!!'


def test_set_env_unset(env):
    env = Env()
    env.set_env('BLARGH', None)
    with pytest.raises(KeyError):
        os.environ['BLARGH']


def test_set_env_unset_error(env):
    env = Env()
    env.set_env('HOWDY', None)
    with pytest.raises(KeyError):
        os.environ['HOWDY']
