#!/usr/bin/env bash

# get_token.sh - Automatically fetch a new access token and save it to the root .env

API_URL="http://127.0.0.1:8000/api/v1/token/"
USERNAME=${1:-your-username-here}
PASSWORD=${2:-your-password-here}

# Path to your project root .env
ENV_FILE="$(dirname "$0")/../.env"

# Fetch token
RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/token/ \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}")


# Extract token
TOKEN=$(echo "$RESPONSE" | jq -r '.access')

# Save token to .env in root
if [ "$TOKEN" != "null" ] && [ -n "$TOKEN" ]; then
  if grep -q '^ACCESS_TOKEN=' "$ENV_FILE"; then
    sed -i "s|^ACCESS_TOKEN=.*|ACCESS_TOKEN=\"$TOKEN\"|" "$ENV_FILE"
  else
    echo "ACCESS_TOKEN=\"$TOKEN\"" >> "$ENV_FILE"
  fi
  export ACCESS_TOKEN="$TOKEN"
  echo "$TOKEN"
else
  echo "❌ Failed to get token. Response:" >&2
  echo "$RESPONSE" >&2
fi

