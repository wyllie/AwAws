import inspect
import pytest

from botocore.stub import Stubber
from AwAws.SQS.sqs import SQS

# some handy constants
sqs_test_queue = 'SQSTestQueue'


def test_init():
    sqs = SQS(region_name='us-least-4')
    assert sqs.sqs_url is None
    assert len(sqs.messages) == 0
    inspect.isclass(SQS)
    assert isinstance(sqs, SQS)


def test_queue_url():
    sqs = SQS(region_name='us-least-5')
    with Stubber(sqs.sqs) as stubber:
        stubber.add_response('get_queue_url', {'QueueUrl': 'https://hello.there/something'})
        sqs.queue_url('test_queue_name')

        assert sqs.sqs_url == 'https://hello.there/something'


def test_queue_url_error():
    sqs = SQS(region_name='us-least-5')
    with Stubber(sqs.sqs) as stubber:
        stubber.add_response('get_queue_url', {'QueueUrl': 'nada'}, {'QueueName': 'hello'})

        with pytest.raises(Exception, match=r'Could not find SQS Queue'):
            sqs.queue_url('test_queue_name')


def test_send_to_sqs():
    sqs = SQS(region_name='us-least-6')
    with Stubber(sqs.sqs) as stubber:
        stubber.add_response('get_queue_url', {'QueueUrl': 'https://hello.there/something'})
        stubber.add_response('send_message', {'MessageId': '1'})

        sqs.queue_url('test_queue_name')
        check = sqs.send_to_sqs('some stuff')
        assert check['MessageId'] == '1'


def test_send_to_sqs_fifo():
    sqs = SQS(region_name='us-least-6')
    with Stubber(sqs.sqs) as stubber:
        stubber.add_response('get_queue_url', {'QueueUrl': 'https://hello.there/something'})
        stubber.add_response('send_message', {'MessageId': '1'})

        sqs.queue_url('test_queue_name')
        check = sqs.send_to_sqs_fifo('some stuff', '12345', group_id='hello')
        assert check['MessageId'] == '1'


def test_read_from_sqs():
    msg_response = {
        'Body': 'This is the message we sent',
        'ReceiptHandle': 'your receipt, thank you',
        'MessageId': 'MessageId is not a number',
        'Attributes': {'ApproximateReceiveCount': '1'}
    }
    sqs = SQS(region_name='us-least-6')
    with Stubber(sqs.sqs) as stubber:
        stubber.add_response('get_queue_url', {'QueueUrl': 'https://hello.there/something'})
        stubber.add_response('receive_message', {'Messages': [msg_response]})

        sqs.queue_url('test_queue_name')
        sqs.read_from_sqs()
        assert len(sqs.messages) == 1
        assert sqs.messages[0].body == 'This is the message we sent'
        assert sqs.messages[0].receipt_handle == 'your receipt, thank you'
        assert sqs.messages[0].message_id == 'MessageId is not a number'
        assert sqs.messages[0].receive_count == 1


def test_remove_from_sqs():
    sqs = SQS(region_name='us-least-6')
    with Stubber(sqs.sqs) as stubber:
        stubber.add_response('get_queue_url', {'QueueUrl': 'https://hello.there/something'})
        stubber.add_response('delete_message', {})

        sqs.queue_url('test_queue_name')
        sqs.remove_from_sqs('some_handle')
