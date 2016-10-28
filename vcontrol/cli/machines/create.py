from __future__ import print_function

import ast
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

        print("Creating machine, please wait...")
        r = requests.post(daemon+"/machines/create/b", data=json.dumps(payload))
        key = ""
        for line in r.text.split("\n"):
            if ".post" in line:
                key = line.split("/", 3)[-1].split("'")[0]
        partial = True
        while partial:
            r = requests.post(daemon+"/machines/create_output/"+key, data=json.dumps(payload))
            try:
                output = r.text
                if '"content": null,' in output:
                    output = output.replace('"content": null', '"content": "null"')
                if ast.literal_eval(output)['state'] == 'done':
                    partial = False
                else:
                    print(ast.literal_eval(output)['content'], end=' ')
            except Exception as e:
                print("Error:", e)
                partial = False
        return ""
