# Roadmap
## Iteration 4
* Implement routes for Slash command support
* Add command-routing layer for `/acrobot add`

## Iteration 5
* Implement [Building block response](https://api.slack.com/block-kit) for a friendlier UX
* Add command-routing layer for `/acrobot delete`

# Ideas (Not yet planned in roadmap)
* Get ampersands working-- escaped characters?
* Make a dev bot for local testing? (and give others access to the slack api key)
* Allow for fuzzy matching?
* Add support for [Slash commands](https://api.slack.com/interactivity/slash-commands#naming_your_command):
-- /acrobot add <acronym> <full message> (log an added-by user+channel)
-- /acrobot delete <acronym>: look up count of matching items. List out found matches as buttons, clicks will delete
-- /acrobot delete-confirm <acronym> force delete all resolutions of the acronym
-- /acrobot show-all (could be dangerous, think about pagination?)
* Auto-update slack channel description, or print count of acronyms after new additions



# Version History
## Iteration 1- Friday Hackathon
* Init project with base Real Time Messaging event loop
* Deploy to Heroku
* json file as backend storage
* Absolute matching with .toLower()

## Iteration 2- Overnight Interest
* Add tests
* CI/CD support with CircleCI

## Iteration 3- Acrobot is Dead, Long Live Acrobot2.0
* Rewrite with Flask
* Deploy with Zappa
* Implemented threading for Event API + Web API
* Implemented before-request logic to slack auth/security
* Change backend storage to postgres, refactor for de-duping
