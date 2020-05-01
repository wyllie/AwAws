import io
import json
import pytest

from botocore.stub import Stubber
from AwAws.Storage.s3 import S3

# some handy constants
test_bucket_name = 'this_is_my_test_bucket'


def test_init():
    s3 = S3(region_name='us-least-4')
    assert s3.session.get_region() == 'us-least-4'
    assert str(type(s3.s3)) == "<class 'botocore.client.S3'>"


def test_init_w_client():
    s3 = S3(client='client_obj', region_name='us-least-4')
    assert s3.session.get_region() == 'us-least-4'
    assert s3.s3 == 'client_obj'


def test_set_bucket_name_missing():
    s3 = S3(region_name='us-least-4')
    with Stubber(s3.s3) as stubber:
        stubber.add_client_error('head_bucket')
        with pytest.raises(Exception, match=r'.* this_is_my_test_bucket not available .*'):
            s3.set_bucket_name(test_bucket_name)


def test_set_bucket_name():
    expected_params = {"Bucket": test_bucket_name}

    s3 = S3(region_name='us-least-4')
    with Stubber(s3.s3) as stubber:
        stubber.add_response('head_bucket', '', expected_params)
        assert s3.set_bucket_name(test_bucket_name)
        assert s3.bucket_name == 'this_is_my_test_bucket'


def test_key_name():
    s3 = S3(region_name='us-least-4')
    with pytest.raises(TypeError):
        s3.set_key_name()

    s3.set_key_name('this_is_my_test_key')
    assert s3.key_name == 'this_is_my_test_key'


def test_put_data_object():
    data_object = {"hello": "this is some stuff"}
    response = {
        'Expiration': 'string',
        'ETag': 'hello',
        'ServerSideEncryption': 'AES256',
        'VersionId': 'string',
        'SSECustomerAlgorithm': 'string',
        'SSECustomerKeyMD5': 'string',
        'SSEKMSKeyId': 'string',
        'RequestCharged': 'requester'
    }
    expected_params = {
        'Body': json.dumps(data_object),
        'Bucket': test_bucket_name,
        'Key': 'this_is_my_test_key'
    }

    s3 = S3(region_name='us-least-4')

    with Stubber(s3.s3) as stubber:
        stubber.add_response('head_bucket', '', {'Bucket': test_bucket_name})
        stubber.add_response('put_object', response, expected_params)
        s3.set_bucket_name(test_bucket_name)
        s3.set_key_name('this_is_my_test_key')
        check = s3.put_data_object(data_object)

        assert check['ETag'] == 'hello'


def test_put_data_object_fail():
    data_object = {"hello": "this is some stuff"}
    expected_params = {
        'Body': json.dumps(data_object),
        'Bucket': test_bucket_name,
        'Key': 'this_is_my_test_key'
    }

    s3 = S3(region_name='us-least-4')
    with Stubber(s3.s3) as stubber:
        stubber.add_response('head_bucket', '', {'Bucket': test_bucket_name})
        stubber.add_client_error('put_object', expected_params=expected_params,
                                 response_meta=None,
                                 service_message='Msg from S3')
        with pytest.raises(Exception, match=r'Error saving to S3:.*?Msg from S3'):
            s3.set_bucket_name(test_bucket_name)
            s3.set_key_name('this_is_my_test_key')
            s3.put_data_object(data_object)


def test_put_file_object(datadir):
    response = {
        'Expiration': 'string',
        'ETag': 'hello',
        'ServerSideEncryption': 'AES256',
        'VersionId': 'string',
        'SSECustomerAlgorithm': 'string',
        'SSECustomerKeyMD5': 'string',
        'SSEKMSKeyId': 'string',
        'RequestCharged': 'requester'
    }

    with open(datadir.join('python-logo.png'), 'rb') as f:
        img_data = f.read()

    expected_params = {
        'Body': img_data,
        'Bucket': test_bucket_name,
        'Key': 'this_is_my_test_key'
    }

    s3 = S3(region_name='us-least-4')

    with Stubber(s3.s3) as stubber:
        stubber.add_response('head_bucket', '', {'Bucket': test_bucket_name})
        stubber.add_response('put_object', response, expected_params)
        s3.set_bucket_name(test_bucket_name)
        s3.set_key_name('this_is_my_test_key')
        check = s3.put_file_object(img_data)

        assert check['ETag'] == 'hello'


