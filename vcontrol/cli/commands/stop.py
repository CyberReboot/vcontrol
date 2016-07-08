import requests

class StopCommandC:
    def stop(self, args, daemon):
        r = requests.get(daemon+"/command_stop/"+args.machine+"/"+args.containers)
        return r.text
