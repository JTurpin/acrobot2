import time
import hmac
import hashlib
from urllib import parse
from functools import wraps

from flask import (
    request,
    Response,
    current_app
)


def verify_event_signature(func):
    @wraps(func)
    def wrapped_route():
        # Verify HMAC
        timestamp = request.headers['X-Slack-Request-Timestamp']
        if abs(int(time.time()) - int(timestamp)) > 60 * 5:
            # The request timestamp is more than five minutes from local time.
            # It could be a replay attack, so let's ignore it.
            return
        sig_basestring = 'v0:' + timestamp + ':' + request.data.decode('utf-8')
        my_signature = 'v0=' + hmac.new(current_app.config["SLACK_SIGNING_SECRET"],
                                        sig_basestring.encode('utf-8'),
                                        digestmod=hashlib.sha256).hexdigest()
        slack_signature = request.headers['X-Slack-Signature']
        if hmac.compare_digest(my_signature, slack_signature):
            return func()
    return wrapped_route


def verfiy_slash_command_token(func):
    @wraps(func)
    def wrapped_route(**kwargs):
        timestamp = request.headers['X-Slack-Request-Timestamp']
        if abs(int(time.time()) - int(timestamp)) > 60 * 5:
            # The request timestamp is more than five minutes from local time.
            # It could be a replay attack, so let's ignore it.
            return
        sig_basestring = f'v0:{timestamp}:{parse.urlencode(request.form.to_dict())}'.encode('utf-8')
        my_signature = 'v0=' + hmac.new(current_app.config["SLACK_SIGNING_SECRET"],
                                        sig_basestring,
                                        digestmod=hashlib.sha256).hexdigest()
        slack_signature = request.headers['X-Slack-Signature']
        if hmac.compare_digest(my_signature, slack_signature):
            kwargs["request_params"] = request.values.to_dict()
            return func(**kwargs)
        else:
            return Response(status=403)
    return wrapped_route
