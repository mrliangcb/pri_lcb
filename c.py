import requests

url = "http://10.0.2.120:50000/NLP/Algorithm/base/dup_check/winnowing?doc1=aa&doc2=ab"

payload = {}
headers= {}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
