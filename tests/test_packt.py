import json

import pytest

import packt.free_title as packt
import api_sample_data as api

headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Mobile Safari/537.36'}


def test_get_id_from_json():
    assert packt.get_id_from_json(api.get_product_id_testdata) == '9781788476195'


def test_image_available_no_protocol_should_return_false():
    assert packt.image_available("wesleytech.com/fakeimage.png") == False


def test_get_cdn_image_returns_correct_url():
    product_id = '2221788123444'
    assert packt.get_cdn_image(product_id) == \
        'https://static.packt-cdn.com/products/2221788123444/cover/smaller'


def test_get_secondary_cdn_image():
    details_dict = json.loads(api.packt_cdn_response_testdata)
    image = packt.get_secondary_cdn_image(details_dict)
    assert image == \
        'https://static.packt-cdn.com/products/9781839210792/cover/' + \
        '9781839210792%20original.png'


def test_get_shop_image_when_shopurl_gets_a_match():
    details_dict = json.loads(api.packt_cdn_response_testdata)
    image = packt.get_shop_image(details_dict)
    assert image == 'https://static.packt-cdn.com/products/9781839210792/cover/smaller'


def test_integration_image_available_backup_image_should_return_true():
    assert packt.image_available(packt.BACKUP_IMAGE) == True


def test_integration_image_available_timeout_should_return_false():
    assert packt.image_available("https://wesleytech.com/fakeimage.png") == False


def test_integration_get_shop_image_when_shopurl_doesnt_match():
    details_dict = json.loads(api.packt_cdn_response_dummydata)
    image = packt.get_shop_image(details_dict)
    assert image == None