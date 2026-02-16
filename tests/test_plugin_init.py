import pytest

import httpie_salesforce_auth


@pytest.fixture
def plugin():
    return httpie_salesforce_auth.SalesforceAuthPlugin()


def test_init(plugin):
    assert plugin.name == "Salesforce REST API Auth"
    assert plugin.auth_type == "salesforce"
    assert plugin.description == (
        "Set a Salesforce REST API request token by executin OAuth 2.0 flow"
    )
    assert plugin.auth_require is False
    assert plugin.prompt_password is False


def test_get_auth(plugin):
    assert isinstance(plugin.get_auth(), httpie_salesforce_auth.PasswordFlow)
