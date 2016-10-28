from ..helpers import get_allowed

import subprocess
import sys
import web

class StatsCommandR:
    """
    This endpoint is for getting stats about a Vent machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine, category, format):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        out = None
        try:
            if category == "all":
                if format:
                    # Get all, no-stream, as json
                    out = subprocess.check_output("/usr/local/bin/docker-machine ssh "+machine+" \"sh /data/info_tools/get_stats.sh -a -j -n\"", shell=True)
                else:
                    # Get all, no-stream, as regular output
                    out = subprocess.check_output("/usr/local/bin/docker-machine ssh "+machine+" \"sh /data/info_tools/get_stats.sh -a -n\"", shell=True)
            elif category == "running":
                if format:
                    # Get running containers, no-stream, as json
                    out = subprocess.check_output("/usr/local/bin/docker-machine ssh "+machine+" \"sh /data/info_tools/get_stats.sh -r -j -n\"", shell=True)
                else:
                    # Get running containers, no-stream, as regular output
                    out = subprocess.check_output("/usr/local/bin/docker-machine ssh "+machine+" \"sh /data/info_tools/get_stats.sh -r -n\"", shell=True)
            else:
                return "Invalid category. Categories are: 'all', 'running'."
        except Exception as e:
            print(sys.exc_info())
            out = "unable to retrieve container stats on "+machine
        return str(out)
