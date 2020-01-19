from flask import jsonify


def handle_setup(challenge_payload):
    return jsonify(challenge=challenge_payload["challenge"])


def handle_event(slack_event, app, slack_client):
    with app.app_context():
        event_type = slack_event["type"]
        if event_type == 'app_mention':
            handle_app_mention(slack_event, slack_client)


def handle_app_mention(slack_event, slack_client):
    # This is the internal ID of the app sur
    # Assumes usage for this bot is "@AcroBot <value>"
    mention_keyword = "<@US801SZ17> "

    # Get the rest of the text, minus the mention
    message = slack_event['text'].replace(mention_keyword, "")
    channel = slack_event["channel"]
    slack_client.chat_postMessage(channel=channel, text=message)
