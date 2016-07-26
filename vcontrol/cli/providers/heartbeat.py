import requests

class HeartbeatProvidersC:
    def heartbeat(self, args, daemon):
        r = requests.get(daemon+"/providers/heartbeat")
        return r.text
