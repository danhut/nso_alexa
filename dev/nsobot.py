import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

DEVICES = ["PE1", "PE2", "CE1", "CE2"]
INTERFACES = ["GIGABIT0", "GIGABIT1", "GIGABIT2", "GIGABIT3"]
SESSION_DEVICE = "device"
SESSION_INTERFACE = "interface"

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def welcome():
    welcome_msg = render_template('welcome')
    return question(welcome_msg).reprompt("Are you ready to add a VPN?")

@ask.intent("AvailableDevices")
def available_devices():
    devices = ", ".join(sorted(DEVICES))
    list_devices_text = render_template('list_devices', devices=devices)
    list_devices_reprompt_text = render_template('list_devices_reprompt')
    return question(list_devices_text).reprompt(list_devices_reprompt_text)

@ask.intent("AvailableInterfaces")
def available_interfaces():
    interfaces = ", ".join(sorted(INTERFACES))
    list_int_text = render_template('list_interfaces', interfaces=interfaces)
    list_int_reprompt_text = render_template('list_int_reprompt')
    return question(list_int_text).reprompt(list_int_reprompt_text)

@ask.intent("YesIntent")
def start_dialogue():
    dialog_create_vpn(devicename,interface)

@ask.intent("CreateVPN")
def dialog_create_vpn(devicename,interface):
    if devicename is not None:
        if devicename.upper() not in DEVICES:
            return available_devices()
        session.attributes[SESSION_DEVICE] = devicename
    if interface is not None:
        if interface.upper() not in INTERFACES:
            return available_interfaces()
        session.attributes[SESSION_INTERFACE] = interface
    msg = render_template('confirmation', device=devicename, interface=interface)
    return statement(msg)

if __name__ == '__main__':
    app.run(debug=True)
