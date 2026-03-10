import os
from groq import Groq
from dotenv import load_dotenv

# Replace 'your_api_key_here' with the key you just copied
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# print(os.getenv("GROQ_API_KEY"))

def extract_carpool_info(user_message):
    system_prompt = """
    You are a specialized Carpool Data Extractor. 
    Your job is to take unstructured WhatsApp messages and convert them into a valid JSON object.
    
    Extract the following fields:
    1. 'type': Must be either 'offer' (if someone has a car) or 'request' (if someone needs a ride).
    2. 'source': Starting point (use 'Unknown' if not mentioned).
    3. 'destination': Ending point (use 'Unknown' if not mentioned).
    4. 'time': The departure time mentioned.
    5. 'seats': Number of seats offered or needed (default to 1 if not specified).
    follow the format strictly , in order and do not include any additional text.
    Return ONLY the JSON object. No conversational text.
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
#         "I need a ride to the stadium tonight at 7."
#     ]

#     for msg in test_messages:
#         print(f"Message: {msg}")
#         print(f"Extracted JSON: {extract_carpool_info(msg)}")
#         print("-" * 30)