import requests

class UnregisterMachineC:
    def unregister(self, args, daemon):
        r = requests.get(daemon+"/machines/unregister/"+args.machine)
        return r.text
