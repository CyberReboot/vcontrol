import requests

class ListProvidersC:
    def list_all(self, args, daemon):
        r = requests.get(daemon+"/list_providers")
        return r.text
