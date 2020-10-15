import requests
import logging


def post_to_webhook(webhook, image, title):
    headers = {'Content-type': 'application/json'}
    data = {
        "text": "Free title of the day: "+title,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Free title of the day: "+title
                    }
            },
            {
                "type": "section",
                "block_id": "link",
                "text": {
                    "type": "mrkdwn",
                    "text": "*<https://www.packtpub.com/free-learning|Claim here: "+title+">*"
                }
            },
            {
                "type": "image",
                "block_id": "content_image",
                "image_url": image,
                "alt_text": "Cover image for free content",
                "title": {
                    "type": "plain_text",
                    "text": "Available for a limited time"
                }
            }
        ]
    }
    r = requests.post(webhook, headers=headers, json=data)
    logging.info("post_to_webhook function")
    logging.info(f"r.status_code: {r.status_code}")
