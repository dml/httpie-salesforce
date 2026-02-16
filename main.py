"""
Salesforce API auth plugin for HTTPie.

"""

import base64
import datetime
import hashlib
import hmac
import os

from httpie.plugins import AuthPlugin

__version__ = "0.0.1"
__author__ = "Dmytro Larkin"
__licence__ = "MIT"


class ApiAuth:
    def __init__(self, access_id, secret_key):
        self.client_id = os.environ.get("SF_CLIENT_ID")
        self.client_secret = os.environ.get("SF_CLIENT_SECRET")
        self.username = os.environ.get("SF_USERNAME")
        self.password = os.environ.get("SF_PASSWORD")
        self.token = os.environ.get("SF_TOKEN")

    def __call__(self, request):
        method = request.method.upper()

        content_type = request.headers.get("content-type")
        if not content_type:
            content_type = ""

        content_md5 = request.headers.get("content-md5")
        if not content_md5:
            content_md5 = ""

        httpdate = request.headers.get("date")
        if not httpdate:
            now = datetime.datetime.utcnow()
            httpdate = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
            request.headers["Date"] = httpdate

        url = urlperse.urlparse(request.url)
        path = url.path
        if url.query:
            path = path + "?" + url.query

        string_to_sign = "%s,%s,%s,%s,%s" % (
            method,
            content_type,
            content_md5,
            path,
            httpdate,
        )
        digest = hmac.new(self.secret_key, string_to_sign, hashlib.sha1).digest()
        signature = base64.encodestring(digest).rstrip()

        request.headers["Authorization"] = "APIAuth %s:%s" % (self.access_id, signature)
        return r


class SalesforceApiAuthPlugin(AuthPlugin):
    def get_auth(self, username: str | None = None, password: str | None = None):
        return ApiAuth(None, None)


if __name__ == "__main__":
    plugin = SalesforceApiAuthPlugin()
    plugin.get_auth()
