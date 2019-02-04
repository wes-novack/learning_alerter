import os
from slackclient import SlackClient


def main(token, message, channel):
    client = create_slack_client(token)
    post_to_channel(client, message, channel)


def create_slack_client(token):
    client = SlackClient(token)
    return client


def post_to_channel(client, message, channel):
    client.api_call("chat.postMessage", channel=channel, text=message)


if __name__ == '__main__':
    main()
