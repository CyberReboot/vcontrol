import requests

class StatsCommandC:
    def stats(self, args, daemon):
        r = requests.get(daemon+"/get_stats/"+args.machine)
        return r.text
