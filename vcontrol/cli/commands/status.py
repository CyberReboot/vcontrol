import requests

class StatusCommandC:
    def status(self, args, daemon):
        print ""
        r = requests.get(daemon+"/command_status_plugin/"+args.machine)
        return r.text
