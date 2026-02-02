
import os
import sys
from pprint import pprint

# Add backend directory to path
sys.path.append(os.getcwd())

from app.services.oferta_service import get_oferta_service
from app.services.recommendation_service import get_recommendation_service

def debug_offers():
    print("--- Debugging Offers ---")
    oferta_service = get_oferta_service()
    
    # List all internships
    print("\nListing active internships (pasantia):")
    try:
        pasantias = oferta_service.list_ofertas(
            tipo='pasantia',
            is_active=True,
            include_expired=False,
            page_size=20
        )
        print(f"Found {pasantias['total']} active internships.")
        for oferta in pasantias['ofertas']:
            print(f"- ID: {oferta['id']}")
            print(f"  Title: {oferta['titulo']}")
            print(f"  Institution: {oferta.get('institution_name')}")
            print(f"  Close Date: {oferta.get('fecha_cierre')}")
            print(f"  Active: {oferta.get('is_active')}")
            
    except Exception as e:
        print(f"Error listing internships: {e}")

    # List all jobs to check if maybe they are categorized as jobs
    print("\nListing active jobs (empleo):")
    try:
        empleos = oferta_service.list_ofertas(
            tipo='empleo',
            is_active=True,
            include_expired=False,
            page_size=20
        )
        print(f"Found {empleos['total']} active jobs.")
        for oferta in empleos['ofertas']:
            print(f"- ID: {oferta['id']}")
            print(f"  Title: {oferta['titulo']}")
            
    except Exception as e:
        print(f"Error listing jobs: {e}")

    # List institutional profiles
    print("\nListing institutional profiles:")
    try:
        from app.db.client import supabase
        response = supabase.table("institutional_profiles").select("id, institution_name").execute()
        if response.data:
            print(f"Found {len(response.data)} profiles.")
            for p in response.data:
                print(f"- {p['institution_name']} ({p['id']})")
        else:
            print("No institutional profiles found.")
    except Exception as e:
        print(f"Error listing profiles: {e}")


if __name__ == "__main__":
    import sys
    with open("debug_output.txt", "w") as f:
        sys.stdout = f
        debug_offers()
