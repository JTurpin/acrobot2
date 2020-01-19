#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_app
------------------------------------

Tests for the `acrobot` app module.
"""
import unittest
from unittest.mock import patch, MagicMock

from acrobot.app import (
    setup_logging,
)


class TestAcrobotApp(unittest.TestCase):
    pass


class TestAcrobotLogging(unittest.TestCase):

    @patch.dict("os.environ", {"SERVERTYPE": "AWS Lambda"})
    def test_setup_logging(self):
        mock_app = MagicMock()
        mock_app.config = {"LOG_LEVEL": "CRITICAL"}
        setup_logging(mock_app)

    @patch.dict("os.environ", {"SERVERTYPE": "NOT LAMBDA"})
    @patch("acrobot.app.logger")
    def test_setup_logging_already_setup(self, mock_logger):

        mock_app = MagicMock()
        mock_app.config = {"LOG_LEVEL": "CRITICAL"}
        mock_logger.hasHandlers.return_value = False

        setup_logging(mock_app)
