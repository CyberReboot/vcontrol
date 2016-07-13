import requests

class DeregisterMachineC:
    def deregister(self, args, daemon):
        r = requests.get(daemon+"/deregister_machine/"+args.machine)
        return r.text
