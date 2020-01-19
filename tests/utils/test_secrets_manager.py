"""
tests.utils.utils.secrets_manager
----------------------------------

Tests for secrets manager helper methods
"""
import json
from flask_testing import TestCase
from unittest.mock import patch

from acrobot.app import create_app
from acrobot.envs.default import DefaultSettings
from acrobot.utils.secrets_manager import SecretsManager


class TestSecretsManager(TestCase):
    def create_app(self):
        app, _ = create_app()
        return app

    def setUp(self):
        self.boto3_patch = patch("acrobot.utils.secrets_manager.boto3")
        self.boto3_mock = self.boto3_patch.start()
        self.addCleanup(self.boto3_patch.stop)

    def test_get_secret(self):
        """
        Test secrets retrieval from Secrets Manager
        """
        self.boto3_mock.session.Session().client().get_secret_value.return_value = \
            {"SecretString": json.dumps({"API_KEY": "test"})}
        secret = SecretsManager().get_secret("test-secret", "us-east-1")["API_KEY"]
        self.assertEqual(secret, "test")

    def test_load_secret_for_default_env(self):
        """
        Test secrets retrieval from Secrets Manager by loading an environment
        """
        self.boto3_mock.session.Session().client().get_secret_value.return_value = \
            {"SecretString": json.dumps({"API_KEY": "test"})}
        secret = DefaultSettings().get_secrets("test-secret", "us-east-1")["API_KEY"]
        self.assertEqual(secret, "test")
