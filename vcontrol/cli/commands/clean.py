import requests

class CleanCommandC:
    def clean(self, args, daemon):
        r = requests.get(daemon+"/commands/clean/"+args.machine+"/"+args.namespace)
        return r.text
