from __future__ import print_function

import ast
import requests

class BuildCommandC:
    def build(self, args, daemon):
        print("Building, please wait...")
        payload = {'no_cache':args.no_cache}
        r = requests.get(daemon+"/commands/build/"+args.machine+"/b", params=payload)
        key = ""
        for line in r.text.split("\n"):
            if "getJSON" in line:
                key = line.split("/")[-1].split("'")[0]
        partial = True
        while partial:
            r = requests.get(daemon+"/commands/build_output/"+args.machine+"/"+key)
            try:
                output = r.text
                if '"content": null,' in output:
                    output = output.replace('"content": null', '"content": "null"')
                if ast.literal_eval(output)['state'] == 'done':
                    partial = False
                else:
                    print(ast.literal_eval(output)['content'], end=' ')
            except Exception as e:
                print(e)
                partial = False
        return ""
