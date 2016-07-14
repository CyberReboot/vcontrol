import requests

class CleanCommandC:
    def clean(self, args, daemon):
        r = requests.get(daemon+"/command_clean/"+args.machine+"/"+args.namespace)
        return r.text
