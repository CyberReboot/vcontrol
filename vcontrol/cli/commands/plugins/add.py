import json
import requests

class AddPluginCommandC:
    def add(self, args, daemon):
    	"""
    	add plugin to machine
    	"""
    	payload = {}
    	payload['url'] = args.url
    	payload['machine'] = args.machine
        r = requests.post(daemon+"/command_add_plugin", data=json.dumps(payload))
        return r.text
