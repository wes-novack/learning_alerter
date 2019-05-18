import datetime
import json
import logging
import requests


def setup_logging():
    logging.basicConfig(level=logging.INFO, filename='learning_alerter.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')    


def main():
    setup_logging()
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Mobile Safari/537.36'}
    product_id = get_product_id(headers)
    title, image = get_title_image(product_id, headers)
    return title, image


def get_product_id(headers):
    now = datetime.date.today()
    today = now.isoformat()
    tomorrow = str(now + datetime.timedelta(days=1))
    url = 'https://services.packtpub.com/free-learning-v1/offers?dateFrom='+today+'T00:00:00.000Z&dateTo='+tomorrow+'T00:00:00.000Z'
    response = requests.get(url, headers)
    logging.info("services.packtpub.com response: {}".format(response.text))
    product_dict = json.loads(response.text)
    product_id = product_dict['data'][0]['productId']
    logging.info("product_id: {}".format(product_id))
    return product_id


def get_title_image(product_id, headers):
    url = 'https://static.packt-cdn.com/products/'+product_id+'/summary'
    response = requests.get(url, headers)
    logging.info("Packt-CDN response: {}".format(response.text))
    details_dict = json.loads(response.text)
    title = details_dict['title']
    image = details_dict['coverImage'].replace(' ', '%20')
    logging.info("title: {}".format(title))
    logging.info("image: {}".format(image))
    return title, image


if __name__ == '__main__':
    main()
