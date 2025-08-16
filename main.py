'''
curl -X 'POST' \
  'http://5.63.153.31:5051/v1/account' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "user90",
  "email": "nazgyl-92@mail.ru",
  "password": "password"
}'
http://localhost:5050/activate/7aee0663-70d4-4e05-9a91-a992922f5ccf

curl -X 'PUT' \
  'http://5.63.153.31:5051/v1/account/7aee0663-70d4-4e05-9a91-a992922f5ccf' \
  -H 'accept: text/plain'
'''
from pprint import pprint

import requests

url = 'http://5.63.153.31:5051/v1/account/3322f2f2-1e29-4620-8826-e5efb8bfcedc'
headers = {
    'accept': 'text/plain'

}
# json = {
#     "login" : "user90",
#     "email" : "nazgyl-92@mail.ru",
#     "password" : "password"
# }
response = requests.put(
    url=url,
    headers=headers
)
print(response.status_code)
pprint(response.json())
response_json =response.json()
print(response_json['resource']['rating']['enabled'])