from vcontrol.rest.machines.boot import BootMachineR

UNSUCCESSFUL_BOOT_MESSAGE = "unable to start machine"


def test_boot_machine_fail():
    """ tests the BootMachine class for improper booting"""
    test_machine = 'foo'
    shutdown_machine_r = BootMachineR()

    assert shutdown_machine_r.GET(test_machine) == UNSUCCESSFUL_BOOT_MESSAGE
