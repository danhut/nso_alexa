#!/usr/bin/env python
import logging, json, requests, yaml
from jinja2 import Environment, FileSystemLoader
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

env = Environment(loader = FileSystemLoader('templates'))
env.filters['jsonify'] = json.dumps
template = env.get_template('nso_template.json')

DEVICES = ["PE1", "PE2", "PE3"]
devices = ", ".join(DEVICES)
INTERFACES = ["GIGABIT 0", "GIGABIT 1"]
interfaces = ", ".join(INTERFACES)

@ask.launch
def welcome():
    welcome_msg = render_template('welcome')
    return question(welcome_msg).reprompt("Are you ready to add a VPN?")

@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
@ask.intent('AMAZON.NoIntent')
def nogo():
    quit = render_template('stop')
    return statement(quit)

@ask.intent('YesIntent')
def vpn_name():
    return question(render_template('vpn_name')).reprompt("What name for the VPN?")

@ask.intent('getvpnname')
def getvpnname(vpn_name):
    if (vpn_name is None):
        return question(render_template('vpn_name')).reprompt("What name for the VPN?")
    vpn_name = vpn_name.replace(' ', '')
    session.attributes['vpn_name'] = vpn_name
    response = render_template('list_devices', devices=devices, site = 'first')
    return question(response).reprompt("Which device?")

@ask.intent('getfirstsite')
def getfirstsite(device):
    if (device is None):
        response = render_template('list_devices', devices=devices, site = 'first')
        return question(response).reprompt("Which device?")
    device = device.replace(' ', '')
    session.attributes['device1'] = device
    response = render_template('list_interfaces', device=device, interfaces=interfaces)
    return question(response).reprompt("Which interface?")

@ask.intent('getfirstinterface')
def getfirstint(interface):
    if (interface is None):
        # need to fix device here - not assigned
        response = render_template('list_interfaces', device=device, interfaces=interfaces)
        return question(response).reprompt("Which interface?")
    session.attributes['interface1'] = interface
    response = render_template('list_devices', devices=devices, site = 'second')
    return question(response).reprompt("Which device?")

@ask.intent('getsecondsite')
def getsecondsite(device):
    if (device is None):
        response = render_template('list_devices', devices=devices, site = 'second')
        return question(response).reprompt("Which device?")
    device = device.replace(' ', '')
    session.attributes['device2'] = device
    response = render_template('list_interfaces', device=device, interfaces=interfaces)
    return question(response).reprompt("Which interface?")

@ask.intent('getsecondinterface')
def getsecondint(interface):
    if (interface is None):
        # need to fix device here - not assigned
        response = render_template('list_interfaces', device=device, interfaces=interfaces)
        return question(response).reprompt("Which interface?")
    session.attributes['interface2'] = interface
    nso_json = generate_nso_json()
    nso_send = send_to_apigw(nso_json)
    msg = render_template('confirmation')
    return statement(msg)

def generate_nso_json():
    (int1_type,int1_number) = session.attributes['interface1'].split(" ")
    (int2_type,int2_number) = session.attributes['interface2'].split(" ")
    int1_number = '0/0/0/' + int1_number
    int2_number = '0/0/0/' + int2_number
    config = {
        'name': (session.attributes['vpn_name']),
        'id1': 'link1',
        'id2': 'link2',
    	'device1': session.attributes['device1'].lower(),
        'device2': session.attributes['device2'].lower(),
        'interface1': int1_number,
        'interface2': int2_number
    }
    nso_json = json.loads(template.render(config=config))
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
    print(response.text)

if __name__ == '__main__':
    app.run(debug=True,)
