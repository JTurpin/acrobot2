#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tests.test_routes
----------------------------------

Tests for versionless routes
"""

from flask_testing import TestCase

from acrobot.app import create_app
from acrobot.exceptions import ServiceError
from acrobot.app import (
    bad_request,
    catch_all_exceptions,
    handle_service_error,
    internal_error,
    not_found
)


class TestDefaultRoutes(TestCase):
    def create_app(self):
        app, _ = create_app()
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_health(self):
        response = self.client.get("/health")
        assert response.status_code == 200

    def test_internal_error(self):
        response, status_code = internal_error("FakeError")
        self.assertEqual(status_code, 500)
        self.assertEqual(response.json, {
            "code": "UNKNOWN",
            "message": "Unknown server error"
        })

    def test_not_found(self):
        response, status_code = not_found("FakeError")
        self.assertEqual(status_code, 404)
        self.assertEqual(response.json, {
            "code": "NOT_FOUND",
            "message": "Route not found"
        })

    def test_bad_request(self):
        response, status_code = bad_request("FakeError")
        self.assertEqual(status_code, 400)
        self.assertEqual(response.json, {
            "code": "BAD_REQUEST",
            "message": "The server cannot process this request"
        })

    def test_handle_service_error(self):
        fake_code = "FAKE"
        fake_message = "A fake error occured"
        fake_status_code = 444
        exception = ServiceError(
            fake_code,
            fake_message,
            status_code=fake_status_code
        )

        response, status_code = handle_service_error(exception)
        self.assertEqual(status_code, fake_status_code)
        self.assertEqual(response.json, {
            "code": fake_code,
            "message": fake_message
        })

    def test_catch_all_exceptions_alert(self):
        exception = Exception("Unit test")
        catch_all_exceptions(exception)
