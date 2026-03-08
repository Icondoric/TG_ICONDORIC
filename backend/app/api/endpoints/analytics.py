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

@router.get("/users-report")
async def get_users_report(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    has_cv: Optional[bool] = Query(None),
    profile_complete: Optional[bool] = Query(None),
    completeness_min: Optional[float] = Query(None),
    cv_updated_since: Optional[str] = Query(None),
    carrera: Optional[str] = Query(None),
    current_user: dict = Depends(verify_operator_access)
):
    """
    Reporte detallado de usuarios con filtros extendidos.
    """
    try:
        query = supabase.table("usuarios").select("id, email, nombre_completo, rol, created_at")
        query = apply_date_filter(query, "created_at", start_date, end_date)

        if role:
            query = query.eq("rol", role)

        response = query.order("created_at", desc=True).execute()
        users = response.data

        # Fetch extended profile info for all users
        profile_response = supabase.table("perfiles_profesionales") \
            .select("usuario_id, is_complete, cv_filename, cv_uploaded_at, completeness_score, updated_at, carrera, semestre_actual, hard_skills, soft_skills, nombre_completo") \
            .execute()

        profiles_map = {}
        for p in profile_response.data:
            profiles_map[p['usuario_id']] = p

        result_users = []
        for user in users:
            profile = profiles_map.get(user['id'], {})
            has_cv_flag = bool(profile.get('cv_filename'))
            is_complete = profile.get('is_complete', False)
            score = float(profile.get('completeness_score', 0))
            cv_uploaded_at = profile.get('cv_uploaded_at')
            perfil_updated_at = profile.get('updated_at')
            carrera_val = profile.get('carrera')
            semestre_val = profile.get('semestre_actual')
            hard_skills = profile.get('hard_skills') or []
            soft_skills = profile.get('soft_skills') or []

            # Apply client-side filters
            if has_cv is not None and has_cv_flag != has_cv:
                continue
            if profile_complete is not None and is_complete != profile_complete:
                continue
            if completeness_min is not None and (score * 100) < completeness_min:
                continue
            if cv_updated_since and cv_uploaded_at:
                if cv_uploaded_at[:10] < cv_updated_since:
                    continue
            if carrera and carrera_val and carrera.lower() not in carrera_val.lower():
                continue

            result_users.append({
                "id": user['id'],
                "email": user['email'],
                "nombre_completo": user.get('nombre_completo') or profile.get('nombre_completo'),
                "rol": user['rol'],
                "fecha_registro": user['created_at'],
                "tiene_cv": has_cv_flag,
                "perfil_completo": is_complete,
                "completeness_score": round(score * 100, 1),
                "cv_uploaded_at": cv_uploaded_at,
                "perfil_updated_at": perfil_updated_at,
                "carrera": carrera_val,
                "semestre_actual": semestre_val,
                "hard_skills_count": len(hard_skills),
                "soft_skills_count": len(soft_skills),
            })

        # Stats
        total = len(result_users)
        roles_count = Counter(u['rol'] for u in result_users)
        with_cv = sum(1 for u in result_users if u['tiene_cv'])
        complete = sum(1 for u in result_users if u['perfil_completo'])
        avg_score = round(sum(u['completeness_score'] for u in result_users) / total, 1) if total > 0 else 0

        return {
            "users": result_users,
            "stats": {
                "total": total,
                "by_role": dict(roles_count),
                "with_cv": with_cv,
                "with_cv_pct": round((with_cv / total * 100), 1) if total > 0 else 0,
                "profile_complete": complete,
                "profile_complete_pct": round((complete / total * 100), 1) if total > 0 else 0,
                "avg_completeness": avg_score
            }
        }
    except Exception as e:
        print(f"Error fetching users report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/offers-report")
