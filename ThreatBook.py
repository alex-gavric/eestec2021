import requests

url = "https://api.threatbook.cn/v3/ip/query"

query = {
  "apikey":"请替换apikey",
  "resource":"159.203.93.255"
}

response = requests.request("GET", url, params=query)

print(response.json())