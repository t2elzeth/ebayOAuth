import json
import logging
import urllib
from datetime import datetime, timedelta

import requests

from .credentialutil import Credentialutil
from .model import util
from .model.model import EbayOAuthToken


class Oauth2api:
    def generate_user_authorization_url(self, env_type, scopes, state=None):
        credential = Credentialutil.get_credentials(env_type)

        scopes = ' '.join(scopes)
        param = {
            'client_id': credential.client_id,
            'redirect_uri': credential.ru_name,
            'response_type': 'code',
            'prompt': 'login',
            'scope': scopes
        }

        if state is not None:
            param.update({'state': state})

        query = urllib.parse.urlencode(param)
        return env_type.web_endpoint + '?' + query

    def exchange_code_for_access_token(self, env_type, code):
        logging.info("Trying to get a new user access token ... ")
        credential = Credentialutil.get_credentials(env_type)

        headers = util.generate_request_headers(credential)
        body = util.generate_oauth_request_body(credential, code)
        resp = requests.post(env_type.api_endpoint, data=body, headers=headers)

        content = json.loads(resp.content)
        token = EbayOAuthToken()

        if resp.status_code == requests.codes.ok:
            token.access_token = content['access_token']
            token.token_expiry = datetime.utcnow() + timedelta(seconds=int(content['expires_in'])) - timedelta(
                minutes=5)
            token.refresh_token = content['refresh_token']
            token.refresh_token_expiry = datetime.utcnow() + timedelta(
                seconds=int(content['refresh_token_expires_in'])) - timedelta(minutes=5)
        else:
            token.error = str(resp.status_code) + ': ' + content['error_description']
        return token

    def get_access_token(self, env_type, refresh_token, scopes):
        """
        refresh token call
        """

        credential = Credentialutil.get_credentials(env_type)

        headers = util.generate_request_headers(credential)
        body = util.generate_refresh_request_body(' '.join(scopes), refresh_token)
        resp = requests.post(env_type.api_endpoint, data=body, headers=headers)
        content = json.loads(resp.content)
        token = EbayOAuthToken()
        token.token_response = content

        if resp.status_code == requests.codes.ok:
            token.access_token = content['access_token']
            token.token_expiry = datetime.utcnow() + timedelta(seconds=int(content['expires_in'])) - timedelta(
                minutes=5)
        else:
            token.error = str(resp.status_code) + ': ' + content['error_description']
        return token
