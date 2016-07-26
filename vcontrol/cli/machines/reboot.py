import requests

class RebootMachineC:
    def reboot(self, args, daemon):
        r = requests.get(daemon+"/machines/reboot/"+args.machine)
        return r.text
