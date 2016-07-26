import requests

class StatusCommandC:
    def status(self, args, daemon):
        r = requests.get(daemon+"/command_status_plugin/"+args.machine+"/"+args.category)
        return r.text
