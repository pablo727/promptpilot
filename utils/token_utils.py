# utils/token_utils.py

import os
from dotenv import load_dotenv


def update_headers():
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
    load_dotenv(dotenv_path=dotenv_path)
    access_token = os.getenv("ACCESS_TOKEN")
    if not access_token:
        raise ValueError(
            "❌ ACCESS_TOKEN not found in .env — run scripts/get_token.sh first."
        )
    else:
        print(f"✅ Loaded token: {access_token[:40]}...")  # Print safely
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
