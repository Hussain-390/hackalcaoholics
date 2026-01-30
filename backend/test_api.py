import requests
import json

# Test the backend
url = "http://localhost:8000/research/start"
data = {"query": "test query"}

print("🧪 Testing backend endpoint...")
print(f"URL: {url}")
print(f"Data: {data}")

try:
    response = requests.post(url, json=data)
    print(f"\n✅ Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"Response: {response.text if 'response' in locals() else 'No response'}")
