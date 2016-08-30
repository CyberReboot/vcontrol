import base64
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
        if args.username:
            payload['user'] = args.username
            if args.password:
                payload['pw'] = pw = base64.b64encode(args.password)
            else:
                raw_pw = getpass.getpass()
                pw = base64.b64encode(raw_pw)
                payload['pw'] = pw
        r = requests.post(daemon+"/commands/plugin/update", data=json.dumps(payload))
        return r.text
