import boto3
import json


class SecretsManager:
    @classmethod
    def get_secret(cls, secret_name, region_name):
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

        # This app only stores things as Secret Strings, not binary
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
