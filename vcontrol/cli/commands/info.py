import requests

class InfoCommandC:
    def info(self, args, daemon):
        r = requests.get(daemon+"/commands/info/"+args.machine)
        return r.text
