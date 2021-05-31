import base64


def generate_request_headers(credential):
    b64_encoded_credential = base64.b64encode(f'{credential.client_id}:{credential.client_secret}'.encode())
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + b64_encoded_credential.decode()
    }

    return headers


def generate_application_request_body(credential, scopes):
    body = {
        'grant_type': 'client_credentials',
        'redirect_uri': credential.ru_name,
        'scope': scopes
    }

    return body


class StandardError(Exception):
    pass


def generate_refresh_request_body(scopes, refresh_token):
    if refresh_token is None:
        raise StandardError("credential object does not contain refresh_token and/or scopes")

    body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'scope': scopes
    }
    return body


def generate_oauth_request_body(credential, code):
    body = {
        'grant_type': 'authorization_code',
        'redirect_uri': credential.ru_name,
        'code': code
    }
    return body
