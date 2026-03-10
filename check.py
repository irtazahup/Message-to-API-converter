
from brain import extract_carpool_info
import json
from database_ingestion import save_to_supabase



raw_ai_output = extract_carpool_info("Hey there! Heading to the mall at 5pm, 2 seats free")
                # 2. Parse the string into a dictionary immediately
data_conv = json.loads(raw_ai_output)
if data_conv.get("status") != "ignored":
                    
    save_to_supabase(data_conv, '923118375964')
                    # ... save to supabase ...
    print("🚀 Successfully processed!")
else:
    print(raw_ai_output)