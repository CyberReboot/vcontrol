import requests

class HeartbeatMachinesC:
    def heartbeat(self, args, daemon):
        r = requests.get(daemon+"/heartbeat_machines")
        return r.text

