import requests

class StatsProviderC:
    def stats(self, args, daemon):
        r = requests.get(daemon+"/get_stats/"+args.provider)
        return r.text
