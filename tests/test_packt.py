import json

import pytest

import packt.free_title as packt

headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Mobile Safari/537.36'}
get_product_id_testdata = '{"data":[{"id":"55c161ec-289e-4e01-b65d-5afbec87bb7f",\
    "productId":"9781788476195","availableFrom":"2019-09-19T00:00:00.000Z",\
    "expiresAt":"2019-09-20T00:00:00.000Z","limitedAmount":false,\
    "amountAvailable":null,"details":null,"priority":0,\
    "createdAt":"2019-09-19T07:49:37.090Z","updatedAt":"2019-09-19T07:49:37.090Z",\
    "deletedAt":null}],"count":1}'
packt_cdn_response_testdata = '{"title":"Universal React with Next.js - The Ultimate \
    Guide [Video]","productId":"9781839210792","isbn10":"1839210796",\
    "isbn13":"9781839210792","isbns":{"video":"9781839210792"},\
    "length":"9 hours 21 minutes","publicationDate":"2019-11-26T00:00:00.000Z",\
    "authors":["101759"],"type":"videos","oneLiner":"Learn how to make awesome \
    server-rendered React apps with Next.js","about":"<p>Do you want to make amazing, \
    performant, and much better React applications? Look no further than Next.js</p>\
    <p>This course is the best guide you\'ll find to learning the Next.js framework. In \
    it, we will make FOUR complete React/Next.js projects, from scratch through to \
    deployment on the web.</p><p></p><p>Here\'s what we\'ll be making:</p><p></p><p>•A \
    full-stack social-media application, built with React.js/Next, a complete Express \
    API, Passport Authentication, and Material UI</p><p>•A Hacker News progressive web \
    app that can run offline and has a perfect (100/100) Lighthouse score</p><p>•A \
    user authentication system which uses signed, secure cookies</p><p>•A portfolio \
    application built as a static site</p><p></p><p>All the codes and supporting files \
    for this course are available at - https://github.com/PacktPublishing/Universal-\
    React-with-Next.js---The-Ultimate-Guide</p>","learn":"<ul><li>Build amazing server-\
    rendered React apps with Next.js </li><li>Master user authentication via Passport \
    in Next.js </li><li>Master cookie authentication in Next.js </li><li>Get cookies \
    from servers and clients</li></ul>","features":"<ul><li>Build amazing server-\
    rendered React apps with Next.js </li><li>Master user authentication via Passport \
    in Next.js </li><li>Master cookie authentication in Next.js </li><li>Get cookies \
    from servers and clients</li></ul>","category":"Web Development","available":true,\
    "releasing":true,"earlyAccess":false,"meta":{"category":{"category_name":"Web \
    Development"},"concepts":{"concept_name":"Web Programming"},\
    "language":{"language_name":"javascript"},"languageVersion":{},\
    "tool":{"tool_name":"React Native"},"vendor":{"vendor":""}},"licensed":true,\
    "shopUrl":"/web-development/universal-react-with-next-js-the-ultimate-guide-video",\
    "readUrl":"/video/web_development/9781839210792","coverImage":\
    "https://static.packt-cdn.com/products/9781839210792/cover/9781839210792 original.png"\
    ,"inStore":true,"inSubs":true}'
dummy_cdn_testdata = '{"title":"Bogus Course Title","productId":"2221788123444",\
    "isbn10":"2221788123444","isbns":{"video":"2221788123444"},\
    "shopUrl":"/web-development/bogus-course-title-the-ultimate-guide-video"}'


def test_get_id_from_json():
    assert packt.get_id_from_json(get_product_id_testdata) == '9781788476195'


def test_image_available_no_protocol_should_return_false():
    assert packt.image_available("wesleytech.com/fakeimage.png") == False


def test_get_cdn_image_returns_correct_url():
    product_id = '2221788123444'
    assert packt.get_cdn_image(product_id) == \
        'https://static.packt-cdn.com/products/2221788123444/cover/smaller'


def test_get_secondary_cdn_image():
    details_dict = json.loads(packt_cdn_response_testdata)
    image = packt.get_secondary_cdn_image(details_dict)
    assert image == 'https://static.packt-cdn.com/products/9781839210792/cover/9781839210792%20original.png'


def test_get_shop_image_when_shopurl_gets_a_match():
    details_dict = json.loads(packt_cdn_response_testdata)
    image = packt.get_shop_image(details_dict)
    assert image == 'https://static.packt-cdn.com/products/9781839210792/cover/smaller'


def test_integration_image_available_backup_image_should_return_true():
    assert packt.image_available(packt.BACKUP_IMAGE) == True


def test_integration_image_available_timeout_should_return_false():
    assert packt.image_available("https://wesleytech.com/fakeimage.png") == False


def test_integration_get_shop_image_when_shopurl_doesnt_match():
    details_dict = json.loads(dummy_cdn_testdata)
    image = packt.get_shop_image(details_dict)
    assert image == None