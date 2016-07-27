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
        r = requests.post(daemon+"/commands/plugin/remove", data=json.dumps(payload))
        return r.text
