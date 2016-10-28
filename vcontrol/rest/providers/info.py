from ..helpers import get_allowed

import web

class InfoProviderR:
    """
    This endpoint is for getting info about a provider.
    """
    def GET(self, machine):
        """ GET HTTP Request """
        try:       
            web.header('Access-Control-Allow-Origin', self.allow_origin)
        except Exception as e:
            print(e.message)
        try:
            # TODO
            return "not implemented yet"
        except:
            return "unable to get provider info"
