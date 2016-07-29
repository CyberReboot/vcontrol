from ..helpers import get_allowed
from ..helpers import json_yield

import subprocess
import uuid
import web

class CleanCommandR:
    """
    This endpoint is for cleaning all containers of a namespace on a Vent
    machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()

    INDEX_HTML = """
    <html>
    <head>
    <script src="http://code.jquery.com/jquery-3.1.0.min.js"></script>
    <script>
    $(function() {

      function update() {
        $.getJSON('/v1/commands/clean/%s/%s/%s', {}, function(data) {
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
    <div id="status">Cleaning, please wait...</div>
    </body>
    </html>
    """

    def GET(self, machine, category, o_type):
        web.header('Access-Control-Allow-Origin', self.allow_origin)

        client_session_id = uuid.uuid4().hex
        out = ""
        if o_type == 'a':
             out = self.INDEX_HTML%(machine, category, client_session_id) + \
                   self.INDEX_HTML_TYPE_A + \
                   self.INDEX_HTML_END
        elif o_type == 'b':
             out = self.INDEX_HTML%(machine, category, client_session_id) + \
                   self.INDEX_HTML_TYPE_B + \
                   self.INDEX_HTML_END
        return out

class CleanCommandOutputR:
    """
    This endpoint is for rendering the output of cleaning Docker containers on a machine in a particular category
    """
    json_yield = json_yield.json_yield_two
    json_yield._gen_dict = {}
    json_yield._fn_id = 0

    allow_origin, rest_url = get_allowed.get_allowed()
    @json_yield
    def GET(self, machine, category, key):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        cmd = "/usr/local/bin/docker-machine ssh "+machine+" \"python2.7 /data/template_parser.py "+category+" clean\""
        try:
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in iter(proc.stdout.readline, b''):
                yield line
            yield "\n\n-----\nFinished cleaning."
        except:
            pass
