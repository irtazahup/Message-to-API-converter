from supabase import create_client, Client
import dotenv
import os
from brain import extract_carpool_info
import json

dotenv.load_dotenv()

SUPABASE_URL=os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY=os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def save_to_supabase(sample, sender_number):
    

# 3. Now you can add the manual field
    sample['user_name'] = 'Whatsapp User'
    sample['sender_num'] = sender_number
    sample['status'] = False  # You can set a default status or any other field you want
    try:
        response = supabase.table("carpool_entries").insert(sample).execute()
        
    except Exception as e:
        print("Error inserting data:", e)
        
# sample_raw=extract_carpool_info("Heading to the mall at 5pm, 2 seats free")

# sample = json.loads(sample_raw)

# # # 3. Now you can add the manual field
# # sample['user_name'] = 'Whatsapp User'
# # sample['sender_num'] = '923118375964'
# # sample['status'] = False  # You can set a default status or any other field you

# save_to_supabase(sample_raw, '923118375964')