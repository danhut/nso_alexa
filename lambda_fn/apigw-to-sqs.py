import boto3,json

def lambda_handler(event, context):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='nso_queue')
    response = queue.send_message(MessageBody=json.dumps(event))
