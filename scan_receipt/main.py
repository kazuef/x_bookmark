import os
import requests
from dotenv import load_dotenv

load_dotenv("env/.env")

dify_api_key = os.environ.get("DIFY_API_KEY")

url = 'http://localhost/v1/files/upload'
file_path = "/Users/tokunoukazuki/Downloads/bookmarks.csv"
mime_tyoe = "document/csv"

headers = {
    "Authorization": f"Bearer {dify_api_key}" 
}

files = {
    "file": (file_path, open(file_path, "rb"), mime_type)
}

data = {
    "user": "kazuki-001"
}

response = requests.post(url, headers=headers, files=files, data=data)

print(response)
# <Response [200]>

print(type(response))
# <class 'requests.models.Response'>




url = 'http://localhost/v1/workflows/run'