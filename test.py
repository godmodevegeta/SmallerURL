import requests

url     = 'http://127.0.0.1:5000/api/shorten'
headers = {"Content-Type" : "application/json"}
randomStringURL = 'https://www.randomnumberapi.com/api/v1.0/randomstring'

for i in range(1):
    payload = { 'longURL' : f'https://www.example.com/'}
    # payload = { 'longURL' : f'https://www.amazon.in/ASUS-Marshmallow-Keyboard-Lightweight-Bluetooth/dp/B0CFF1XMT4/ref=pd_ci_mcx_mh_mcx_views_0_title?pd_rd_w=O6xI4&content-id=amzn1.sym.fa0aca50-60f7-47ca-a90e-c40e2f4b46a9%3Aamzn1.symc.ca948091-a64d-450e-86d7-c161ca33337b&pf_rd_p=fa0aca50-60f7-47ca-a90e-c40e2f4b46a9&pf_rd_r=1CNCFM0YJ2X31EYW6YMY&pd_rd_wg=QLjhk&pd_rd_r=a2dde6c2-d9e5-493b-811d-583ae1a36b7b&pd_rd_i=B0CFF1XMT4&th=1'}
    res = requests.post(url, json=payload, headers=headers)
    print (res.text)

# randomString = requests.get(randomStringURL).json()[0]
# print(randomString)