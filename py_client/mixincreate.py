import requests

endpoint = "http://localhost:8000/api/product/mixin/"

data = {
    "title":"Kidogo",
    "content":"madukka",
    "price":550.99
    }
get_response = requests.post(endpoint, json=data)
print(get_response)