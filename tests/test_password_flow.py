import pytest

import httpie_salesforce_auth


@pytest.fixture
def flow():
    return httpie_salesforce_auth.PasswordFlow()


def test_url(flow):
    assert flow.url == "https://login.salesforce.com/services/oauth2/token"


def test_payload(flow):
    assert flow.payload == {
        "grant_type": "password",
        "client_id": "test-client-id",
        "client_secret": "test-client-secret",
        "username": "test-username",
        "password": "test-passwordtest-security-token",
    }
