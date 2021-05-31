import os
import unittest

import TestUtil
from oauthclient.credentialutil import Credentialutil
from oauthclient.model.model import Environment
from oauthclient.oauth2api import Oauth2api

app_scopes = ["https://api.ebay.com/oauth/api_scope", "https://api.ebay.com/oauth/api_scope/sell.inventory",
              "https://api.ebay.com/oauth/api_scope/sell.marketing",
              "https://api.ebay.com/oauth/api_scope/sell.account",
              "https://api.ebay.com/oauth/api_scope/sell.fulfillment"]


class TestGetApplicationCredential(unittest.TestCase):
    def test_generate_authorization_url(self):
        app_config_path = os.path.join(os.path.split(__file__)[0], 'config', 'ebay-config-sample-user.yaml')
        Credentialutil.load(app_config_path)
        oauth2api_inst = Oauth2api()
        signin_url = oauth2api_inst.generate_user_authorization_url(Environment.SANDBOX, app_scopes)
        self.assertIsNotNone(signin_url)
        print('\n *** test_get_signin_url ***: \n', signin_url)

    def test_exchange_authorization_code(self):
        app_config_path = os.path.join(os.path.split(__file__)[0], 'config', 'ebay-config-sample-user.yaml')
        Credentialutil.load(app_config_path)
        oauth2api_inst = Oauth2api()
        signin_url = oauth2api_inst.generate_user_authorization_url(Environment.SANDBOX, app_scopes)
        code = TestUtil.get_authorization_code(signin_url)
        user_token = oauth2api_inst.exchange_code_for_access_token(Environment.SANDBOX, code)
        self.assertIsNotNone(user_token.access_token)
        self.assertTrue(len(user_token.access_token) > 0)
        print('\n *** test_get_user_access_token ***:\n', user_token)

    def test_exchange_refresh_for_access_token(self):
        app_config_path = os.path.join(os.path.split(__file__)[0], 'config', 'ebay-config-sample-user.yaml')
        Credentialutil.load(app_config_path)
        oauth2api_inst = Oauth2api()
        signin_url = oauth2api_inst.generate_user_authorization_url(Environment.SANDBOX, app_scopes)
        code = TestUtil.get_authorization_code(signin_url)
        user_token = oauth2api_inst.exchange_code_for_access_token(Environment.SANDBOX, code)
        self.assertIsNotNone(user_token.refresh_token)
        self.assertTrue(len(user_token.refresh_token) > 0)

        user_token = oauth2api_inst.get_access_token(Environment.SANDBOX, user_token.refresh_token, app_scopes)
        self.assertIsNotNone(user_token.access_token)
        self.assertTrue(len(user_token.access_token) > 0)

        print('\n *** test_refresh_user_access_token ***:\n', user_token)


if __name__ == '__main__':
    unittest.main()
