import json
import requests

class UpdatePluginCommandC:
    def update(self, args, daemon):
        """
    	update plugin repository on Vent
    	"""
    	payload = {}
    	payload['url'] = args.url
    	payload['machine'] = args.machine
        r = requests.post(daemon+"/command_update_plugin", data=json.dumps(payload))
        return r.text
