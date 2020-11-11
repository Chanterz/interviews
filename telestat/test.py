import json

import requests
response = requests.post('http://localhost:8000/request_doc_signing', json={'name': 'my doc', 'recipients': ['john', 'patrick'], 'url': '123'})
print(response.json())
