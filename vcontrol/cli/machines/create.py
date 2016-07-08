import json
import requests

class CreateMachineC:
    def create(self, args, daemon):
        """
        first ssh into the machine running vcontrol daemon
        from there use docker-machine to provision
        """
        payload = {}
        payload['machine'] = args.machine
        payload['provider'] = args.provider
        payload['cpus'] = args.cpus
        payload['disk_size'] = args.disk_size
        payload['iso'] = args.iso
        payload['memory'] = args.memory
        payload['group'] = args.group
        payload['labels'] = args.labels

        r = requests.post(daemon+"/create_machine", data=json.dumps(payload))
        return r.text
