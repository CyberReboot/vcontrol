import requests

class StatsProviderC:
    def stats(self, args, daemon):
        r = requests.get(daemon+"/providers/stats/"+args.provider)
        return r.text
