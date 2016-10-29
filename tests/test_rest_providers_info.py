from vcontrol.rest.providers.info import InfoProviderR

UNSUCCESSFUL_INFO_PROVIDERS_MESSAGE =  "unable to get provider info"

# TODO: Test provider ID set for foo for now. The method is unimplemented. This needs to be fixed when the method is implemented
TEST_PROVIDER_ID = "foo"


def test_successful_get_provider_info():
    """ tests if the InfoProvidersR gets the providers successfully """
    info_providers = InfoProviderR()

    assert info_providers.GET(TEST_PROVIDER_ID) != UNSUCCESSFUL_INFO_PROVIDERS_MESSAGE
