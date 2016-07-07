import os

def get_allowed():
    rest_url = ""
    if "ALLOW_ORIGIN" in os.environ:
        allow_origin = os.environ["ALLOW_ORIGIN"]
        host_port = allow_origin.split("//")[1]
        host = host_port.split(":")[0]
        port = str(int(host_port.split(":")[1])+1)
        rest_url = host+":"+port
    else:
        allow_origin = ""
    return allow_origin, rest_url
