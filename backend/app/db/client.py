from supabase import create_client, Client
from app.core.config import settings

# Initialize Supabase Client
try:
    settings.validate_setup()
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
except ValueError as e:
    print(f"WARNING: Database setup issue: {e}")
    # We allow the app to start so we can see the error, but DB calls will fail.
    supabase = None

def get_supabase_client() -> Client:
    return supabase
