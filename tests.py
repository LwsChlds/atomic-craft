import requests

input_dict = {
    "CO": 1,
    "O": 1,
}
url = "http://localhost:8000/combine"
data = {"data": input_dict}

response = requests.post(url, json=data)
print(response.text)
