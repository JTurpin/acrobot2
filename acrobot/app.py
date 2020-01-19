import os
import logging

from flask import (
    Flask,
    jsonify,
    request,
)

from acrobot.routes import acrobot
from acrobot.envs.setup_environment import setup_environment
from acrobot.exceptions import ServiceError
from acrobot.models import db

logger = logging.getLogger(__name__)
LOG_LEVEL_MAP = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


def create_app(db_uri=None, testing=False):
    app = Flask(__name__)
    app.after_request(respond_with_request_id)
    app.register_error_handler(500, internal_error)
    app.register_error_handler(404, not_found)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(ServiceError, handle_service_error)
    app.register_error_handler(Exception, catch_all_exceptions)
    app.register_blueprint(acrobot, url_prefix='')
    app.config["LOG_LEVEL"] = os.environ.get(
        "SERVICE_LOG_LEVEL",
        "INFO"
    )
    setup_logging(app)
    setup_environment(app)
    db.init_app(app)
    return app, db


def setup_logging(app):
    verbosity = app.config["LOG_LEVEL"]
    global_logger = logging.getLogger("")
    global_logger.setLevel(LOG_LEVEL_MAP[verbosity])

    if os.environ.get("SERVERTYPE") != "AWS Lambda" and not logger.hasHandlers():
        # When we run under lambda, zappa sets up logging for us, but running
        # under pure flask / wsgi-server we have to do this ourselves
        global_stream = logging.StreamHandler()
        global_stream.setFormatter(logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s"
        ))
        global_logger.addHandler(global_stream)


def respond_with_request_id(response):
    response.headers["X-Request-ID"] = request.headers.get("X-Request-ID", "")
    return response


def internal_error(error):
    logger.error(error)
    return jsonify(code="UNKNOWN", message="Unknown server error"), 500


def not_found(error):
    logger.error(error)
    return jsonify(code="NOT_FOUND", message="Route not found"), 404


def bad_request(error):
    logger.error(error)
    return jsonify(code="BAD_REQUEST", message="The server cannot process this request"), 400


def handle_service_error(error):
    logger.exception(error)
    return jsonify(code=error.code, message=error.message), error.status_code


def catch_all_exceptions(error):
    logger.exception(error)
    return jsonify(
        code="INTERNAL_SERVER_ERROR",
        message="The server encountered an unexpected condition "
                "which prevented it from fulfilling the request."
    ), 500
