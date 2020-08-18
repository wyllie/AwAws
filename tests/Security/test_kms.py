import inspect
import pytest

from AwAws.Security.kms import KMS
from mock import patch


def test_init():
    kms = KMS(region_name='us-least-4')
    inspect.isclass(KMS)
    assert isinstance(kms, KMS)
    assert str(type(kms.kms)) == "<class 'botocore.client.KMS'>"
    assert len(kms.enc_regions) == 0
    assert len(kms.master_keys) == 0


def test_set_encryption_regions():
    kms = KMS(region_name='us-least-4')
    t_regions = 'us-jest-5'
    kms.set_encryption_regions(t_regions)
    assert len(kms.enc_regions) == 1
    assert kms.enc_regions == [t_regions]
    assert type(kms.enc_regions) == list


def test_set_encryption_multi_regions():
    kms = KMS(region_name='us-least-4')
    t_regions = ['us-least-4', 'us-jest-5']
    kms.set_encryption_regions(t_regions)
    assert len(kms.enc_regions) == len(t_regions)
    assert sorted(kms.enc_regions) == sorted(t_regions)
    assert type(kms.enc_regions) == list


def test_set_master_keys():
    kms = KMS(region_name='us-least-4')
    t_keys = 'arn:single_region:key'
    kms.set_master_keys(t_keys)
    assert len(kms.master_keys) == 1
    assert kms.master_keys == [t_keys]
    assert type(kms.master_keys) == list


def test_set_master_multi_keys():
    kms = KMS(region_name='us-least-4')
    t_keys = ['arn:east_region:key', 'arn:west_region:key']
    kms.set_master_keys(t_keys)
    assert len(kms.master_keys) == len(t_keys)
    assert sorted(kms.master_keys) == sorted(t_keys)
    assert type(kms.master_keys) == list


def test_set_key_provider_error():
    kms = KMS(region_name='us-least-4')
    with pytest.raises(Exception, match=r'Region or Master Keys not set'):
        kms.set_key_provider()


@patch('aws_encryption_sdk.KMSMasterKeyProvider', autospec=True)
def test_set_key_provider_error2(aes):
    aes.side_effect = Exception()

    kms = KMS(region_name='us-least-4')
    kms.set_encryption_regions('us-least-4')
    kms.set_master_keys('arn:now:I:am:the:master')
    with pytest.raises(Exception, match=r'Could not set key_provider'):
        kms.set_key_provider()


@patch('aws_encryption_sdk.KMSMasterKeyProvider', autospec=True)
def test_set_key_provider(aes):
    aes.return_value = 'something'

    kms = KMS(region_name='us-least-4')
    kms.set_encryption_regions('us-least-4')
    kms.set_master_keys('arn:now:I:am:the:master')
    kms.set_key_provider()

    assert kms.key_provider == 'something'


@patch('aws_encryption_sdk.KMSMasterKeyProvider', autospec=True)
@patch('aws_encryption_sdk.encrypt', autospec=True)
def test_encrypt(aes, key):

    aes.return_value = ('encrypted_text_la_la_la', 'encrypted_header_x')
    key.return_value = 'something'

    kms = KMS(region_name='us-least-4')
    kms.set_encryption_regions('us-least-4')
    kms.set_master_keys('arn:now:I:am:the:master')
    kms.set_master_keys()
    result = kms.encrypt_it('stuff to encrypt')
    assert result['cipher_text'] == 'encrypted_text_la_la_la'
    assert result['encryptor_header'] == 'encrypted_header_x'


@patch('aws_encryption_sdk.KMSMasterKeyProvider', autospec=True)
@patch('aws_encryption_sdk.encrypt', autospec=True)
def test_encrypt_object(aes, key):

    aes.return_value = ('encrypted_text_la_la_la', 'encrypted_header_x')
    key.return_value = 'something'

    kms = KMS(region_name='us-least-4')
    kms.set_encryption_regions('us-least-4')
    kms.set_master_keys('arn:now:I:am:the:master')
    kms.set_master_keys()

    test_obj = {
        'this': 'is a test',
        'with': ['a', 'list', 'of', 'items'],
        'and': {
            'some': 'nested info'
        }
    }
    result = kms.encrypt_object(test_obj)
    assert result['cipher_text'] == 'encrypted_text_la_la_la'
    assert result['encryptor_header'] == 'encrypted_header_x'


