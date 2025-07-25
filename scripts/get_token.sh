#!/usr/bin/env bash

# get_token.sh - Automatically fetch a new access token and save it to the root .env

API_URL="http://127.0.0.1:8000/api/v1/token/"
USERNAME=${1:-admin}
PASSWORD=${2:-pablosk8}

# Path to your project root .env
ENV_FILE="$(dirname "$0")/../.env"

# Fetch token
RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/token/ \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}")

# DEBUG: Print raw response for inspection
echo "🔍 Raw response: $RESPONSE"

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
  echo "✅ Access token saved to .env in project root and exported to shell."
else
  echo "❌ Failed to get token. Response:"
  echo "$RESPONSE"
fi
