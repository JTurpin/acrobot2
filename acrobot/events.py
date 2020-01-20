from flask import jsonify

from acrobot.models import find_acronyms


def handle_setup(challenge_payload):
    return jsonify(challenge=challenge_payload["challenge"])


def handle_event(slack_event, app, slack_client):
    with app.app_context():
        event_type = slack_event["type"]
        if event_type == 'app_mention':
            handle_app_mention(slack_event, slack_client)


def handle_app_mention(slack_event, slack_client):
    # This is the internal ID of the app user
    # Assumes usage for this bot is "@AcroBot <value>"
    mention_keyword = "<@US801SZ17> "

    # Get the rest of the text, minus the mention
    search_key = slack_event['text'].replace(mention_keyword, "")
    found_acronyms = find_acronyms(search_key)
    message = build_acronym_response(found_acronyms)
    channel = slack_event["channel"]
    slack_client.chat_postMessage(channel=channel, text=message)


def build_acronym_response(found_acronyms):
    # separated into its own method so that this can be a more robust and reusable response in the future
    found_count = len(found_acronyms)
    if found_count < 1:
        return "Couldn't find any matches. You can now add new acronyms with `/acrobot-add \"acronym\" \"definition\". Try it yourself!`"

    acronym_definitions = ", or ".join([acronym.acronym_definition for acronym in found_acronyms])
    message = f"Found {found_count} possible result(s): {acronym_definitions}"
    return message