@patch('aws_encryption_sdk.KMSMasterKeyProvider', autospec=True)
@patch('aws_encryption_sdk.encrypt', autospec=True)
@patch('json.dumps', autospec=True)
def test_encrypt_broken_object(jsn, aes, key):

    jsn.side_effect = Exception()
    aes.return_value = ('encrypted_text_la_la_la', 'encrypted_header_x')
    key.return_value = 'something'

    kms = KMS(region_name='us-least-4')
    kms.set_encryption_regions('us-least-4')
    kms.set_master_keys('arn:now:I:am:the:master')
    kms.set_master_keys()

    test_obj = {
        'this': 'is a test',
        'with': ['a', 'list', 'of', 'items'],
        'and': {
            'some': 'nested info'
        }
    }

    with pytest.raises(Exception, match='Could not serialize object'):
        kms.encrypt_object(test_obj)


@patch('aws_encryption_sdk.KMSMasterKeyProvider', autospec=True)
@patch('aws_encryption_sdk.decrypt', autospec=True)
def test_decrypt(aes, key):

    aes.return_value = ('plain_text_ok', 'some_header_stuff_from_encryptor')
    key.return_value = 'something'

    kms = KMS(region_name='us-least-4')
    kms.set_encryption_regions('us-least-4')
    kms.set_master_keys('arn:now:I:am:the:master')
    kms.set_master_keys()

    cipher_object = {
        'cipher_text': 'encrypted_text_la_la_la',
        'encryptor_header': 'some_header_stuff_from_encryptor'
    }
    result = kms.decrypt_it(cipher_object)
    assert result == 'plain_text_ok'


@patch('aws_encryption_sdk.KMSMasterKeyProvider', autospec=True)
@patch('aws_encryption_sdk.decrypt', autospec=True)
def test_decrypt_object(aes, key):

    aes.return_value = (b'{"this": "is a test", "with": ["a", "list", "of", \
                        "items"], "and": { "some": "nested info"}}',
                        'some_header_stuff_from_encryptor')
    key.return_value = {
        'this': 'is a test',
        'with': ['a', 'list', 'of', 'items'],
        'and': {
            'some': 'nested info'
        }
    }

    kms = KMS(region_name='us-least-4')
    kms.set_encryption_regions('us-least-4')
    kms.set_master_keys('arn:now:I:am:the:master')
    kms.set_master_keys()

    cipher_object = {
        'cipher_text': 'encrypted_text_la_la_la',
        'encryptor_header': 'some_header_stuff_from_encryptor'
    }
    result = kms.decrypt_object(cipher_object)
    assert result == {
        'this': 'is a test',
        'with': ['a', 'list', 'of', 'items'],
        'and': {
            'some': 'nested info'
        }
    }


@patch('aws_encryption_sdk.KMSMasterKeyProvider', autospec=True)
@patch('aws_encryption_sdk.decrypt', autospec=True)
def test_decrypt_bad_header(aes, key):

    aes.return_value = ('plain_text_ok', 'wrong_header_stuff_from_encryptor')
    key.return_value = 'something'

    kms = KMS(region_name='us-least-4')
    kms.set_encryption_regions('us-least-4')
    kms.set_master_keys('arn:now:I:am:the:master')
    kms.set_master_keys()

    cipher_object = {
        'cipher_text': 'encrypted_text_la_la_la',
        'encryptor_header': 'some_header_stuff_from_encryptor'
    }
    with pytest.raises(Exception, match='Encryption headers do not match!!!'):
        kms.decrypt_it(cipher_object)

