import boto3,json

messageGroupId = 'nso-group'
queueURL= 'https://us-west-2.queue.amazonaws.com/486637738594/nsoqueue.fifo'

def lambda_handler(event, context):
    client = boto3.client('sqs')
    response = client.send_message(QueueUrl=queueURL, MessageBody=json.dumps(event),MessageGroupId=messageGroupId)
