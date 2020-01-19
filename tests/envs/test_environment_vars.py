"""
tests.envs.test_environment_vars
----------------------------------

Tests for class-based enviroment objects loaded into Flask app context
"""
import os
from flask_testing import TestCase
from unittest.mock import patch

from acrobot.app import create_app


secrets_manager_return_value = {"SECRETS_LOADED": True}


class TestEnvironmentSetup(TestCase):
    def tearDown(self):
        os.environ["ENV"] = "dev"

    def create_app(self):
        app, _ = create_app()
        return app

    def test_environment_setup_error(self):
        """
        Test that invalid environment name throws an error
        """
        os.environ["ENV"] = "foo"
        with self.assertRaises(Exception):
            self.create_app()

    @patch('acrobot.envs.stage.StageSettings.get_secrets',
           return_value=secrets_manager_return_value)
    def test_staging_environment_setup(self, mock_secrets):
        """
        Tests loading uat env configs

        Mock get_secrets() so we don't make a real call to AWS
        """
        os.environ["ENV"] = "stage"
        app = self.create_app()
        self.assertEqual(app.config["ENV"], "stage")
        self.assertTrue(app.config["ENV_LOADED"])

    @patch('acrobot.envs.production.ProductionSettings.get_secrets',
           return_value=secrets_manager_return_value)
    def test_production_environment_setup(self, mock_secrets):
        """
        Tests loading production env configs

        Mock get_secrets() so we don't make a real call to AWS
        """
        os.environ["ENV"] = "prod"
        app = self.create_app()
        self.assertEqual(app.config["ENV"], "prod")
        self.assertTrue(app.config["ENV_LOADED"])

    @patch('acrobot.envs.development.DevelopmentSettings.get_secrets',
           return_value=secrets_manager_return_value)
    def test_default_environment_setup(self, mock_secrets):
        """
        Tests loading default env configs
        """
        app = self.create_app()
        self.assertEqual(app.config["ENV"], "dev")
        self.assertTrue(app.config["ENV_LOADED"])
