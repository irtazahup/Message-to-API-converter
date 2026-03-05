from flask import Flask, request, jsonify
from brain import extract_carpool_info # Your Sprint 1 logic
from database_ingestion import save_to_supabase  # Wrap your Sprint 2 code in a function

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    data = request.json
    
    # 1. Check if this is actually a message (Green-API sends other status updates too)
    if data.get('typeWebhook') == 'incomingMessageReceived':
        
        # 2. Safety check for the text data
        # We use .get() and multiple steps to avoid the KeyError
        message_data = data.get('messageData', {})
        text_data = message_data.get('textMessageData', {})
        message_text = text_data.get('textMessage')

        # Only proceed if there is actual text
        if message_text:
            sender_data = data.get('senderData', {})
            sender_number = sender_data.get('sender', 'Unknown')

            print(f"✅ New Message: {message_text}")
            
            # Now trigger your Sprint 1 & 2 logic
            try:
                # Use your existing logic here
                raw_ai_output = extract_carpool_info(message_text)
                save_to_supabase(raw_ai_output, sender_number)
                # ... save to supabase ...
                print("🚀 Successfully processed!")
            except Exception as ai_err:
                print(f"❌ AI Error: {ai_err}")
        else:
            print("ℹ️ Received a message but it had no text (maybe an image or emoji?)")

    return jsonify({"status": "success"}), 200
if __name__ == '__main__':
    app.run(port=5000)