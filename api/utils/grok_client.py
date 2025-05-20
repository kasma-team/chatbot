import requests
import os
# GROK_API_KEY  = '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'
def call_grok(query):
    api_key = os.getenv("GROK_API_KEY")
    print(f"API Key: {api_key}")
    url = os.getenv("GROK_API_URL")
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"query": query}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return "Sorry, I couldn’t process your request right now."