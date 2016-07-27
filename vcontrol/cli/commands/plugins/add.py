import json
import requests

class AddPluginCommandC:
    def add(self, args, daemon):
        """
        add plugin repository to Vent machine
        """
        payload = {}
        payload['url'] = args.url
        payload['machine'] = args.machine
        r = requests.post(daemon+"/commands/plugin/add", data=json.dumps(payload))
        return r.text
