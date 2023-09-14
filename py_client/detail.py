import requests


endpoint = "http://127.0.0.1:8000/api/"
get_response = requests.get(endpoint+"product/21/")

# print(get_response.headers)
print(get_response.json())            