# Acrobot2
Acrobot2 is a recreation of the idea behind Acrobot, with a friendlier and more flexible backend.

Acrobot2 is written with Flask, and deployed to AWS Lambda with Zappa. Deployments happen automatically with CircleCI on pushes to master. The backend datastore is a Postgres RDS instance. There is also a docker-compose file to run postgres locally.

For a full, slightly rambling writeup, check [here](https://simpleenergy.atlassian.net/wiki/spaces/~403095670/pages/881132280/ABHA+A+Broad+History+of+Acrobot)

## Usage
`@Acrobot <acronym>`: Original functionality of Acrobot v1 has been retained, mentioning the bot in a channel along with an acronym will look it up and post it to the same channel

`/acrobot <acronym>`: Like other slackbots, a slash command was introduced that will do the same lookup, but only post it back to the requesting user, using Slacks' ephemeral messaging feature.

`/acrobot-add "<acronym>" "<acronym definition>"`: Allows a requesting user to add a new acronym. Also posts the result back to #acrobot-support and tags the user


# How it works
Acrobot is a REST API that is reactionary to messages it receives from Slack APIs.

The routes defined in `/acrobot/routes.py` are utilized as follows:

## `/events`
A catch-all to generic Slack events. This route is decorated by `verify_event_signature`, which ensures the source of the message was definitely Slack, and that it has been signed with our app's signings secret.

There are two hardcoded rules for this route:

1. The key `challenge` appears in the Slack payload. This is used only during setup, when Slack wants to ensure that the target app is up and can return the challenge hash.
This is processed in `/acrobots/events.py`, with `handle_setup()`

2. The key `event` appears in the Slack payload. These are theoretically sent to the server any time an event (message, reaction, etc.) happens in a channel that the bot is added to, but this currently is only used to handle mentions (ie, `@Acrobot`).
This is then processed in `/acrobots/events.py`, with `handle_event()`

## `/commands/search`
This is the main slack command (`/acrobot`). This does a simple roundtrip lookup to our database to see if the acronym exists. It will send an ephemeral message to the user with the acronym definition, or with a generic error.

As an attempt to log this usage, when this slash command is used, Acrobot will also send a DM to a list of users, found in

## `/commands/add`
This is the `/acrobot-add "acronym" "definition"` command. The idea here is to take two encapsulated values (`acronym` and `acronym`) and store them in the database.
This is a lazy function- it does not check for duplicates, spelling mistakes, etc.
To make sure this isn't being mis-used, when a new acronym is successfully added, it posts to the support channel.

# Ideas (Not yet planned in roadmap)
* Get ampersands working-- escaped characters?
* Make a dev bot for local testing? (and give others access to the slack api key)
* Allow for fuzzy matching?
* Add support for more Slash commands:
-- /acrobot delete <acronym>: look up count of matching items. List out found matches as buttons, clicks will delete
-- /acrobot delete-confirm <acronym> force delete all resolutions of the acronym
-- /acrobot show-all (could be dangerous, think about pagination?)
* Auto-update slack channel description, or print count of acronyms after new additions



# Version History
## Iteration 4- "Just Read the Instructions"
* Implement routes for Slash command support
* Add command-routing layer for Slash commands: `/acrobot` and `/acrobot-add`

## Iteration 3- RIP Acrobot, Long Live Acrobot2.0
* Rewrite with Flask
* Deploy with Zappa to Tendril prod AWS
* Implemented threading for Event API + Web API
* Implemented before-request logic to slack auth/security
* Change backend storage to postgres, refactor for de-duping

## Iteration 2- Overnight Interest
* Add tests
* CI/CD support with CircleCI

## Iteration 1- Friday Hackathon
* Init project with base Real Time Messaging event loop
* Deploy to Heroku
* json file as backend storage
* Absolute matching with .lower()
