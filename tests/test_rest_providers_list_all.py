from os import remove

from vcontrol.rest.providers.list_all import ListProvidersR
UNSUCCESSFUL_GET_PROVIDERS_MESSAGE = "unable to get providers"
PROVIDERS_FILE_PATH = '../vcontrol/rest/providers/providers.txt'


def test_successful_get_providers():
    """ tests if the ListProvidersR gets the providers successfully """
    list_providers = ListProvidersR()

    # create file
    with open(PROVIDERS_FILE_PATH, 'w') as f:
        f.write('TEST : TEST')

    assert list_providers.GET() == {'TEST ': 'TEST'}

    # delete file
    remove(PROVIDERS_FILE_PATH)


def test_unsuccessful_get_providers():
    list_providers = ListProvidersR()

    # create file
    with open(PROVIDERS_FILE_PATH, 'w') as f:
        f.write('TEST TEST')  # invalid because there is no ':' in the file

    assert list_providers.GET() == UNSUCCESSFUL_GET_PROVIDERS_MESSAGE

    # delete file
    remove(PROVIDERS_FILE_PATH)
    