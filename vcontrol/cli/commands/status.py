import requests

class StatusCommandC:
    def status(self, args, daemon):
        r = requests.get(daemon+"/commands/status/"+args.machine+"/"+args.category)
        return r.text
