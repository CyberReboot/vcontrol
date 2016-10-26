from vcontrol.rest.machines.shutdown import ShutdownMachineR
UNSUCCESSFUL_SHUTDOWN_MESSAGE = "unable to stop machine"

def test_create_machine_shutdown():
    """ tests the ShutdownMachineR class for proper shutting down"""
    test_machine = 'foo'
    shutdown_machine_r = ShutdownMachineR()

    assert shutdown_machine_r.GET(test_machine) == UNSUCCESSFUL_SHUTDOWN_MESSAGE
