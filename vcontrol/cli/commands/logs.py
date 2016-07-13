import requests

class LogsCommandC:
    def logs(self, args, daemon):
        r = requests.get(daemon + "/get_logs/"+args.machine)
        return r.text

