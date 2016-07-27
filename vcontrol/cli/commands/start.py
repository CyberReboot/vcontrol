import requests

class StartCommandC:
    def start(self, args, daemon):
        r = requests.get(daemon+"/commands/start/"+args.machine+"/"+args.containers)
        return r.text

