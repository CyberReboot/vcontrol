import requests

class ListProvidersC:
    def list_all(self, args, daemon):
        r = requests.get(daemon+"/providers/list")
        return r.text
