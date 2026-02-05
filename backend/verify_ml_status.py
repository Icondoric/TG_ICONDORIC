
import sys
import os
from pathlib import Path

# Add app to path
sys.path.append(os.path.join(os.getcwd(), 'app'))

try:
    from app.services.ml_integration_service import get_ml_service
    
    print("Initializing ML Service...")
    ml_service = get_ml_service()
    
    print(f"Is Ready: {ml_service.is_ready}")
    
    if ml_service.is_ready:
        print("Model Info:", ml_service.get_model_info())
    else:
        print("Model failed to load.")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
