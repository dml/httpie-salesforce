"""
Salesforce API auth plugin for HTTPie.

"""

import importlib.metadata
import os
import sys

import requests
from httpie.plugins import AuthPlugin

__version__ = importlib.metadata.version("httpie-salesforce")
__author__ = "Dmytro Larkin"
__licence__ = "BSD"

SANDBOX_LOGIN_URL = "https://test.salesforce.com/services/oauth2/token"
PRODUCTION_LOGIN_URL = "https://login.salesforce.com/services/oauth2/token"


class BaseFlow:
    @property
    def url(self):
        if os.environ.get("SF_TEST") is not None:
            return SANDBOX_LOGIN_URL

        return PRODUCTION_LOGIN_URL


class PasswordFlow(BaseFlow):
    def __init__(self):
        self.client_id = os.environ.get("SF_CLIENT_ID")
        self.client_secret = os.environ.get("SF_CLIENT_SECRET")
        self.username = os.environ.get("SF_USERNAME")
        self.password = os.environ.get("SF_PASSWORD")
        self.token = os.environ.get("SF_TOKEN")

    def __call__(self, request):
        response = requests.post(self.url, data=self.payload).json()
        access_token = response.get("access_token")
        request.headers.update({"Authorization": "Bearer %s" % access_token})

        return request

    @property
    def payload(self):
        return {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": f"{self.password}{self.token}",
        }


class SalesforceAuthPlugin(AuthPlugin):
    """Plugin registration"""

    name = "Salesforce REST API Auth"
    auth_type = "salesforce"
    description = "Set a Salesforce REST API request token by executin OAuth 2.0 flow"
    auth_require = False
    prompt_password = False

    def get_auth(self, username: str | None = None, password: str | None = None):
        return PasswordFlow()


if __name__ == "__main__" and len(sys.argv) == 2:
    session = requests.Session()
    auth = PasswordFlow()
    request = auth(session).get(sys.argv[1])

    print(request.url)
    print(request.headers)
    print(request.json())
