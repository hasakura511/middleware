# %%
from db.models import DBUser
from db.db_sqlite import get_db
import requests
import json
url = 'http://localhost:5000/items/new'

body = {
    "title": "string",
    "content": "string",
    "published": True,
    "comment_title": 12
}
# missing/wrong datatype data returns 422 - Unprocessable Entity

response = requests.post(url, data=json.dumps(body))

print(response.status_code)
print(response.text)
# %%

url = 'http://localhost:5000/items/new2/12?version=2'

body = {
    "title": "string",
    "content": "string",
    "published": True,
    "comment_title": 12
}
# missing/wrong datatype data returns 422 - Unprocessable Entity

response = requests.post(url, data=json.dumps(body))

print(response.status_code)
print(response.text)


# %%

url = 'http://localhost:5000/items/new/12/comment?commentTitle=2'

body = {
    "title": "string",
    "content": "string",
    "published": True,
    "comment_title": 12
}
# missing/wrong datatype data returns 422 - Unprocessable Entity

response = requests.post(url, data=json.dumps(body))

print(response.status_code)
print(response.text)

# %%
#url = 'http://localhost:5000/items/new/12/comment?commentTitle=2&v=string1&v=string2&v=string3'
#url = 'http://localhost:5000/items/new/12/comment?commentTitle=2'
url = 'http://localhost:5000/items/new/12/comment/9?commentTitle=2'

body = {
    "item": {
        "title": "string",
        "content": "string",
        "published": True,
        "comment_title": 12,
        "tags": ["tag1", "tag2"],
        "metadata": {'key': 'value'},
        "image": {
            "url": "string",
            "alias": "string"
        },
    },
    "content": "overwrite optional if not elipsis",
}
# missing/wrong datatype data returns 422 - Unprocessable Entity

response = requests.post(url, data=json.dumps(body))

print(response.status_code)
print(json.dumps(response.json(), indent=2, sort_keys=True))
# %%

url = 'http://localhost:5000/item/all'
url = 'http://localhost:5000/user'
url = 'http://localhost:5000/user/2/delete'
url = 'http://localhost:5000/user/1'
url = 'http://localhost:5000/article/100'

# missing/wrong datatype data returns 422 - Unprocessable Entity
# non existant users return 200/null
response = requests.get(url)

print(response.status_code)
print(json.dumps(response.json(), indent=2, sort_keys=True))
# %%
#url = 'http://localhost:5000/user/'
url = 'http://localhost:5000/user/3/update'

body = {
    "username": "update_test2",
    "email": "update_test2",
    "password": "update_string"
}
response = requests.post(url, data=json.dumps(body))

print(response.status_code)
print(json.dumps(response.json(), indent=2, sort_keys=True))

# %%
url = 'http://localhost:5000/article/'
#url = 'http://localhost:5000/article/1/update'

body = {
    "title": "article2",
    "content": "article2",
    "published": True,
    "user_id": 1
}
response = requests.post(url, data=json.dumps(body))

print(response.status_code)
print(json.dumps(response.json(), indent=2, sort_keys=True))

# %%


db = next(get_db())
user = db.query(DBUser).filter(DBUser.id == 1)

# %%
