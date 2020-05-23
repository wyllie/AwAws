import pytest

from AwAws.Api.response import Response


def test_init():
    response = Response()
    assert response.status_code == 0
    assert response.headers == {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true"
    }
    assert response.body is None


def test_ok_200():
    response = Response()
    check = response.ok_200()
    assert check['statusCode'] == 200
    assert check['headers']['Access-Control-Allow-Origin'] == '*'
    assert check['body'] is None


def test_ok_200_dict():
    response = Response()
    check = response.ok_200({'my_data': 'dict of data to return'})
    assert check['statusCode'] == 200
    assert check['body'] == '{"my_data": "dict of data to return"}'


def test_ok_200_JSON():
    response = Response()
    check = response.ok_200('{"my_data": "big blob of JSON"}')
    assert check['statusCode'] == 200
    assert check['body'] == '{"my_data": "big blob of JSON"}'


def test_error_4XX():
    response = Response()
    check = response.error_4XX()
    assert check['statusCode'] == 422
    assert check['body'] is None
    assert check['headers']['Access-Control-Allow-Origin'] == '*'


def test_error_4XX_message():
    response = Response()
    check = response.error_4XX('this is a program error')
    assert check['statusCode'] == 422
    assert check['body'] == '{"message": "this is a program error"}'
    assert check['headers']['Access-Control-Allow-Origin'] == '*'


def test_error_4XX_status_code_message():
    response = Response()
    response.set_status_code(426)
    check = response.error_4XX('I\'m a teapot!!!')
    assert check['statusCode'] == 426
    assert check['body'] == '{"message": "I\'m a teapot!!!"}'
    assert check['headers']['Access-Control-Allow-Origin'] == '*'


def test_error_5XX():
    response = Response()
    check = response.error_5XX()
    assert check['statusCode'] == 500
    assert check['body'] is None
    assert check['headers']['Access-Control-Allow-Origin'] == '*'


def test_error_5XX_message():
    response = Response()
    check = response.error_5XX('this is a system error')
    assert check['statusCode'] == 500
    assert check['body'] == '{"message": "this is a system error"}'
    assert check['headers']['Access-Control-Allow-Origin'] == '*'


def test_error_5XX_status_code_message():
    response = Response()
    response.set_status_code(506)
    check = response.error_5XX('I\'m a variant!!!')
    assert check['statusCode'] == 506
    assert check['body'] == '{"message": "I\'m a variant!!!"}'
    assert check['headers']['Access-Control-Allow-Origin'] == '*'


def test_set_status_code():
    response = Response()
    response.set_status_code(500)
    assert response.status_code == 500


def test_set_status_code_exp():
    response = Response()
    with pytest.raises(Exception):
        response.set_status_code(700)


def test_set_header():
    response = Response()
    response.set_header('x-api', 'some_random_stuff')
    assert response.headers['x-api'] == 'some_random_stuff'


def test_set_header_missing_key():
    response = Response()
    with pytest.raises(Exception, match=r"a header key"):
        response.set_header(None, 'some_random_stuff')


def test_build_response():
    response = Response()
    response.set_status_code(404)
    response.set_header('x-app', 'blargh!')
    response.set_body('{"hello": "world"}')

    check = response._build_response()
    assert check['statusCode'] == 404
    assert check['body'] == '{"hello": "world"}'
    assert check['headers']['x-app'] == "blargh!"


def test_build_response_error_1():
    response = Response()
    response.status_code = 0
    response.set_header('x-app', 'blargh!')
    response.set_body('{"hello": "world"}')

    with pytest.raises(Exception, match=r'Response not well formed'):
        response._build_response()


def test_build_response_error_2():
    response = Response()
    response.status_code = 200
    response.headers = None
    response.set_body('{"hello": "world"}')

    with pytest.raises(Exception, match=r'Response not well formed'):
        response._build_response()
