import requests

class HeartbeatProvidersC:
    def heartbeat(self, args, daemon):
        r = requests.get(daemon+"/heartbeat_providers")
        return r.text
