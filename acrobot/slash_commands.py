import requests

from acrobot.models import Acronym, find_acronyms


def respond_to_search_command(slack_event, app):
    # Sends an ephemeral message back to the user
    with app.app_context():
        search_key = slack_event['text']
        found_acronyms = find_acronyms(search_key)
        message_text = build_acronym_response(found_acronyms)
        message = {
            "response_type": "ephemeral",
            "text": message_text
        }
        requests.post(slack_event['response_url'], json=message)


def respond_to_add_command(slack_event, app, slack_client):
    with app.app_context():
        channel = "test"
        message = "This is a mock response!"
        # Sloppy way to break out the two args passed in to slack
        # Example: slack_event["text"] == '"gpc" "green button connect"'
        # Want to split on '" "', and replace the remaining quotes
        try:
            acronym, definition = slack_event["text"].replace('" "', '|||').strip('"').split("|||")
        except:
            message = {
                "response_type": "ephemeral",
                "text": "It looks like your message was malformatted. :sadparrot:"
                        "\nUsage is `/acrobot-add \"acronym\" \"definition\"`. "
                        "\n Example: `/acrobot-add \"saas\" \"Software as a Service\"` :acrobot:"
            }
            requests.post(slack_event['response_url'], json=message)
        else:
            message = {
                "response_type": "ephemeral",
                "text": "Okay, i'll add it! :acrobot:"
            }
            Acronym.create(acronym, definition, created_by=slack_event["user_name"])
            mentioned_user = slack_event["user_id"]
            message = f"I have learned `{acronym}` means `{definition}`. Thank you <@{mentioned_user}>!"
            slack_client.chat_postMessage(channel=channel, text=message)


def build_acronym_response(found_acronyms):
    # separated into its own method so that this can be a more robust and reusable response in the future
    found_count = len(found_acronyms)
    if found_count < 1:
        return "Couldn't find any matches. Fill out this form to add it! " \
               "https://forms.gle/ue5GMSaajdiHiGX2A, you can also talk about me in <#CS832PHPU>"

    acronym_definitions = ", or ".join([acronym.acronym_definition for acronym in found_acronyms])
    message = f"Found {found_count} possible result(s): {acronym_definitions}"
    return message
