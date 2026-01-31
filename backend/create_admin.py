import os
import sys
from dotenv import load_dotenv

# Add backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from app.core.config import settings
from app.core.security import get_password_hash
from supabase import create_client

def create_admin(email, password):
    print(f"Attempting to create admin user: {email}")
    
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_KEY
    
    if not url or not key:
        print("Error: SUPABASE_URL or SUPABASE_KEY not set in .env")
        return

    try:
        supabase = create_client(url, key)
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        return

    # Check if user exists
    try:
        res = supabase.table("usuarios").select("id").eq("email", email).execute()
        if res.data:
            print(f"User with email '{email}' already exists.")
            return
    except Exception as e:
        print(f"Error checking existing user: {e}")
        return

    hashed = get_password_hash(password)
    
    user_data = {
        "email": email,
        "password_hash": hashed,
        "rol": "administrador",
        "nombre_completo": "Admin User"
    }
    
    try:
        print("Inserting user into 'usuarios' table...")
        res = supabase.table("usuarios").insert(user_data).execute()
        
        if res.data:
            user_id = res.data[0]['id']
            print(f"User created with ID: {user_id}. Creating profile...")
            
            # Create empty profile
            supabase.table("perfiles_profesionales").insert({"usuario_id": user_id}).execute()
            print("Profile created successfully.")
            print(f"\nSUCCESS: Admin user '{email}' created.")
            print(f"Password: {password}")
        else:
            print("Failed to create user (no data returned).")
            
    except Exception as e:
        print(f"Error creating user: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        create_admin(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python create_admin.py <email> <password>")
        print("Using default credentials...")
        create_admin("admin@example.com", "admin123")
