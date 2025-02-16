import requests

url     = 'http://127.0.0.1:5000/api/shorten'
headers = {"Content-Type" : "application/json"}
for i in range(10):
    payload = { 'longURL' : f'http://www.example{i}.com/'}
    res = requests.post(url, json=payload, headers=headers)
    print (res.text)