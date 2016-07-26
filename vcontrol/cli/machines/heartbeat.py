import requests

class HeartbeatMachinesC:
    def heartbeat(self, args, daemon):
        r = requests.get(daemon+"/machines/heartbeat")
        return r.text

