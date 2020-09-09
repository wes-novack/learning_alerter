# learning_alerter
Web scraper that can run on a schedule to find and post about free learning content. Requires python >=3.6 

## Run the program
Schedule execution similar to the following:

`python main.py --packt --slacktoken 'xoxp-your-super-secret-slack-token' --slackchannel '#yourchannel'`

## Run tests
From the root of the repository/project, run:

`python -m pytest`

## Build Docker image
docker build -t learning_alerter .

## Run in Docker
docker run -it -e SLACKTOKEN='xoxp-your-secret-slack-token' -e SLACKCHANNEL='yourchannel' -e PACKT=true learning_alerter:latest