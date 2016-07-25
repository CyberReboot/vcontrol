import json
import requests

class RemovePluginCommandC:
    def remove(self, args, daemon):
        """
    	remove plugin repository from Vent machine
    	"""
    	payload = {}
    	payload['url'] = args.url
    	payload['machine'] = args.machine
        r = requests.post(daemon+"/command_remove_plugin", data=json.dumps(payload))
        return r.text
