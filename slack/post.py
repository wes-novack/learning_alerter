import os
from slackclient import SlackClient


def main(token, image, title, channel):
    client = create_slack_client(token)
    post_to_channel(client, image, title, channel)


def create_slack_client(token):
    client = SlackClient(token)
    return client


def post_to_channel(client, image, title, channel):
    client.api_call(
                    "chat.postMessage",
                    username='learning_alerter',
                    channel=channel,
                    icon_emoji=":books:",
                    text="Free ebook of the day: "+title,
                    attachments=[{'fallback': 'Packt free book of the day',
                                  'image_url': image,
                                  'title': 'Download here: '+title,
                                  'title_link': 'https://www.packtpub.com/packt/offers/free-learning',
                                  'text': 'Only available for 24 hours'}]
    )


if __name__ == '__main__':
    main()
