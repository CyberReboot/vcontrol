import requests

class VersionC:
    def version(self, args, daemon):
        r = requests.get(daemon+"/version")
        return r.text
