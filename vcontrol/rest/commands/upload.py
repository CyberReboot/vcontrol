from ..helpers import get_allowed

import os
import subprocess
import web

class UploadCommandR:
    """
    This endpoint is for getting uploading a file to a Vent machine to be
    processed.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def OPTIONS(self, machine):
        return self.POST(machine)

    def POST(self, machine):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        # TODO how does this work with swagger?
        x = web.input(myfile={})
        filedir = '/tmp/files/'+machine # change this to the directory you want to store the file in.
        try:
            if not os.path.exists(filedir):
                os.makedirs(filedir)
            if 'myfile' in x: # to check if the file-object is created
                filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
                filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
                fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
                fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
                fout.close() # closes the file, upload complete.
                # copy file to vent instance
                cmd = "docker-machine scp "+filedir+"/"+filename+" "+machine+":/files/"
                output = subprocess.check_output(cmd, shell=True)
                # remove file from vcontrol-daemon
                output = subprocess.check_output("rm -f "+filedir+"/"+filename, shell=True)
                return "successfully uploaded", filename, "to", str(machine)
        except Exception as e:
            return "failed to upload to", str(machine), str(e)
        return "failed to upload to", str(machine)
