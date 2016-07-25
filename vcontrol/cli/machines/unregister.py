import requests

class UnregisterMachineC:
    def unregister(self, args, daemon):
        r = requests.get(daemon+"/unregister_machine/"+args.machine)
        return r.text
