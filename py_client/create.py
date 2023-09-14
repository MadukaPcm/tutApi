import requests

endpoint = "http://localhost:8000/api/product/"

data = {
    "title":"Kidogo",
    "content":"",
    "price":550.99
    }
get_response = requests.post(endpoint, json=data)
print(get_response)