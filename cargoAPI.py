import requests
from requests.auth import HTTPBasicAuth
method = "get"
api_key ="yhGyEqQFdDxQgmIUqB2kmS2yiZdp0RsPOQccu0VUX5hrpyFEMW54jpakNqvZ26Fu7bnAAJnNh_J6g1p6Yb09zmyLcM0_eQHvlYkp0Ww566yyhU1DH63NTlk06pW0YXYx"
url = "https://api.yelp.com/v3/businesses/search?location=NYC&categories=bars&open_now=true$limit=40&offset=40&key=yhGyEqQFdDxQgmIUqB2kmS2yiZdp0RsPOQccu0VUX5hrpyFEMW54jpakNqvZ26Fu7bnAAJnNh_J6g1p6Yb09zmyLcM0_eQHvlYkp0Ww566yyhU1DH63NTlk06pW0YXYx"

headers = {'Authorization': 'Bearer {}'.format(api_key)}
rsp = requests.request(method, url,headers={},data={})

print(rsp.text)