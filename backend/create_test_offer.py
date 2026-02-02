
import os
import sys
from datetime import date, timedelta

# Add backend directory to path
sys.path.append(os.getcwd())

from app.db.client import supabase
from app.services.oferta_service import get_oferta_service

def create_offer():
    print("--- Creating Test Offer ---")
    
    # 1. Get a profile
    response = supabase.table("institutional_profiles").select("id, institution_name, sector, requirements").limit(1).execute()
    if not response.data:
        print("No institutional profiles found. Cannot create offer.")
        return

    profile = response.data[0]
    print(f"Using profile: {profile['institution_name']} ({profile['id']})")
    
    # 2. Create offer data
    oferta_service = get_oferta_service()
    
    # Use profile requirements as offer requirements
    reqs = profile.get('requirements', {})
    
    offer_data = {
        'titulo': f"Pasantia en {profile['institution_name']}",
        'descripcion': "Esta es una pasantia de prueba generada automaticamente para validar el sistema de recomendaciones.",
        'tipo': 'pasantia',
        'modalidad': 'hibrido',
        'ubicacion': 'La Paz, Bolivia',
        'institutional_profile_id': profile['id'],
        'requisitos_especificos': reqs,
        'fecha_inicio': date.today().isoformat(),
        'fecha_cierre': (date.today() + timedelta(days=30)).isoformat(),
        'cupos_disponibles': 5
    }
    
    # 3. Insert offer
    # We need a user ID for 'created_by'. I'll try to find an admin user or just use a placeholder if DB allows.
    # Looking for a user...
    try:
        user_resp = supabase.table("usuarios").select("id").limit(1).execute()
        user_id = user_resp.data[0]['id'] if user_resp.data else "00000000-0000-0000-0000-000000000000"
    except Exception as e:
        print(f"Error fetching user: {e}")
        user_id = "00000000-0000-0000-0000-000000000000"
    
    print(f"Creating offer for user: {user_id}")
    
    try:
        oferta = oferta_service.create_oferta(offer_data, created_by=user_id)
        print(f"Successfully created offer: {oferta['id']}")
        print(f"Title: {oferta['titulo']}")
    except Exception as e:
        print(f"Error creating offer: {e}")

if __name__ == "__main__":
    create_offer()
