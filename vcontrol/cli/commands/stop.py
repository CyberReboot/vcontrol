import requests

class StopCommandC:
    def stop(self, args, daemon):
        r = requests.get(daemon+"/commands/stop/"+args.machine+"/"+args.containers)
        return r.text
