import logging

import requests


def main(webhook, image, title, dryrun):
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
    if dryrun:
        print("DRYRUN")
        print(f"Would have run: requests.post({webhook}, headers={headers}, json={data})")
    else:
        r = requests.post(webhook, headers=headers, json=data)
        logging.info("post_with_webhook called")
        logging.info(f"r.status_code: {r.status_code}")
