import requests
url = "https://www.24tv.ua"
response = requests.get(url)
print(response.text)