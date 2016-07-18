from ..helpers import get_allowed
from ..helpers import json_yield

import ast
import json
import os
import subprocess
import uuid
import web

class CreateMachineR:
    """
    This endpoint is for creating a new machine of Vent on a provider.
    """
    allow_origin, rest_url = get_allowed.get_allowed()

    INDEX_HTML = """
    <html>
    <head>
    <script src="http://code.jquery.com/jquery-3.1.0.min.js"></script>
    <script>
    $(function() {

      function update() {
        $.getJSON('/v1/create/%s/%s', {}, function(data) {
          if (data.state != 'done') {
    """
    INDEX_HTML_TYPE_A = """
            $('#status').append($('<div>'+data.content+'</div>'));
    """
    INDEX_HTML_TYPE_B = """
            $('#status').text(data.content);
    """
    INDEX_HTML_END = """
            setTimeout(update, 0);
          }
        });
      }

      update();
    });
    </script>
    </head>
    <body>
    <div id="status">Creating machine, please wait...</div>
    </body>
    </html>
    """

    def OPTIONS(self):
        return self.POST()

    def POST(self):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        web.header('Access-Control-Allow-Headers', "Content-type")
        data = web.data()
        payload = {}
        try:
            payload = ast.literal_eval(data)
            if type(payload) != dict:
                payload = ast.literal_eval(json.loads(data))
        except:
            return "malformed json body"

        # TODO add --engine-label(s) vent specific labels
        engine_labels = "--engine-label vcontrol_managed=yes "
        try:
            if os.path.isfile('providers.txt'):
                with open('providers.txt', 'r') as f:
                    for line in f:
                        if line.split(":")[0] == payload['provider']:
                            # add --engine-label for group specified in payload
                            if "group" in payload:
                                engine_labels += "--engine-label vcontrol_group="+payload["group"]+" "
                            # !! TODO add any additional --engine-label(s) in payload
                            if "labels" in payload:
                                if payload["labels"] != "":
                                    labels = payload["labels"].split(",")
                                    for label in labels:
                                        engine_labels += "--engine-label "+label+" "
                            proc = None
                            cleanup = False
                            if line.split(":")[1] == 'openstack' or line.split(":")[1] == 'vmwarevsphere':
                                # TODO check usage stats first and make sure it's not over the limits (capacity)
                                cmd = "/usr/local/bin/docker-machine create "+engine_labels+"-d "+line.split(":")[1]+" "+line.split(":")[5].strip()
                                if line.split(":")[1] == 'vmwarevsphere':
                                    if payload['iso'] == '/tmp/vent/vent.iso':
                                        cmd += ' --vmwarevsphere-boot2docker-url=https://github.com/CyberReboot/vent/releases/download/v0.1.1/vent.iso'
                                    else:
                                        cmd += ' --vmwarevsphere-boot2docker-url='+payload['iso']
                            elif line.split(":")[1].strip() == "virtualbox":
                                cmd = "/usr/local/bin/docker-machine create "+engine_labels+"-d "+line.split(":")[1].strip()
                                if payload['iso'] == '/tmp/vent/vent.iso':
                                    if not os.path.isfile('/tmp/vent/vent.iso'): 
                                        cleanup = True
                                        os.system("git config --global http.sslVerify false")
                                        os.system("cd /tmp && git clone --recursive https://github.com/CyberReboot/vent.git")
                                        os.system("cd /tmp/vent && make")
                                    proc = subprocess.Popen(["nohup", "python", "-m", "SimpleHTTPServer"], cwd="/tmp/vent")
                                    cmd += ' --virtualbox-boot2docker-url=http://localhost:8000/vent.iso'
                                cmd += ' --virtualbox-cpu-count "'+str(payload['cpus'])+'" --virtualbox-disk-size "'+str(payload['disk_size'])+'" --virtualbox-memory "'+str(payload['memory'])+'"'
                            else:
                                cmd = "/usr/local/bin/docker-machine create "+engine_labels+"-d "+line.split(":")[1]+" "+line.split(":")[2].strip()
                            if line.split(":")[1] == "vmwarevsphere":
                                cmd += ' --vmwarevsphere-cpu-count "'+str(payload['cpus'])+'" --vmwarevsphere-disk-size "'+str(payload['disk_size'])+'" --vmwarevsphere-memory-size "'+str(payload['memory'])+'"'
                            cmd += ' '+payload['machine']
                            output = subprocess.check_output(cmd, shell=True)
                            if proc != None:
                                os.system("kill -9 "+str(proc.pid))
                            if cleanup:
                                shutil.rmtree('/tmp/vent')
                            return output
                return "provider specified was not found"
            else:
                return "no providers, please first add a provider"
        except:
            return "unable to create machine"
