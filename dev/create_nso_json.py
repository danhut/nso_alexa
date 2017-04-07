import json
from jinja2 import Environment, FileSystemLoader

env = Environment(loader = FileSystemLoader('templates'))

env.filters['jsonify'] = json.dumps

template = env.get_template('nso_template.json')

config = {
    'name': 'myvpn',
    'id1': 'link1',
    'id2': 'link2',
	'device1': 'PE1',
    'device2': 'PE2',
    'interface1': '0/0/0/0',
    'interface2': '0/0/0/0'
}
payload = json.dumps(template.render(config=config))
print payload
