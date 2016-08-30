import base64
import getpass
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
        if args.username:
            payload['user'] = args.username
            if args.password:
                payload['pw'] = pw = base64.b64encode(args.password)
            else:
                raw_pw = getpass.getpass()
                pw = base64.b64encode(raw_pw)
                payload['pw'] = pw
        r = requests.post(daemon+"/commands/plugin/add", data=json.dumps(payload))
        return r.text
