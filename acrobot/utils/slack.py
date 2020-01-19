import time
import hmac
import hashlib
from functools import wraps

from flask import (
    request
)

SLACK_SIGNING_SECRET = bytes('fe4203c03990bf948110a7f3d06c5238', 'UTF-8')


def verify_slack_signature(func):
    @wraps(func)
    def wrapped_route():
        # Verify HMAC
        timestamp = request.headers['X-Slack-Request-Timestamp']
        if abs(int(time.time()) - int(timestamp)) > 60 * 5:
            # The request timestamp is more than five minutes from local time.
            # It could be a replay attack, so let's ignore it.
            return
        sig_basestring = 'v0:' + timestamp + ':' + request.data.decode('utf-8')
        my_signature = 'v0=' + hmac.new(SLACK_SIGNING_SECRET,
                                        sig_basestring.encode('utf-8'),
                                        digestmod=hashlib.sha256).hexdigest()
        slack_signature = request.headers['X-Slack-Signature']
        if hmac.compare_digest(my_signature, slack_signature):
            return func()
    return wrapped_route
