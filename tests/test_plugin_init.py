import httpie_salesforce_auth


def test_init():
    plugin = httpie_salesforce_auth.SalesforceAuthPlugin()

    assert plugin.name == "Salesforce REST API Auth"
    assert plugin.auth_type == "salesforce"
    assert plugin.description == (
        "Set a Salesforce REST API request token by executin OAuth 2.0 flow"
    )
    assert plugin.auth_require is False
    assert plugin.prompt_password is False
