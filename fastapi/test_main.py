from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

'''
https://docs.pytest.org/en/6.2.x/goodpractices.html
pytest implements the following standard test discovery:

If no arguments are specified then collection starts from testpaths (if configured) or the current directory. Alternatively, command line arguments can be used in any combination of directories, file names or node ids.

Recurse into directories, unless they match norecursedirs.

In those directories, search for test_*.py or *_test.py files, imported by their test package name.

From those files, collect test items:

test prefixed test functions or methods outside of class

test prefixed test functions or methods inside Test prefixed test classes (without an __init__ method)
'''


def test_all_items():
    response = client.get('/item/all')
    assert response.status_code == 200


def test_auth_error():
    response = client.post('/token',
                           # request body type: application/x-www.form-urlencoded -> use data
                           data={'username': '', 'password': ''}
                           )
    access_token = response.json().get('access_token')
    # check if test fails, will print to console if failed
    #assert access_token == ''
    assert access_token is None
    print(response.json())
    message = response.json().get('detail')[0].get('msg')
    # print(message)
    assert message == 'field required'


def test_auth_success():
    response = client.post('/token',
                           # request body type: application/x-www.form-urlencoded -> use data
                           data={'username': 'test', 'password': 'test'}
                           )
    access_token = response.json().get('access_token')
    # check if test fails, will print to console if failed
    #assert access_token == ''
    assert access_token


def test_post_article():
    response = client.post('/token',
                           # request body type: application/x-www.form-urlencoded -> use data
                           data={'username': 'test', 'password': 'test'}
                           )
    access_token = response.json().get('access_token')
    # check if test fails, will print to console if failed
    #assert access_token == ''
    assert access_token

    response = client.post('/article/',
                           # application/json -> use json
                           json={
                               "title": "pytest",
                               "content": "pytest",
                               "published": True,
                               "user_id": 1
                           },
                           headers={
                               'Authorization': 'bearer '+access_token
                           }
                           )
    assert response.status_code == 200
    assert response.json().get('title') == 'pytest'
