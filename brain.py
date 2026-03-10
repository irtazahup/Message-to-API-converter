import os
from groq import Groq
from dotenv import load_dotenv

# Replace 'your_api_key_here' with the key you just copied
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# print(os.getenv("GROQ_API_KEY"))

def extract_carpool_info(user_message):
    system_prompt = """
        You are a specialized Carpool Data Extractor. Your job is to classify and extract data from WhatsApp messages.

            ### CRITICAL INSTRUCTIONS:
            1. EVALUATE RELEVANCE: Determine if the message is a carpool 'offer' (driver with seats) or 'request' (passenger needing a ride).
            2. IF NOT RELEVANT: If the message is a greeting, spam, or unrelated to carpooling, return exactly this JSON: {"status": "ignored", "reason": "not important"}.
            3. IF RELEVANT: Extract the following fields into a valid JSON object:
                - 'type': Must be either 'offer' or 'request'.
                - 'source': The starting location.
                - 'destination': The ending location.
                - 'time': The departure time mentioned.
                - 'seats': Number of seats (default to 1 if not mentioned).
                - 'status': "captured"

            ### FORMATTING:
            Return ONLY the JSON object. Do not include any conversational text or explanations.
            """
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        model="llama-3.1-8b-instant", # This is a fast, free-tier model
        response_format={"type": "json_object"} # Forces the AI to return JSON
    )
    
    return chat_completion.choices[0].message.content

# if __name__ == "__main__":
# # # --- Testing Phase ---
#     test_messages = [
#         "Heading to the mall at 5pm, 2 seats free",
#         "Anyone going to the airport tomorrow morning around 8am? Need a lift.",
#         "Offer: Ride from Downtown to Tech Park at 09:00. 3 spots left!",
#         "I need a ride to the stadium tonight at 7.",
#         "I love to have you in me"
#     ]

#     for msg in test_messages:
#         print(f"Message: {msg}")
#         print(f"Extracted JSON: {extract_carpool_info(msg)}")
#         print("-" * 30)