def test_put_file_object_fail(datadir):
    with open(datadir.join('python-logo.png'), 'rb') as f:
        img_data = f.read()

    expected_params = {
        'Body': img_data,
        'Bucket': test_bucket_name,
        'Key': 'this_is_my_test_key'
    }

    s3 = S3(region_name='us-least-4')
    with Stubber(s3.s3) as stubber:
        stubber.add_response('head_bucket', '', {'Bucket': test_bucket_name})
        stubber.add_client_error('put_object', expected_params=expected_params,
                                 response_meta=None,
                                 service_message='Msg from S3')
        with pytest.raises(Exception, match=r'Error saving to S3:.*?Msg from S3'):
            s3.set_bucket_name(test_bucket_name)
            s3.set_key_name('this_is_my_test_key')
            s3.put_file_object(img_data)


def test_get_data_object():
    data_object = {"hello": "this is some stuff"}
    expected_params = {
        'Bucket': test_bucket_name,
        'Key': 'this_is_my_test_key'
    }
    response = {
        'Body': json.dumps(data_object)
    }

    s3 = S3(region_name='us-least-4')

    with Stubber(s3.s3) as stubber:
        stubber.add_response('head_bucket', '', {'Bucket': test_bucket_name})
        stubber.add_response('get_object', response, expected_params)
        s3.set_bucket_name(test_bucket_name)
        s3.set_key_name('this_is_my_test_key')
        data_obj = s3.get_data_object()
        assert data_obj['hello'] == 'this is some stuff'


def test_get_data_object_fail():
    expected_params = {
        'Bucket': test_bucket_name,
        'Key': 'this_is_my_test_key'
    }

    s3 = S3(region_name='us-least-4')

    with Stubber(s3.s3) as stubber:
        stubber.add_response('head_bucket', '', {'Bucket': test_bucket_name})
        stubber.add_client_error('get_object', expected_params=expected_params,
                                 response_meta=None,
                                 service_message='Msg from S3')
        with pytest.raises(Exception, match=r'Error reading from S3:.*?Msg from S3'):
            s3.set_bucket_name(test_bucket_name)
            s3.set_key_name('this_is_my_test_key')
            s3.get_data_object()


def test_get_file_object(datadir):
    expected_params = {
        'Bucket': test_bucket_name,
        'Key': 'this_is_my_test_key'
    }

    with open(datadir.join('python-logo.png'), 'rb') as f:
        img_data = f.read()

    response = {'Body': img_data}

    s3 = S3(region_name='us-least-4')

    with Stubber(s3.s3) as stubber:
        stubber.add_response('head_bucket', '', {'Bucket': test_bucket_name})
        stubber.add_response('get_object', response, expected_params)
        s3.set_bucket_name(test_bucket_name)
        s3.set_key_name('this_is_my_test_key')
        data_obj = s3.get_file_object()
        assert data_obj == img_data


def test_get_file_object_fail():
    expected_params = {
        'Bucket': test_bucket_name,
        'Key': 'this_is_my_test_key'
    }

    s3 = S3(region_name='us-least-4')

    with Stubber(s3.s3) as stubber:
        stubber.add_response('head_bucket', '', {'Bucket': test_bucket_name})
        stubber.add_client_error('get_object', expected_params=expected_params,
                                 response_meta=None,
                                 service_message='Msg from S3')
        with pytest.raises(Exception, match=r'Error reading from S3:.*?Msg from S3'):
            s3.set_bucket_name(test_bucket_name)
            s3.set_key_name('this_is_my_test_key')
            s3.get_file_object()


def test_get_file_stream_object(datadir):
    expected_params = {
        'Bucket': test_bucket_name,
        'Key': 'this_is_my_test_key'
    }

    with open(datadir.join('python-logo.png'), 'rb') as f:
        img_data = f.read()

    response = {'Body': io.BytesIO(img_data)}

    s3 = S3(region_name='us-least-4')

    with Stubber(s3.s3) as stubber:
        stubber.add_response('head_bucket', '', {'Bucket': test_bucket_name})
        stubber.add_response('get_object', response, expected_params)
        s3.set_bucket_name(test_bucket_name)
        s3.set_key_name('this_is_my_test_key')
        data_obj = s3.get_streaming_file_object()
        assert data_obj == img_data


def test_get_file_stream_object_fail():
    expected_params = {
        'Bucket': test_bucket_name,
        'Key': 'this_is_my_test_key'
    }

    s3 = S3(region_name='us-least-4')

    with Stubber(s3.s3) as stubber:
        stubber.add_response('head_bucket', '', {'Bucket': test_bucket_name})
        stubber.add_client_error('get_object', expected_params=expected_params,
                                 response_meta=None,
                                 service_message='Msg from S3')
        with pytest.raises(Exception, match=r'Error reading from S3:.*?Msg from S3'):
            s3.set_bucket_name(test_bucket_name)
            s3.set_key_name('this_is_my_test_key')
            s3.get_streaming_file_object()


