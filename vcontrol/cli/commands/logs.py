import requests

class LogsCommandC:
    def logs(self, args, daemon):
        r = requests.get(daemon + "/commands/logs/"+args.machine)
        return r.text

