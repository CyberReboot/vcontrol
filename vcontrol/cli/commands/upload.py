import requests

class UploadCommandC:
    def upload(self, args, daemon):
        files = {'myfile': open(args.path, 'rb')}
        # !! TODO how do files work with swagger?
        r = requests.post(daemon+"/commands/upload/"+args.machine, files=files)
        return r.text
