import json
import requests

class GenericCommandC:
    def generic(self, args, daemon):
        payload = {'command':args.command}
        r = requests.post(daemon+"/commands/generic/"+args.machine, data=json.dumps(payload))
        return r.text
