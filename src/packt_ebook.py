import json, re
import requests, slackclient


def main():
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Mobile Safari/537.36'}
    product_id = get_product_id(headers)
    #title_image = get_title_image(product_id, headers)


def get_product_id(headers):
    url = 
    response = requests.get(url, headers)
    product_dict = json.loads(response)
    product_id = product_dict['']
    print(product_id)
    return product_id


def get_title_image(product_id, headers):
    url = https://static.packt-cdn.com/products/product_id/summary
    response = requests.get(url, headers)
    details_dict = json.loads(response)
    title = details_dict['title']
    image = details_dict['image']



if __name__ == '__main__':
    main()
