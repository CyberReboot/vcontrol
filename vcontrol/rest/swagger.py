from helpers import get_allowed

import web

class SwaggerR:
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        web.header("Content-Type","text/yaml")
        try:
            with open("swagger.yaml", 'r') as f:
                filedata = f.read()
            newdata = filedata.replace("mydomain", self.rest_url)
            with open("swagger.yaml", 'w') as f:
                f.write(newdata)
            f = open("swagger.yaml", 'r')
        except:
            try:
                with open("../vcontrol/swagger.yaml", 'r') as f:
                    filedata = f.read()
                newdata = filedata.replace("mydomain", self.rest_url)
                with open("../vcontrol/swagger.yaml", 'w') as f:
                    f.write(newdata)
                f = open("../vcontrol/swagger.yaml", 'r')
            except:
                # using python path, don't allow write-back
                pass
        return f.read()
