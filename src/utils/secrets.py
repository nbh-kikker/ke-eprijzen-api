from google.cloud.secretmanager import SecretManagerServiceClient, AccessSecretVersionRequest

from google.cloud.secretmanager import (
    SecretManagerServiceClient,
    AccessSecretVersionRequest,
)
# import google.auth as ga
# import google.auth.impersonated_credentials as gai
from google.oauth2 import service_account
import google.auth as ga
from typing import Optional, Callable


class Settings:
    _secret_manger = Optional[SecretManagerServiceClient]
    
    def __init__(self, project: str) -> None:
        self.cred, self.project_id = ga.default()
        self.client = self.open_secret_client(self.cred)
        self.project = project
    
    @classmethod
    def open_secret_client(cls, cred: service_account.Credentials):
        cls._secret_manger = SecretManagerServiceClient(credentials=cred)

    
    def access_value(self, secret: str, output: Callable = str, version: str = "latest"):
        """
        arg output : data type of the secret
        arg secret : name of secret
        """

        request = AccessSecretVersionRequest(
            name=f"projects/{self.project}/secrets/{secret}/versions/"
            + version
        )

        payload = self._secret_manger.access_secret_version(request=request).payload

        out = payload.data.decode("utf-8")

        return output(out)

    @classmethod
    def close_secret_client(cls):
        cls._secret_manger.transport.close()
