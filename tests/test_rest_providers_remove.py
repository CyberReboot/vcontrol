""" Test for the remove.py module in the vcontrol/rest/providers directory """
from os import remove as delete_file
from web import threadeddict

from vcontrol.rest.providers import remove

PROVIDERS_FILE_PATH = "../vcontrol/rest/providers/providers.txt"


class ContextDummy():
    env = threadeddict()
    env['HTTP_HOST'] = 'localhost:8080'


class WebDummy():
    # dummy class to emulate the web.ctx.env call in remove.py
    ctx = ContextDummy()


def test_successful_provider_removal():
    """ Here we give the module a text file with PROVIDER: written in it,
        it should remove that line in the file """
    remove_provider = remove.RemoveProviderR()
    remove.web = WebDummy()  # override the web variable in remove.py

    test_provider = "PROV"
    expected_providers_contents = ['What:\n', 'Test:']  # what we expect to see in providers.txt after we call GET
    # create the file
    with open(PROVIDERS_FILE_PATH, 'w') as f:
        f.writelines([
            "What:",
            "\n",
            test_provider + ":",
            "\n",
            "Test:"
        ])

    assert remove_provider.GET(test_provider) == "removed " + test_provider

    # read the file and see if it has removed the line with the test_provider
    with open(PROVIDERS_FILE_PATH, 'r') as f:
        provider_contents = f.readlines()

    delete_file(PROVIDERS_FILE_PATH)  # delete the file

    assert provider_contents == expected_providers_contents


def test_unsuccessful_provider_removal():
    """ Here we give the module a text file without the provider written in it,
        it should tell us that it couldn't find the provider we gave it as an argument"""
    remove_provider = remove.RemoveProviderR()
    remove.web = WebDummy()  # override the web variable in remove.py

    test_provider = "PROV"
    expected_providers_contents = ['What:\n', 'NOTPROV:\n', 'Test:']  # what we expect to see in providers.txt after GET

    # create the file
    with open(PROVIDERS_FILE_PATH, 'w') as f:
        f.writelines([
            "What:",
            "\n",
            "NOTPROV:",
            "\n",
            "Test:"
        ])

    assert remove_provider.GET(test_provider) == test_provider + " not found, couldn't remove"

    # read the file and see if it's the same
    with open(PROVIDERS_FILE_PATH, 'r') as f:
        provider_contents = f.readlines()

    delete_file(PROVIDERS_FILE_PATH)  # delete the file

    assert provider_contents == expected_providers_contents