async def get_offers_report(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    tipo: Optional[str] = Query(None),
    estado: Optional[str] = Query(None),
    modalidad: Optional[str] = Query(None),
    sector: Optional[str] = Query(None),
    institucion: Optional[str] = Query(None),
    area: Optional[str] = Query(None),
    # Nuevos filtros por perfil de postulante
    con_postulaciones: Optional[bool] = Query(None),
    rol_postulante: Optional[str] = Query(None),
    carrera_postulante: Optional[str] = Query(None),
    min_postulaciones: Optional[int] = Query(None),
    min_score: Optional[float] = Query(None),
    current_user: dict = Depends(verify_operator_access)
):
    """
    Reporte detallado de ofertas laborales con filtros extendidos,
    incluyendo segmentacion por rol y carrera de postulantes.
    """
    try:
        query = supabase.table("ofertas_laborales") \
            .select("*, institutional_profiles(institution_name, sector)")
        query = apply_date_filter(query, "created_at", start_date, end_date)

        if tipo:
            query = query.eq("tipo", tipo)
        if modalidad:
            query = query.eq("modalidad", modalidad)

        response = query.order("created_at", desc=True).execute()
        ofertas = response.data

        # Fetch postulaciones with usuario_id for role/career breakdown
        postulaciones_resp = supabase.table("postulaciones") \
            .select("oferta_id, match_score, clasificacion, usuario_id") \
            .execute()

        # Build user role map: usuario_id -> rol
        users_resp = supabase.table("usuarios").select("id, rol").execute()
        user_rol_map: Dict[str, str] = {u['id']: u.get('rol', '') for u in users_resp.data}

        # Build user carrera map: usuario_id -> carrera
        profiles_resp = supabase.table("perfiles_profesionales") \
            .select("usuario_id, carrera").execute()
        user_carrera_map: Dict[str, str] = {
            p['usuario_id']: p['carrera']
            for p in profiles_resp.data if p.get('carrera')
        }

        # Build enriched post_map: oferta_id -> [postulacion + rol + carrera]
        post_map: Dict[str, List] = {}
        for p in postulaciones_resp.data:
            oid = p['oferta_id']
            uid = p.get('usuario_id')
            post_map.setdefault(oid, []).append({
                **p,
                'rol': user_rol_map.get(uid, '') if uid else '',
                'carrera': user_carrera_map.get(uid, '') if uid else '',
            })

        today_dt = datetime.now()
        today = today_dt.strftime("%Y-%m-%d")

        result_ofertas = []
        for o in ofertas:
            is_active = o.get('is_active', True)
            fecha_cierre = o.get('fecha_cierre')
            is_expired = bool(fecha_cierre and fecha_cierre < today)

            if is_expired:
                oferta_estado = 'expirada'
            elif is_active:
                oferta_estado = 'activa'
            else:
                oferta_estado = 'inactiva'

            if estado and oferta_estado != estado:
                continue

            inst = o.get('institutional_profiles') or {}
            inst_name = inst.get('institution_name') or ''
            inst_sector = inst.get('sector') or ''

            if sector and sector.lower() not in inst_sector.lower():
                continue
            if institucion and institucion.lower() not in inst_name.lower():
                continue
            area_val = o.get('area') or ''
            if area and area.lower() not in area_val.lower():
                continue

            # Postulaciones stats
            posts = post_map.get(o['id'], [])
            total_posts = len(posts)
            scores = [p['match_score'] for p in posts if p.get('match_score') is not None]
            avg_score = round(sum(scores) / len(scores) * 100, 1) if scores else None
            aptos = sum(1 for p in posts if p.get('clasificacion') == 'APTO')
            considerados = sum(1 for p in posts if p.get('clasificacion') == 'CONSIDERADO')
            no_aptos = sum(1 for p in posts if p.get('clasificacion') == 'NO_APTO')

            # Role breakdown of applicants
            n_estudiantes = sum(1 for p in posts if p.get('rol') == 'estudiante')
            n_titulados = sum(1 for p in posts if p.get('rol') == 'titulado')

            # Top 3 careers of applicants
            carrera_counter = Counter(p['carrera'] for p in posts if p.get('carrera'))
            top_carreras = [c for c, _ in carrera_counter.most_common(3)]

            # Apply new filters
            if con_postulaciones is True and total_posts == 0:
                continue
            if min_postulaciones is not None and total_posts < min_postulaciones:
                continue
            if min_score is not None and (avg_score is None or avg_score < min_score):
                continue
            if rol_postulante == 'estudiante' and n_estudiantes == 0:
                continue
            if rol_postulante == 'titulado' and n_titulados == 0:
                continue
            if carrera_postulante and not any(
                carrera_postulante.lower() in c.lower() for c in carrera_counter
            ):
                continue

            # Days remaining
            dias_restantes = None
            if fecha_cierre and oferta_estado == 'activa':
                try:
                    cierre_dt = datetime.strptime(fecha_cierre, "%Y-%m-%d")
                    dias_restantes = (cierre_dt - today_dt).days
                except Exception:
                    pass

            result_ofertas.append({
                "id": o['id'],
                "titulo": o['titulo'],
                "tipo": o['tipo'],
                "modalidad": o.get('modalidad'),
                "area": area_val or None,
                "ubicacion": o.get('ubicacion'),
                "institucion": inst_name or None,
                "sector": inst_sector or None,
                "estado": oferta_estado,
                "fecha_inicio": o.get('fecha_inicio'),
                "fecha_cierre": fecha_cierre,
                "dias_restantes": dias_restantes,
                "cupos_disponibles": o.get('cupos_disponibles', 1),
                "created_at": o['created_at'],
                "updated_at": o.get('updated_at'),
                "total_postulaciones": total_posts,
                "avg_match_score": avg_score,
                "aptos": aptos,
                "considerados": considerados,
                "no_aptos": no_aptos,
                "postulantes_estudiantes": n_estudiantes,
                "postulantes_titulados": n_titulados,
                "top_carreras": top_carreras,
            })

        total = len(result_ofertas)
        activas = sum(1 for o in result_ofertas if o['estado'] == 'activa')
        inactivas = sum(1 for o in result_ofertas if o['estado'] == 'inactiva')
        expiradas = sum(1 for o in result_ofertas if o['estado'] == 'expirada')
        by_tipo = Counter(o['tipo'] for o in result_ofertas)
        by_modalidad = Counter(o['modalidad'] for o in result_ofertas if o.get('modalidad'))
        total_posts_all = sum(o['total_postulaciones'] for o in result_ofertas)
        all_scores = [o['avg_match_score'] for o in result_ofertas if o['avg_match_score'] is not None]
        avg_score_global = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0

        # Global carrera stats across all filtered offers
        global_carrera = Counter()
        for o in result_ofertas:
            global_carrera.update({c: 1 for c in o['top_carreras']})
        top_carreras_global = dict(global_carrera.most_common(8))

        return {
            "ofertas": result_ofertas,
            "stats": {
                "total": total,
                "activas": activas,
                "inactivas": inactivas,
                "expiradas": expiradas,
                "by_tipo": dict(by_tipo),
                "by_modalidad": dict(by_modalidad),
                "total_postulaciones": total_posts_all,
                "avg_match_score": avg_score_global,
                "postulantes_estudiantes": sum(o['postulantes_estudiantes'] for o in result_ofertas),
                "postulantes_titulados": sum(o['postulantes_titulados'] for o in result_ofertas),
                "top_carreras": top_carreras_global,
            }
        }
    except Exception as e:
        print(f"Error fetching offers report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profiles-report")
