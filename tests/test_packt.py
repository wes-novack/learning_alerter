import pytest
import logging
import packt.free_title as packt
import json

headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Mobile Safari/537.36'}
get_product_id_testdata = '{"data":[{"id":"55c161ec-289e-4e01-b65d-5afbec87bb7f","productId":"9781788476195","availableFrom":"2019-09-19T00:00:00.000Z","expiresAt":"2019-09-20T00:00:00.000Z","limitedAmount":false,"amountAvailable":null,"details":null,"priority":0,"createdAt":"2019-09-19T07:49:37.090Z","updatedAt":"2019-09-19T07:49:37.090Z","deletedAt":null}],"count":1}'


def test_setup_logging():
    logger = packt.setup_logging()
    assert type(logger.handlers[1]) is logging.handlers.RotatingFileHandler


def test_get_id_from_json():
    response_text = get_product_id_testdata
    assert packt.get_id_from_json(response_text) == '9781788476195'
