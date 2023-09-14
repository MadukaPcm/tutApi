import requests
from getpass import getpass

auth_endpoint = "http://localhost:8000/api/auth/"
password = getpass()

auth_response = requests.post(auth_endpoint, json={'username':'frank','password':password})
print(auth_response.json())  

if auth_response.status_code == 200:
    token = auth_response.json()['token']
    header = {"Authorization": f"Token {token}"}
    
    endpoint = "http://localhost:8000/api/product/mixin/"

    get_response = requests.get(endpoint,headers=header)
    print(get_response.json())