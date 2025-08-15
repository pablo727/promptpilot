# scripts/run_prompt.py

import json
import requests
from utils.token_utils import update_headers

BASE_URL = "http://127.0.0.1:8000/api/v1/playgrounds/run/"


def run_prompt(prompt_text):
    headers = update_headers()
    payload = {"prompt": prompt_text, "model": "mistral", "variables": {}}

    print(f"📨 Sending prompt: {prompt_text}")
    response = requests.post(BASE_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        print("\n✅ Response:")
        print(json.dumps(data, indent=2))
    else:
        print(f"\n❌ Error {response.status_code}: {response.text}")


if __name__ == "__main__":
    run_prompt("Write me a short motivational quote about coding.")
