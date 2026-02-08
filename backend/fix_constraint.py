
import asyncio
from app.db.client import supabase

async def update_role_constraint():
    try:
        # SQL to drop the old constraint and add the new one
        sql = """
        ALTER TABLEUsuarios DROP CONSTRAINT IF EXISTS usuarios_rol_check;
        ALTER TABLE usuarios ADD CONSTRAINT usuarios_rol_check 
        CHECK (rol IN ('estudiante', 'titulado', 'administrador', 'admin', 'operador'));
        """
        
        # Execute the SQL directly using the rpc or a direct query if possible.
        # Since supabase-py client might not expose direct SQL execution easily for schema changes 
        # without a stored procedure, we might strictly need to use the dashboard or a migration tool.
        # However, for this environment, let's try to use the `rpc` if there is a 'exec_sql' function
        # or just print the SQL for the user if we can't run it.
        
        # BUT, wait, we are in a python environment. 
        # The supabase client usually interacts with the REST API (PostgREST).
        # Schema changes via PostgREST are not allowed typically unless we have a specific function.
        
        print("--- INSTRUCCIONES MANUALES ---")
        print("Debido a restricciones de seguridad de la API, por favor ejecuta el siguiente SQL en el editor SQL de Supabase:")
        print(sql)
        print("------------------------------")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(update_role_constraint())
