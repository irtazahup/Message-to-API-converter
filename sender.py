import asyncio
import os
import requests
from dotenv import load_dotenv
from supabase import create_async_client, AsyncClient

load_dotenv()

# Credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
ID_INSTANCE = os.getenv("idInstance")
API_TOKEN_INSTANCE = os.getenv("apiTokenInstance")
CHAT_NUM = os.getenv("CHAT_NUM")
CHAT_ID = f"{CHAT_NUM}@c.us"

def send_whatsapp_message(text):
    url = f"https://api.green-api.com{ID_INSTANCE}/sendMessage/{API_TOKEN_INSTANCE}"
    payload = {"chatId": CHAT_ID, "message": text}
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Green API Error: {e}")
        return False

async def handle_insert(payload, supabase: AsyncClient):
    # Data is inside the 'new' key for INSERT events
    new_row = payload.get('new', {})
    row_id = new_row.get('id')
    
    if not row_id:
        return

    message_text = (
        "*NEW MESSAGE FROM CARPOOL-BOT*\n\n"
        f"From: {new_row.get('sender_number')}\n"
        f"Type: {new_row.get('type')}\n"
        f"Source: {new_row.get('source')}\n"
        f"Destination: {new_row.get('destination')}\n"
        f"Time: {new_row.get('time')}\n"
        f"Seats: {new_row.get('seats')}"
    )

    print(f"Processing row {row_id}...")

    if send_whatsapp_message(message_text):
        # Update row status to True
        await supabase.table("carpool_entries").update({"status": True}).eq("id", row_id).execute()
        print(f"Success: Row {row_id} updated.")

async def main():
    # 1. Initialize Async Client
    supabase: AsyncClient = await create_async_client(SUPABASE_URL, SUPABASE_KEY)

    # 2. Setup the channel
    channel = supabase.channel("db-changes")
    
    # 3. Use the correct method: on_postgres_changes
    channel.on_postgres_changes(
        event="INSERT",
        schema="public",
        table="carpool_entries",
        callback=lambda payload: asyncio.create_task(handle_insert(payload, supabase))
    )
    
    # 4. Subscribe to start receiving events
    await channel.subscribe()

    print("Listener active. Waiting for new carpool entries...")
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")

if __name__ == "__main__":
    asyncio.run(main())
