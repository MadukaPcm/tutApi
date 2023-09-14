import requests


endpoint = "http://127.0.0.1:8000/api/"

data = {
    "title":"Leo mimi sina neno brother frank",
    "content":"Oy maduka wewe Mbona unaonekana ni nouma sana mkuu",
    "price":129.99
}
get_response = requests.put(endpoint+"product/21/update/", json=data)

# print(get_response.headers)   
print(get_response.json())              