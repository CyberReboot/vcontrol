import requests

class BuildCommandC:
    def build(self, args, daemon):
        payload = {'no_cache':args.no_cache}
        r = requests.get(daemon+"/command_build/"+args.machine, params=payload)
        return r.text
