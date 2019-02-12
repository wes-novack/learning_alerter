import json
import datetime
import requests


def main():
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
    product_dict = json.loads(response.text)
    product_id = product_dict['data'][0]['productId']
    return product_id


def get_title_image(product_id, headers):
    url = 'https://static.packt-cdn.com/products/'+product_id+'/summary'
    response = requests.get(url, headers)
    details_dict = json.loads(response.text)
    title = details_dict['title']
    image = details_dict['coverImage']
    return title, image


if __name__ == '__main__':
    main()
