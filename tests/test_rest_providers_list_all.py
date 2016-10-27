from vcontrol.rest.providers.list_all import ListProvidersR
UNSUCCESSFUL_GET_PROVIDERS_MESSAGE = "unable to get providers"


def test_successful_get_providers():
    """ tests if the ListProvidersR gets the providers successfully """
    list_providers = ListProvidersR()

    assert list_providers.GET() != UNSUCCESSFUL_GET_PROVIDERS_MESSAGE
