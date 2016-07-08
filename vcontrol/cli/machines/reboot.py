import requests

class RebootMachineC:
    def reboot(self, args, daemon):
        r = requests.get(daemon+"/command_reboot/"+args.machine)
        return r.text
