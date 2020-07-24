
from AwAws.Session.session import Session


class SQS():
    def __init__(self, region_name=None, role_arn=None):
        self.sqs_url = None
        self.sqs = Session(region_name, role_arn).get_client('sqs')
        self.messages = []

    def queue_url(self, qname):
        'given the queue name, get the associated URL'
        if qname:
            try:
                self.sqs_url = self.sqs.get_queue_url(
                    QueueName=qname
                )['QueueUrl']
            except Exception as e:
                raise Exception('Could not find SQS Queue', e)

        return self.sqs_url

    def send_to_sqs(self, message):
        'send a message to a queue'
        response = self.sqs.send_message(
            QueueUrl=self.sqs_url,
            MessageBody=message
        )
        return response


    def send_to_sqs_fifo(self, message, dedup_id, group_id='standard'):
        'send a message to a FIFO queue'
        response = self.sqs.send_message(
            QueueUrl=self.sqs_url,
            MessageBody=message,
            MessageDeduplicationId=dedup_id,
            MessageGroupId=group_id
        )
        return response

    def read_from_sqs(self, waittime=1):
        'set a waittime to enable long polling'
        max_messages = 1

        response = self.sqs.receive_message(
            QueueUrl=self.sqs_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=waittime
        )

        status = None
        if 'Messages' in response:
            status = len(response['Messages'])
            for msg in response['Messages']:
                self.messages.append(RequestQueueItem(msg))

        return status

    def remove_from_sqs(self, receipt_handle):
        'remove a message from a queue'
        response = self.sqs.delete_message(
            QueueUrl=self.sqs_url,
            ReceiptHandle=receipt_handle
        )
        return response


class RequestQueueItem(object):
    def __init__(self, attribs):
        self.body = attribs['Body']
        self.receipt_handle = attribs['ReceiptHandle']
        self.message_id = attribs['MessageId']
        self.receive_count = int(attribs['Attributes']['ApproximateReceiveCount'])
