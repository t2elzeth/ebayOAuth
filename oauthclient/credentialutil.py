import json
import yaml

from .model.model import Environment, Credentials

user_config_ids = ["sandbox-user", "production-user"]


class Credentialutil:
    _credential_list = {}

    @classmethod
    def load(cls, app_config_path):
        with open(app_config_path, 'r') as f:
            if app_config_path.endswith('.yaml') or app_config_path.endswith('.yml'):
                content = yaml.load(f, Loader=yaml.FullLoader)
            elif app_config_path.endswith('.json'):
                content = json.loads(f.read())
            else:
                raise ValueError('Configuration file need to be in JSON or YAML')
            Credentialutil._iterate(content)

    @classmethod
    def _iterate(cls, content):
        for key in content:
            if key in [Environment.PRODUCTION.config_id, Environment.SANDBOX.config_id]:
                client_id = content[key]['appid']
                dev_id = content[key]['devid']
                client_secret = content[key]['certid']
                ru_name = content[key]['redirecturi']

                app_info = Credentials(client_id, client_secret, dev_id, ru_name)
                cls._credential_list.update({key: app_info})

    @classmethod
    def get_credentials(cls, env_type):
        """
        env_config_id: Environment.PRODUCTION.config_id or Environment.SANDBOX.config_id
        """
        if len(cls._credential_list) == 0:
            raise CredentialNotLoadedError("No Environment loaded from configuration file")
        return cls._credential_list[env_type.config_id]


class CredentialNotLoadedError(Exception):
    pass
