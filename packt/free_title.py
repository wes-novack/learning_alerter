import datetime
import json
import logging
import re
import sys

import requests
from bs4 import BeautifulSoup 

BACKUP_IMAGE = 'https://www.packtpub.com/media/wysiwyg/homepage_split_promo/freelearn_split_right.png'
FREE_URL = 'https://www.packtpub.com/free-learning'
HEADERS = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Mobile Safari/537.36'}
URL_ROOT = 'https://services.packtpub.com/free-learning-v1/offers?dateFrom='


def main():
    #switching to get_free_title_info()
    #product_id = get_product_id()
    #title, image = get_cdn_data(product_id)
    title, image = get_free_title_info()
    return title, image


def get_free_title_info():
    response = requests.get(FREE_URL, HEADERS, timeout=7)
    soup = BeautifulSoup(response.content, 'html.parser')
    free_title_image_object = soup.find(class_="product-image")
    free_title_image = free_title_image_object['src']
    free_title_name = free_title_image_object['alt'].replace("Free eBook - ","")
    return free_title_name, free_title_image


def get_product_id():
    now = datetime.datetime.utcnow()
    today = now.date()
    logging.info("now: {} today {}".format(now, today))
    tomorrow = today + datetime.timedelta(days=1)
    url = URL_ROOT+str(today)+'T00:00:00.000Z&dateTo='+str(tomorrow)+'T00:00:00.000Z'
    logging.info(f"url: {url}")
    response = requests.get(url, HEADERS, timeout=7)
    logging.info("services.packtpub.com response: {}".format(response.text))
    product_id = get_id_from_json(response.text)
    return product_id


def get_id_from_json(response_text):
    product_dict = json.loads(response_text)

    try:
        product_id = product_dict['data'][0]['productId']
        logging.info("product_id: {}".format(product_id))
    except IndexError:
        logging.error("Unable to retrieve product_id, API response empty.")
        sys.exit("Unable to retrieve product_id, API response empty.")

    return product_id


def get_cdn_data(product_id):
    url = 'https://static.packt-cdn.com/products/'+product_id+'/summary'
    response = requests.get(url, HEADERS, timeout=7)
    logging.info("Packt-CDN response: {}".format(response.text))
    details_dict = json.loads(response.text)
    title = details_dict['title']
    logging.info("title: {}".format(title))
    image = get_cdn_image(product_id)
    if not image_available(image):
        image = get_secondary_cdn_image(details_dict)
        if not image_available(image):
            image = get_shop_image(details_dict)
            if not image_available(image):
                image = BACKUP_IMAGE
    return title, image


def get_cdn_image(product_id):
    url_prefix = 'https://static.packt-cdn.com/products/'
    url_suffix = '/cover/smaller'
    return url_prefix+product_id+url_suffix


def get_secondary_cdn_image(details_dict):
    image = details_dict['coverImage'].replace(' ', '%20')
    logging.info("secondary_cdn_image: {}".format(image))
    return image


def get_shop_image(details_dict):
    shop_url = details_dict['shopUrl']
    url = 'https://www.packtpub.com'+shop_url
    logging.info("shop_url: {}".format(url))
    response = requests.get(url, HEADERS, timeout=7)
    logging.debug("response: {}".format(response.text))
    match = re.search(r'(?<=og\:image" content=").*(?=\")', str(response.text))
    logging.info("match: {}".format(match))
    if match:
        shop_image = match.group(0)
        logging.info("shop_image: {}".format(shop_image))
        return shop_image
    return None


def image_available(image):
    try:
        r = requests.head(image, timeout=7)
        if r.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        logging.info("Exception: {}".format(e))
        return False


if __name__ == '__main__':
    main()
