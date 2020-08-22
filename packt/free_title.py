import datetime
import json
import logging
import logging.handlers
import requests
import re

LOG_FILENAME = 'learning_alerter.log'
LOG_LEVEL = 'INFO'
MAX_BYTES = 524288000
BACKUP_COUNT = 3


def setup_logging():
    logging.basicConfig(level=LOG_LEVEL, filename=LOG_FILENAME, format='%(name)s - %(levelname)s - %(message)s')    
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    logging.getLogger('').addHandler(handler)
    return logging.getLogger()


def main():
    setup_logging()
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Mobile Safari/537.36'}
    product_id = get_product_id(headers)
    title, image = get_cdn_data(product_id, headers)
    return title, image


def get_id_from_json(response_text):
    product_dict = json.loads(response_text)
    product_id = product_dict['data'][0]['productId']
    logging.info("product_id: {}".format(product_id))
    return product_id


def get_product_id(headers):
    now = datetime.datetime.utcnow()
    today = now.date()
    logging.info("now: {} today {}".format(now, today))
    tomorrow = str(today + datetime.timedelta(days=1))
    url = 'https://services.packtpub.com/free-learning-v1/offers?dateFrom='+str(today)+'T00:00:00.000Z&dateTo='+tomorrow+'T00:00:00.000Z'
    response = requests.get(url, headers)
    logging.info("services.packtpub.com response: {}".format(response.text))
    product_id = get_id_from_json(response.text)
    return product_id


def get_cdn_data(product_id, headers):
    url = 'https://static.packt-cdn.com/products/'+product_id+'/summary'
    response = requests.get(url, headers)
    logging.info("Packt-CDN response: {}".format(response.text))
    details_dict = json.loads(response.text)
    title = details_dict['title']
    image = details_dict['coverImage'].replace(' ', '%20')
    shop_url = details_dict['shopUrl']
    logging.info("title: {}".format(title))
    logging.info("image: {}".format(image))
    image = check_image_availability(image, shop_url, headers)
    return title, image


def check_image_availability(image, shop_url, headers):
    backup_image = 'https://www.packtpub.com/media/wysiwyg/homepage_split_promo/freelearn_split_right.png'
    if image_available(image):
        return image
    else:
        url = 'https://www.packtpub.com'+shop_url
        logging.info(url)
        response = requests.get(url, headers)
        logging.debug("response: {}".format(response.text))
        match = re.search('(?<=og\:image" content=").*(?=\")', str(response.text))
        shop_image = match.group(0)
        logging.info("shop_image: {}".format(shop_image))
        if image_available(shop_image):
            return shop_image
        else:
            return backup_image


def image_available(image):
    r = requests.head(image)
    if r.status_code == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    main()
