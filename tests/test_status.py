from vcontrol.cli.commands.status import StatusCommandC
import unittest
import requests.exceptions

class Arg():
    """ dummy class for testing"""
    machine = "foo"
    category = "bar"
    format = "foobar"


class TestCase(unittest.TestCase):
    def test_status_command_fail(self):
        """ test the status command to throw an exception on max entries with an invalid URL"""
        status_class = StatusCommandC()
        daemon = "http://localhost:8080"
        args = Arg()

        self.assertRaises(requests.exceptions.ConnectionError, status_class.status, args, daemon)