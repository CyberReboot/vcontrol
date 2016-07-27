import json
import os
import requests

class DownloadCommandC:
    def download(self, args, daemon):
        payload = {}
        payload['machine'] = args.machine
        payload['template'] = args.template
        # !! TODO probably need to check that the response succeeded
        r = requests.post(daemon+"/commands/download", stream=True, data=json.dumps(payload))
        filedir = '/tmp/templates/'+args.machine
        try:
            if not os.path.exists(filedir):
                os.makedirs(filedir)
            with open(filedir+"/"+args.template, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        except Exception as e:
            return "failed to download", args.template
        return "successfully downloaded", args.template, "to", filedir
