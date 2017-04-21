import logging, json, requests, yaml, boto3
from jinja2 import Template
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

try:
    f = open('config.yaml', 'r')
except:
    raise

config = yaml.safe_load(f)
apigw_url, apigw_key = config['apigw_url'],config['apigw_key']

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# Get Jinja2 template from DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('nso')
response = table.get_item(Key={'doc_id':'1'})
item = response['Item']['template']
template = Template(json.dumps(item))

# SQS Queue Config
messageGroupId = 'nso-group'
queueURL= 'https://us-west-2.queue.amazonaws.com/486637738594/nsoqueue.fifo'

DEVICES = ["PE1", "PE2", "PE3"]
devices = ", ".join(DEVICES)
INTERFACES = ["GIGABIT 0", "GIGABIT 1"]
interfaces = ", ".join(INTERFACES)


def generate_nso_json():
    config = {
        'name': 'bronze',
        'id1': 'link1',
        'id2': 'link2',
    	'device1': 'pe1',
        'device2': 'pe1',
        'interface1': 'gigabit 0/0/0/0',
        'interface2': 'gigabit 0/0/0/0'
    }
    nso_json = template.render(config=config)
    nso_json = json.dumps(nso_json)
    return nso_json

def send_to_apigw(nso_json):
    url = apigw_url
    headers = {
    'authorization': apigw_key,
    'content-type': "application/json",
    'cache-control': "no-cache"}
    response = requests.request("POST", url, data=nso_json, headers=headers)
    # move print to logger
    print response.text

nso_flow = generate_nso_json()
print (nso_flow)
send_to_apigw(nso_flow)

if __name__ == '__main__':
    app.run(debug=False)
