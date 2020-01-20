import logging
import threading

from slack import WebClient
from flask import (
    Blueprint,
    jsonify,
    request,
    Response,
    current_app
)

from acrobot.events import (
    handle_setup,
    handle_event,
)
from acrobot.slash_commands import (
    respond_to_search_command,
    respond_to_add_command
)
from acrobot.utils.slack import (
    verify_event_signature,
    verfiy_slash_command_token
)

logger = logging.getLogger(__name__)
acrobot = Blueprint("acrobot", __name__)


@acrobot.route("/events", methods=["POST"])
@verify_event_signature
def route_slack_event():
    slack_client = WebClient(current_app.config["SLACK_BOT_TOKEN"])

    slack_event_payload = request.json
    if 'challenge' in slack_event_payload.keys():
        # Handle setup 'challenge' call
        # See https://api.slack.com/events/url_verification
        return handle_setup(slack_event_payload)
    elif 'event' in slack_event_payload.keys():
        # Need to eagerly respond to the event from Slack
        # Do everything else in a thread
        event_thread = threading.Thread(
                                 target=handle_event,
                                 args=(slack_event_payload['event'],
                                       current_app._get_current_object(),
                                       slack_client
                                       )
                                )
        event_thread.start()
        # Utilize join() to get everything working in Lambda
        # https://stackoverflow.com/questions/53386968/multithreading-in-aws-lambda-using-python3
        event_thread.join()
        return Response(status=200)


@acrobot.route("/commands/search", methods=["POST"])
@verfiy_slash_command_token
def search_slash_command(**kwargs):
    # Kwargs passed from verfiy_slash_command_token decorator
    request_params = kwargs['request_params']
    respond_thread = threading.Thread(target=respond_to_search_command,
                                      args=(request_params,
                                            current_app._get_current_object()
                                            )
                                      )
    respond_thread.start()
    respond_thread.join()
    return Response(status=200)


@acrobot.route("/commands/add", methods=["POST"])
@verfiy_slash_command_token
def add_slash_command(**kwargs):
    slack_client = WebClient(current_app.config["SLACK_BOT_TOKEN"])
    # Kwargs passed from verfiy_slash_command_token decorator
    request_params = kwargs['request_params']
    respond_thread = threading.Thread(target=respond_to_add_command,
                                      args=(request_params,
                                            current_app._get_current_object(),
                                            slack_client
                                            )
                                      )
    respond_thread.start()
    respond_thread.join()
    return Response(status=200)


# Healthcheck
@acrobot.route("/health")
def health():
    return jsonify(status="UP")