async def get_profiles_report(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    sector: Optional[str] = Query(None),
    estado: Optional[str] = Query(None),
    nombre: Optional[str] = Query(None),
    current_user: dict = Depends(verify_operator_access)
):
    """
    Reporte detallado de perfiles institucionales con filtros extendidos.
    """
    try:
        query = supabase.table("institutional_profiles").select("*")
        query = apply_date_filter(query, "created_at", start_date, end_date)
        response = query.order("created_at", desc=True).execute()
        profiles = response.data

        # Offers count per institution
        today = datetime.now().strftime("%Y-%m-%d")
        offers_resp = supabase.table("ofertas_laborales") \
            .select("id, institutional_profile_id, is_active, fecha_cierre") \
            .execute()

        offers_map: Dict[str, Dict] = {}
        oferta_inst_map: Dict[str, str] = {}
        for o in offers_resp.data:
            iid = o.get('institutional_profile_id')
            oid = o.get('id')
            if iid:
                oferta_inst_map[oid] = iid
                if iid not in offers_map:
                    offers_map[iid] = {'total': 0, 'activas': 0}
                offers_map[iid]['total'] += 1
                is_active = o.get('is_active', True)
                fecha_cierre = o.get('fecha_cierre')
                if is_active and not (fecha_cierre and fecha_cierre < today):
                    offers_map[iid]['activas'] += 1

        # Postulaciones count per institution (through offers)
        post_resp = supabase.table("postulaciones").select("oferta_id").execute()
        post_by_inst: Dict[str, int] = {}
        for p in post_resp.data:
            iid = oferta_inst_map.get(p.get('oferta_id'))
            if iid:
                post_by_inst[iid] = post_by_inst.get(iid, 0) + 1

        result_profiles = []

        for p in profiles:
            inst_name = p.get('institution_name') or ''
            inst_sector = p.get('sector') or ''
            is_active = p.get('is_active', True)

            # Apply client-side filters
            if sector and sector.lower() not in inst_sector.lower():
                continue
            if nombre and nombre.lower() not in inst_name.lower():
                continue
            if estado == 'activo' and not is_active:
                continue
            if estado == 'inactivo' and is_active:
                continue

            inst_offers = offers_map.get(p['id'], {'total': 0, 'activas': 0})

            result_profiles.append({
                "id": p['id'],
                "institution_name": inst_name or None,
                "sector": inst_sector or None,
                "ubicacion": p.get('ubicacion'),
                "contact_email": p.get('contact_email'),
                "contact_phone": p.get('contact_phone'),
                "is_active": is_active,
                "total_ofertas": inst_offers['total'],
                "ofertas_activas": inst_offers['activas'],
                "total_postulaciones": post_by_inst.get(p['id'], 0),
                "created_at": p['created_at'],
                "updated_at": p.get('updated_at'),
            })

        total = len(result_profiles)
        activos = sum(1 for p in result_profiles if p['is_active'])
        by_sector = Counter(p['sector'] for p in result_profiles if p.get('sector'))
        total_ofertas_activas = sum(p['ofertas_activas'] for p in result_profiles)
        total_postulaciones = sum(p['total_postulaciones'] for p in result_profiles)

        return {
            "profiles": result_profiles,
            "stats": {
                "total": total,
                "activos": activos,
                "inactivos": total - activos,
                "by_sector": dict(by_sector),
                "total_ofertas_activas": total_ofertas_activas,
                "total_postulaciones": total_postulaciones,
            }
        }
    except Exception as e:
        print(f"Error fetching profiles report: {e}")
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
