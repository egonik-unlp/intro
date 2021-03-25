
import json
import requests

URL_JSON = 'https://raw.githubusercontent.com/egonik-unlp/intro_bot/main/prueba.json'
r = requests.get(URL_JSON)

d = r.json()

print(d)
print(type(d))
