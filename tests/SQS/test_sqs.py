import inspect

from botocore.stub import Stubber
from AwAws.SQS.sqs import SQS

# some handy constants
sqs_test_queue = 'SQSTestQueue'


def test_init():
    sqs = SQS()
    assert sqs.sqs_url is None
    inspect.isclass(SQS)
    assert isinstance(sqs, SQS)


# def test_queue_url():


### @mock_sqs
### def test_send_message():
###     create_test_queue()
###
###     request_queue = RequestQueue(qname=SQS_TEST_QUEUE, region='us-east-1')
###     chk = request_queue.send_to_sqs(message='this is a test')
###     print('CHECK', chk)
###     assert chk['ResponseMetadata']['HTTPStatusCode'] == 200
###
###
### @mock_sqs
### def test_receive_message():
###     create_test_queue()
###
###     request_queue = RequestQueue(qname=SQS_TEST_QUEUE, region='us-east-1')
###     request_queue.send_to_sqs(message='zero this is a test')
###     request_queue.send_to_sqs(message='one this is a test')
###     request_queue.send_to_sqs(message='two this is a test')
###     request_queue.send_to_sqs(message='three this is a test')
###
###     # now set up a second RequestQueue Object and query the queue
###     new_queue = RequestQueue(qname=SQS_TEST_QUEUE, region='us-east-1')
###     status = new_queue.read_from_sqs(num_msg=4)
###
###     assert status == 4
###     assert new_queue.messages[3].body == 'three this is a test'
###
###
### @mock_sqs
### def test_receive_message_count():
###     create_test_queue()
###
###     request_queue = RequestQueue(qname=SQS_TEST_QUEUE, region='us-east-1')
###     request_queue.send_to_sqs(message='zero this is a test')
###     request_queue.send_to_sqs(message='one this is a test')
###     request_queue.send_to_sqs(message='two this is a test')
###     request_queue.send_to_sqs(message='three this is a test')
###
###     # now set up a second RequestQueue Object and query the queue
###     new_queue = RequestQueue(qname=SQS_TEST_QUEUE, region='us-east-1')
###     status = new_queue.read_from_sqs(num_msg=1)
###
###     assert status == 1
###     assert new_queue.messages[0].body == 'zero this is a test'
###     assert new_queue.messages[0].receive_count == 1
###
###
### @mock_sqs
### def test_receive_from_empty_queue():
###     create_test_queue()
###
###     request_queue = RequestQueue(qname=SQS_TEST_QUEUE, waittime=2, region='us-east-1')
###     msg = request_queue.read_from_sqs()
###
###     assert msg is None
###
###
### @mock_sqs
### def test_delete_message():
###     create_test_queue()
###
###     # create a message and send it to the queue
###     request_queue = RequestQueue(qname=SQS_TEST_QUEUE, region='us-east-1')
###     request_queue.send_to_sqs(message='this is a test')
###
###     # read the message from the queue
###     new_queue = RequestQueue(qname=SQS_TEST_QUEUE, region='us-east-1')
###     msg = new_queue.read_from_sqs()
###
###     assert msg is not None
###     assert new_queue.messages[0].body == 'this is a test'
###     receipt = new_queue.messages[0].receipt_handle
###
###     res = new_queue.remove_from_sqs(receipt)
###     assert res['ResponseMetadata']['HTTPStatusCode'] == 200
###
###
