from supabase import create_client, Client
import dotenv
import os
from brain import extract_carpool_info


SUPABASE_URL=os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY=os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

sample=extract_carpool_info("Heading to the mall at 5pm, 2 seats free")
print(sample)