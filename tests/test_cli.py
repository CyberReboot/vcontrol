from vcontrol.cli.commands import info

class Args():
    """ test class to create mock args object """
    def __init__(self):
        self.machine = "foo"

def test_info_command_c():
    """ tests the InfoCommandC class """
    c_inst = info.InfoCommandC()
    args = Args()
    result = c_inst.info(args, "http://localhost:8080")
    assert result == "not found"
