import os
import asyncio
import requests
from supabase import acreate_client, AsyncClient
from dotenv import load_dotenv

load_dotenv()

# --- Config ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
ID_INSTANCE = os.getenv("idInstance")
API_TOKEN = os.getenv("apiTokenInstance")
CONTACT_NUMBER = os.getenv("CHAT_NUM")# The number you want to send messages to (for testing)


def send_whatsapp(number, text):
    # print(f"📤 Sending to {number}: {text}")
    """Sends a message via Green-API (Keep this sync or make it async)"""
    url = f"https://7103.api.greenapi.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    if "@c.us" not in str(number):
        number = f"{number}@c.us"
    
    payload = {"chatId": number, "message": text}
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        # print(f"🚀 Sent to {number}: {response.status_code}")
    except Exception as e:
        print(f"❌ Green-API Error: {e}")

# The callback must be a regular function, but we can trigger logic from it
def on_insert(payload):
    # 1. Debug: See exactly what Supabase sent
    
    
    # 2. Extract the record. Python SDK typically uses 'record' for INSERTs
    # but some versions/configs use 'new'
    # print(f"DEBUG - Full Payload: {payload}")
    
    # 1. Access the 'data' key first, then 'record'
    data = payload.get('data', {})
    new_record = data.get('record') or data.get('new')

    if not new_record:
        print("❌ Error: Still couldn't find the record. Check the DEBUG print above.")
        return

    # 3. Use the exact column names from your Supabase table
    # Example: If your DB column is 'source_loc', use new_record.get('source_loc')
    car_type = new_record.get('type', 'Unknown')
    src = new_record.get('source', 'Unknown')
    dest = new_record.get('destination', 'Unknown')
    tm = new_record.get('time', 'Not specified')
    st = new_record.get('seats', '0')
    sender = new_record.get('sender_num', 'Unknown')

    # ... (Your WhatsApp sending logic)
    message = f"🚗 New Carpool Alert!\nType: {car_type}\nFrom: {src}\nTo: {dest}\nTime: {tm}\nSeats: {st}\nContact: {sender}"
    send_whatsapp(CONTACT_NUMBER, message)
    

async def main():
    # Initialize the ASYNC client
    supabase: AsyncClient = await acreate_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("👂 Listener is starting...")
    
    # Set up the channel
    channel = supabase.channel('db-changes')
    await channel.on_postgres_changes(
        event="INSERT",
        schema="public",
        table="carpool_entries", # <--- CHANGE THIS
        callback=on_insert
    ).subscribe()

    # Keep the script running
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Stopping...")

if __name__ == "__main__":
    asyncio.run(main())