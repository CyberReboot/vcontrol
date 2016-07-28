import base64
import getpass
import json
import os
import requests

class AddProviderC:
    def add(self, provider, args, daemon):
        """
        only privileged can add providers, which currently is only
        accessible from the server running the vcontrol daemon
        """
        open_d = os.environ.get('VCONTROL_OPEN')
        if open_d != "true":
            # daemon as passed in is: 'http:..../'+api_v
            # split and get the end and append
            api_v = daemon.split('/')[-1]
            daemon = 'http://localhost:8080/'+api_v
        if provider == "virtualbox":
            payload = {'name': args.name, 'provider': provider}
        elif provider == "vmwarevsphere":
            if not "--vmwarevsphere-password " in args.args:
                raw_pw = getpass.getpass()
                pw = base64.b64encode(raw_pw)
                args.args = args.args+" --vmwarevsphere-password "+pw
                payload = {'name': args.name, 'provider': provider, 'args': args.args}
            else:
                # assume there are no spaces in any args, 
                raw_pw = args.args.split("-password ")[1]
                pw = base64.b64encode(raw_pw)
                arguments = args.args.split(" ")
                for i in range(0,len(arguments)-1):
                    # checks if the argument is '--vmwarevsphere-password' and it is not the last argument
                    # removes the arguments and breaks from loop
                    if arguments[i] == "--vmwarevsphere-password" and (i+1) < len(arguments):
                        del arguments[i + 1]
                        del arguments[i]
                        break
                args.args = (" ").join(arguments)+" --vmwarevsphere-password "+pw
                payload = {'name': args.name, 'provider': provider, 'args': args.args}
        elif provider == "openstack":
            if not "--openstack-password " in args.args:
                raw_pw = getpass.getpass()
                pw = base64.b64encode(raw_pw)
                args.args = args.args+" --openstack-password "+pw
                payload = {'name': args.name, 'provider': provider, 'args': args.args}
            else:
                # assume there are no spaces in any args, 
                raw_pw = args.args.split("--openstack-password ")[1]
                pw = base64.b64encode(raw_pw)
                arguments = args.args.split(" ")
                for i in range(0,len(arguments)-1):
                    # checks if the argument is '--openstack-password' and it is not the last argument
                    # removes the arguments and breaks from loop
                    if arguments[i] == "--openstack-password" and (i+1) < len(arguments):
                        del arguments[i + 1]
                        del arguments[i]
                        break
                args.args = (" ").join(arguments)+" --openstack-password "+pw
                payload = {'name': args.name, 'provider': provider, 'args': args.args}

        else:
            raw_pw = args.args.split("-password ")[1]
            pw = base64.b64encode(raw_pw)
            args.args = (" ").join(args.args.split(" ")[:-1])+" "+pw
            payload = {'name': args.name, 'provider': provider, 'args': args.args}
        if provider == "openstack" or provider == "vmwarevsphere":
            payload['cpu'] = str(args.max_cpu_usage)
            payload['ram'] = str(args.max_ram_usage)
            payload['disk'] = str(args.max_disk_usage)
        r = requests.post(daemon+"/providers/add", data=json.dumps(payload))
        return r.text
