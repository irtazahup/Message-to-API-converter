from supabase import create_client, Client
import dotenv
import os
from brain import extract_carpool_info
import json

SUPABASE_URL=os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY=os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# sample_raw=extract_carpool_info("Heading to the mall at 5pm, 2 seats free")

# sample = json.loads(sample_raw)

# # 3. Now you can add the manual field
# sample['user_name'] = 'Whatsapp User'

# print(sample)
def save_to_supabase(extracted_data, sender_number):
    sample = json.loads(extracted_data)

# 3. Now you can add the manual field
    sample['user_name'] = 'Whatsapp User'
    sample['sender_num'] = sender_number
    try:
        response = supabase.table("carpool_entries").insert(sample).execute()
        print("Data inserted successfully:", response.data)
    except Exception as e:
        print("Error inserting data:", e)