import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

DEVICES = ["PE1", "PE2", "CE1", "CE2"]
INTERFACES = ["GIGABIT 0", "GIGABIT 1", "GIGABIT 2", "GIGABIT 3"]
SESSION_SITEADEVICE = "devicea"
SESSION_SITEAINTERFACE = "interfacea"
SESSION_SITEBDEVICE = "deviceb"
SESSION_SITEBINTERFACE = "interfaceb"

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def welcome():
    welcome_msg = render_template('welcome')
    return question(welcome_msg).reprompt("Are you ready to add a VPN?")


@ask.intent("CreateVPN", default={'siteAdevice': 'Unknown', 'siteBdevice': 'Unknown'})
def dialog_create_vpn(siteAdevice,siteAinterface,siteBdevice,siteBinterface):
    if siteAdevice.upper() not in DEVICES:
        return available_devices()
        session.attributes[SESSION_SITEADEVICE] = siteAdevice
    #if siteAinterface.upper() not in INTERFACES:
    #    return available_interfaces('site one')
    #    session.attributes[SESSION_SITEAINTERFACE] = siteAinterface
    if siteBdevice.upper() not in DEVICES:
        return available_devices()
        session.attributes[SESSION_SITEBDEVICE] = siteBdevice
    #if siteBinterface.upper() not in INTERFACES:
#        return available_interfaces('site two')
#        session.attributes[SESSION_SITEBINTERFACE] = siteBinterface
    msg = render_template('confirmation', deviceA=siteAdevice, interfaceA=siteAinterface, deviceB=siteBdevice, interfaceB=siteBinterface)
    return statement(msg)

#@ask.intent("AvailableInterfaces")
#def available_interfaces(site):
#    interfaces = ", ".join(sorted(INTERFACES))
#    list_int_text = render_template('list_interfaces', interfaces=interfaces, site = site)
#    list_int_reprompt_text = render_template('list_int_reprompt')
#    return question(list_int_text).reprompt(list_int_reprompt_text)

@ask.intent("AvailableDevices")
def available_devices():
    devices = ", ".join(sorted(DEVICES))
    list_devices_text = render_template('list_devices', devices=devices)
    list_devices_reprompt_text = render_template('list_devices_reprompt')
    return question(list_devices_text).reprompt(list_devices_reprompt_text)

if __name__ == '__main__':
    app.run(debug=True,)
