from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from collections import Counter

from app.api.dependencies import verify_admin_role, verify_operator_access
from app.db.client import supabase

router = APIRouter()

def apply_date_filter(query, date_field, start_date, end_date):
    if start_date:
        query = query.gte(date_field, start_date)
    if end_date:
        # Add 1 day to include the end date fully if it's just a date string
        # Assuming end_date comes as YYYY-MM-DD
        try:
             # Just a simple check, in real app might need more robustness
             if len(end_date) == 10: 
                 end_dt = datetime.fromisoformat(end_date) + timedelta(days=1)
                 end_date = end_dt.isoformat()
        except:
            pass
        query = query.lte(date_field, end_date)
    return query

@router.get("/users-summary")
async def get_users_summary(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_user: dict = Depends(verify_operator_access)
):
    """
    Obtener resumen de usuarios. 
    Total siempre es histórico.
    'Nuevos usuarios' respeta el filtro de fechas (o últimos 30 días por defecto).
    """
    try:
        # Total users (Always absolute)
        total_query = supabase.table("usuarios").select("*", count="exact", head=True).execute()
        total_users = total_query.count

        # By Role (Always absolute for distribution chart usually, but let's keep it absolute)
        estudiantes_query = supabase.table("usuarios").select("*", count="exact", head=True).eq("rol", "estudiante").execute()
        titulados_query = supabase.table("usuarios").select("*", count="exact", head=True).eq("rol", "titulado").execute()
        admins_query = supabase.table("usuarios").select("*", count="exact", head=True).eq("rol", "administrador").execute()

        # Users in period (New Users)
        recent_query = supabase.table("usuarios").select("*", count="exact", head=True)
        
        if start_date or end_date:
            recent_query = apply_date_filter(recent_query, "created_at", start_date, end_date)
        else:
            # Default to last 30 days
            last_month = (datetime.now() - timedelta(days=30)).isoformat()
            recent_query = recent_query.gt("created_at", last_month)
            
        recent_count = recent_query.execute().count

        return {
            "total_users": total_users,
            "roles": {
                "estudiante": estudiantes_query.count,
                "titulado": titulados_query.count,
                "administrador": admins_query.count
            },
            "new_users_in_period": recent_count
        }
    except Exception as e:
        print(f"Error fetching user summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user-growth")
async def get_user_growth(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_user: dict = Depends(verify_operator_access)
):
    """
    Obtener crecimiento de usuarios en el rango.
    """
    try:
        query = supabase.table("usuarios").select("created_at")
        query = apply_date_filter(query, "created_at", start_date, end_date)
        response = query.execute()
        
        growth_data = {}
        
        # Determine grouping based on range duration could be cool, but let's stick to monthly/daily
        # For simplicity, if range is small (< 60 days), group by day. Else group by month.
        
        by_day = False
        if start_date and end_date:
            try:
                s = datetime.fromisoformat(start_date)
                e = datetime.fromisoformat(end_date)
                if (e - s).days < 60:
                    by_day = True
            except:
                pass
        
        for user in response.data:
            if user.get("created_at"):
                dt = datetime.fromisoformat(user["created_at"].replace("Z", "+00:00"))
                
                if by_day:
                    key = dt.strftime("%Y-%m-%d")
                else:
                    key = dt.strftime("%Y-%m")
                    
                growth_data[key] = growth_data.get(key, 0) + 1

        # Fill gaps? (Optional, maybe later)

        # Sort by date
        sorted_data = dict(sorted(growth_data.items()))
        
        return {
            "labels": list(sorted_data.keys()),
            "data": list(sorted_data.values()),
            "grouped_by": "day" if by_day else "month"
        }
    except Exception as e:
        print(f"Error fetching user growth: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/skills-cloud")
async def get_skills_cloud(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_user: dict = Depends(verify_operator_access)
):
    """
    Obtener habilidades de perfiles actualizados en el rango.
    """
    try:
        query = supabase.table("perfiles_profesionales").select("hard_skills, soft_skills")
        # Filter by updated_at to reflect skills active/added in that period
        query = apply_date_filter(query, "updated_at", start_date, end_date)
        response = query.execute()
        
        hard_counter = Counter()
        soft_counter = Counter()
        
        for profile in response.data:
            h_skills = profile.get("hard_skills") or []
            s_skills = profile.get("soft_skills") or []
            
            for s in h_skills:
                if s: hard_counter[s.strip().lower()] += 1
                
            for s in s_skills:
                if s: soft_counter[s.strip().lower()] += 1
                
        # Get top 15
        top_hard = [{"name": k, "count": v} for k, v in hard_counter.most_common(15)]
        top_soft = [{"name": k, "count": v} for k, v in soft_counter.most_common(15)]
        
        return {
            "hard_skills": top_hard,
            "soft_skills": top_soft
        }
    except Exception as e:
        print(f"Error fetching skills cloud: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profile-completion")
async def get_profile_completion(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_user: dict = Depends(verify_operator_access)
):
    """
    Estadísticas sobre el estado de completitud.
    Nota: Las métricas totales suelen ser absolutas. 
    Aquí podríamos filtrar 'perfiles completados en el periodo', 
    pero la estructura actual ('is_complete' boolean) no tiene fecha de completitud.
    Usaremos 'updated_at' como proxy de actividad en el periodo.
    """
    try:
        # Users candidates (Always absolute total)
        users_query = supabase.table("usuarios").select("id", count="exact", head=True) \
            .neq("rol", "administrador").execute()
        total_candidates = users_query.count
        
        # Profiles active/updated in period
        query = supabase.table("perfiles_profesionales").select("is_complete, cv_filename", count="exact")
        query = apply_date_filter(query, "updated_at", start_date, end_date)
        response = query.execute()
        
        active_in_period = response.count # Profiles touched in this period
        data = response.data
        
        completed_count = sum(1 for p in data if p.get("is_complete"))
        with_cv_count = sum(1 for p in data if p.get("cv_filename"))
        
        return {
            "total_candidates": total_candidates,
            "profiles_active_in_period": active_in_period, # New metric
            "profiles_completed": completed_count,
            "profiles_with_cv": with_cv_count,
            "completion_rate": (completed_count / active_in_period * 100) if active_in_period > 0 else 0
        }
    except Exception as e:
        print(f"Error fetching profile stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
