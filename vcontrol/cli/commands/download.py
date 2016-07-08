import requests

class DownloadCommandC:
    def download(self, args, daemon):
        payload = {}
        payload['machine'] = args.machine
        payload['filename'] = args.filename
        r = requests.get(daemon+"/get_template", data=payload)
        return r.text
