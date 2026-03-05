import requests
import json
import os 
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().with_name(".env"))

# Your Green API credentials (replace with your actual values)
ID_INSTANCE = os.getenv("idInstance")
API_TOKEN_INSTANCE = os.getenv("apiTokenInstance")


print(f"ID_INSTANCE: {ID_INSTANCE}")
print(f"API_TOKEN_INSTANCE: {API_TOKEN_INSTANCE}")
# The recipient's phone number with country code, followed by "@c.us"
# Example: "79876543210@c.us"
CHAT_ID = "923118375964@c.us" 
MESSAGE_TEXT = "Hello from Green API!"

# The API URL for the sendMessage method
url = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN_INSTANCE}"

# The payload for the POST request
payload = json.dumps({
  "chatId": CHAT_ID,
  "message": MESSAGE_TEXT
})

# The headers for the POST request
headers = {
  'Content-Type': 'application/json'
}

try:
    # Send the request
    response = requests.request("POST", url, headers=headers, data=payload)
    print('successfull')
    # Print the response
    print(response.text)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")

