import requests

class StatsCommandC:
    def stats(self, args, daemon):
        r = requests.get(daemon+"/commands/stats/"+args.machine+"/"+args.category+"/"+args.format)
        return r.text
