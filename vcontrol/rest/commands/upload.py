from ..helpers import get_allowed

import web

class UploadCommandR:
    """
    This endpoint is for getting uploading a file to a Vent machine to be
    processed.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        # TODO
        return 1
