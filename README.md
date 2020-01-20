# Acrobot2
Acrobot2 is a recreation of the idea behind Acrobot, with a friendlier and more flexible backend.

Acrobot2 is written with Flask, and deployed to AWS Lambda with Zappa. Deployments happen automatically with CircleCI on pushes to master. The backend datastore is a Postgres RDS instance. There is also a docker-compose file to run postgres locally.

For a full, slightly rambling writeup, check [here](https://simpleenergy.atlassian.net/wiki/spaces/~403095670/pages/881132280/ABHA+A+Broad+History+of+Acrobot)

## Usage
`@Acrobot <acronym>`: Original functionality of Acrobot v1 has been retained, mentioning the bot in a channel along with an acronym will look it up and post it to the same channel

`/acrobot <acronym>`: Like other slackbots, a slash command was introduced that will do the same lookup, but only post it back to the requesting user, using Slacks' ephemeral messaging feature.

`/acrobot-add "<acronym>" "<acronym definition>"`: Allows a requesting user to add a new acronym. Also posts the result back to #acrobot-support and tags the user



# Roadmap
## Iteration 5
* Implement [Building block response](https://api.slack.com/block-kit) for a friendlier UX
* Add command-routing layer for `/acrobot delete`

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
* Deploy with Zappa
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
