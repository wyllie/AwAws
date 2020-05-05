import os
import pytest
import re
import sys

from AwAws.Lambda.base import Lambda


def test_init():
    base = Lambda()

    lib_path_name = os.path.dirname(os.path.realpath(__file__))
    p = re.compile('tests/Lambda')
    assert p.sub('AwAws/Lambda/lib', lib_path_name) in sys.path
    assert '/var/task/lib' in sys.path
    assert base.status == 'ok'


def test_do_something():
    base = Lambda()
    assert base.do_something() == 'ok'


def test_get_region():
    os.environ['AWS_REGION'] = 'us-4-least'
    base = Lambda()
    assert base.get_region() == 'us-4-least'
    os.environ.pop('AWS_REGION')


def test_get_aw_env():
    os.environ['AW_ENV'] = 'test_environment'
    base = Lambda()
    assert base.get_aw_env() == 'test_environment'
    os.environ.pop('AW_ENV')


def test_get_aw_account():
    os.environ['AW_ACCT'] = 'test_account'
    base = Lambda()
    assert base.get_aw_account() == 'test_account'
    os.environ.pop('AW_ACCT')


def test_get_env():
    os.environ['AW_OTHER'] = 'other_env_variable'
    base = Lambda()
    assert base.get_env('AW_OTHER') == 'other_env_variable'
    os.environ.pop('AW_OTHER')


def test_get_handler():
    function = Lambda.get_handler()
    assert function.__name__ == 'handler'
    assert function('whipit', None) == 'whipped'

    # if we call this function here we are going to error out
    # this is intentional as we should not be running handle from here,
    # in needs to be implemented in a class
    with pytest.raises(NotImplementedError):
        assert function([], None).__name__ == 'something'


def test_handle():
    with pytest.raises(NotImplementedError):
        base = Lambda()
        base.handle(None, None)

