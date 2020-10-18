# learning_alerter
Web scraper that can run on a schedule to find and post about free learning content. Requires python >=3.6 

## Prepare a non-containerized environment
```
virtualenv venv -p python3
. venv/bin/activate
pip install -r requirements.txt
```

## Run the program
Schedule execution similar to the following examples.

To use a Slack webhook:

`python main.py --packt --slackwebhook 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX'`

Note: Slack now requires you to use the webhook configuration in order to set the display name, the avatar/icon, and the targeted channel. See [the instructions here on creating a Slack webhook](https://api.slack.com/messaging/webhooks).

To use a Slack legacy Slack API token (now deprecated by Slack):

`python main.py --packt --slacktoken 'xoxp-your-super-secret-slack-token' --slackchannel '#yourchannel'`

## Run tests
From the root of the repository/project, run:

`python -m pytest`

## Build Docker image
From the root of the repository/project, run:

`docker build -t learning_alerter .`

## Run in Docker
After you've built the container image locally using docker build, then run:

`docker run -it -e SLACKWEBHOOK='https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX' -e PACKT=true learning_alerter:latest`

Note: if running from a cron, omit the `-it` flags, as interactive (-i) and tty (-t) are not available in cron.
