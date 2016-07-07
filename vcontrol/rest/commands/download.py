from ..helpers import get_allowed

import web

class DownloadCommandR:
    """
    This endpoint is for retrieving the template file of an machine.
    """
    def GET(self):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        # !! TODO does this work with swagger?
        data = web.data()
        data = data.split("&")
        payload = {}
        for param in data:
            p = param.split("=")
            payload[p[0]] = p[1]
        print payload
        return 1
