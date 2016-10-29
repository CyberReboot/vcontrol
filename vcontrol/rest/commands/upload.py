from ..helpers import get_allowed

import os
import subprocess
import web


def create_directory(file_directory):
    """ checks if the directory exists and if it doesn't - it creates it"""
    if not os.path.exists(file_directory):
        os.makedirs(file_directory)


def write_new_file(file_object, file_directory, file_name):
    file_out = open(file_directory + '/' + file_name, 'w')  # creates the file where the uploaded file should be stored
    file_out.write(file_object.myfile.file.read())  # writes the uploaded file to the newly created file.
    file_out.close()  # closes the file, upload complete.


class UploadCommandR:
    """
    This endpoint is for getting uploading a file to a Vent machine to be
    processed.
    """
    allow_origin, rest_url = get_allowed.get_allowed()

    def OPTIONS(self, machine):
        return self.POST(machine)

    def POST(self, machine):
        try:
            web.header('Access-Control-Allow-Origin', self.allow_origin)
        except Exception as e:
            print(e.message)
        # TODO how does this work with swagger?
        fileobj = web.input(myfile={})
        filedir = '/tmp/files/' + machine  # change this to the directory you want to store the file in.
        try:
            create_directory(file_directory=filedir)
            if 'myfile' in fileobj:  # to check if the file-object is created
                # replaces the windows-style slashes with linux ones
                filepath = fileobj.myfile.filename.replace('\\', '/')
                # splits the and chooses the last part (the filename with extension)
                filename = filepath.split('/')[-1]
                write_new_file(fileobj, filedir, filename)
                # copy file to vent instance
                cmd = "docker-machine scp " + filedir + "/" + filename + " " + machine + ":/files/"
                subprocess.check_output(cmd, shell=True)
                # remove file from vcontrol-daemon
                subprocess.check_output("rm -f " + filedir + "/" + filename, shell=True)
                return "successfully uploaded", filename, "to", str(machine)
        except Exception as e:
            return "failed to upload to", str(machine), str(e)
        return "failed to upload to", str(machine)
