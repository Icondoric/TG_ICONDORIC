"""
Admin Ranking Routes - Evaluación de Candidatos por Oferta
Endpoints para que administradores vean el ranking de candidatos
para cada oferta laboral, basado en las postulaciones realizadas.
"""

import io
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.api.dependencies import verify_admin_role
from app.db.client import supabase
from app.services.oferta_service import get_oferta_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin/ranking", tags=["Admin - Ranking Candidatos"])


@router.get("/convocatorias")
async def list_ofertas_con_stats(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo: 'pasantia' o 'empleo'"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    include_expired: bool = Query(True, description="Incluir ofertas expiradas"),
    search: Optional[str] = Query(None, description="Buscar por título"),
    current_user: dict = Depends(verify_admin_role)
):
    """
    Lista todas las ofertas laborales (activas y pasadas) con estadísticas
    de postulaciones: total, clasificación y mejor puntaje obtenido.
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

    try:
        query = supabase.table("convocatorias_laborales") \
            .select(
                "id, titulo, tipo, modalidad, ubicacion, area, descripcion,"
                " cupos_disponibles, is_active, fecha_inicio, fecha_cierre,"
                " contact_email, contact_phone, requirements, weights, thresholds,"
                " institutional_profile_id, created_at,"
                " institutional_profiles(institution_name, sector)"
            ) \
            .order("created_at", desc=True)

        if tipo:
            query = query.eq("tipo", tipo)
        if is_active is not None:
            query = query.eq("is_active", is_active)

        response = query.execute()
        ofertas = response.data or []

        # Filtro de búsqueda por título (client-side, dataset pequeño)
        if search:
            search_lower = search.lower()
            ofertas = [o for o in ofertas if search_lower in o.get("titulo", "").lower()]

        result = []
        for oferta in ofertas:
            inst = oferta.pop("institutional_profiles", None) or {}
            oferta["institution_name"] = inst.get("institution_name")
            oferta["sector"] = inst.get("sector")

            # Estadísticas de postulaciones para esta oferta
            stats_resp = supabase.table("postulaciones") \
                .select("clasificacion, match_score") \
                .eq("oferta_id", oferta["id"]) \
                .execute()

            posts = stats_resp.data or []
            scores = [p["match_score"] for p in posts if p.get("match_score") is not None]

            oferta["stats"] = {
                "total": len(posts),
                "apto": sum(1 for p in posts if p.get("clasificacion") == "APTO"),
                "considerado": sum(1 for p in posts if p.get("clasificacion") == "CONSIDERADO"),
                "no_apto": sum(1 for p in posts if p.get("clasificacion") == "NO_APTO"),
                "mejor_puntaje": round(max(scores) * 100) if scores else None,
                "promedio_puntaje": round(sum(scores) / len(scores) * 100) if scores else None,
            }
            result.append(oferta)

        return {"ofertas": result, "total": len(result)}

    except Exception as e:
        logger.error(f"Error listando ofertas para ranking: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/convocatorias/{oferta_id}/candidatos")
async def get_ranking_candidatos(
    oferta_id: str,
    top_n: int = Query(default=3, ge=1, le=20, description="Número de candidatos a mostrar"),
    current_user: dict = Depends(verify_admin_role)
):
    """
    Obtiene el ranking de los mejores candidatos para una oferta laboral.

    Retorna los top_n usuarios con mayor puntaje de correspondencia,
    ordenados de forma descendente, incluyendo:
    - Datos del perfil profesional (nombre, contacto, skills)
    - Resultado de evaluación ML (scores, clasificación, match details)
    - Justificación detallada de la selección
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

    try:
        # Detalle completo de la oferta
        oferta_service = get_oferta_service()
        oferta = oferta_service.get_oferta(oferta_id)
        if not oferta:
            raise HTTPException(status_code=404, detail="Oferta no encontrada")

        # Top N postulaciones ordenadas por puntaje
        posts_resp = supabase.table("postulaciones") \
            .select("*") \
            .eq("oferta_id", oferta_id) \
            .order("match_score", desc=True) \
            .limit(top_n) \
            .execute()

        posts = posts_resp.data or []

        # Total de postulantes (para contexto)
        total_resp = supabase.table("postulaciones") \
            .select("id", count="exact") \
            .eq("oferta_id", oferta_id) \
            .execute()
        total_postulantes = total_resp.count or len(posts)

        candidatos = []
        for rank, post in enumerate(posts, start=1):
            usuario_id = post["usuario_id"]

            # Perfil profesional del candidato
            perfil_resp = supabase.table("perfiles_profesionales") \
                .select(
                    "nombre_completo, email_contacto, telefono, direccion,"
                    " hard_skills, soft_skills, education_level, experience_years,"
                    " languages, cv_filename, completeness_score"
                ) \
                .eq("usuario_id", usuario_id) \
                .execute()
            perfil = perfil_resp.data[0] if perfil_resp.data else {}

            # Datos básicos del usuario (email, rol)
            usuario_resp = supabase.table("usuarios") \
                .select("email, nombre_completo, rol") \
                .eq("id", usuario_id) \
                .execute()
            usuario = usuario_resp.data[0] if usuario_resp.data else {}

            candidatos.append({
                "rank": rank,
                "usuario_id": usuario_id,
                "match_score": post["match_score"],
                "clasificacion": post["clasificacion"],
                "scores_detalle": post.get("scores_detalle") or {},
                "fortalezas": post.get("fortalezas") or [],
                "debilidades": post.get("debilidades") or [],
                "match_details": post.get("match_details"),
                "estado_postulacion": post.get("estado", "pendiente"),
                "postulado_en": post.get("created_at"),
                "perfil": {
                    "nombre_completo": perfil.get("nombre_completo") or usuario.get("nombre_completo") or "Sin nombre",
                    "email": perfil.get("email_contacto") or usuario.get("email"),
                    "telefono": perfil.get("telefono"),
                    "direccion": perfil.get("direccion"),
                    "rol": usuario.get("rol"),
                    "hard_skills": perfil.get("hard_skills") or [],
                    "soft_skills": perfil.get("soft_skills") or [],
                    "education_level": perfil.get("education_level"),
                    "experience_years": perfil.get("experience_years") or 0,
                    "languages": perfil.get("languages") or [],
                    "completeness_score": perfil.get("completeness_score") or 0,
                    "cv_filename": perfil.get("cv_filename"),
                },
            })

        return {
            "oferta": oferta,
            "total_postulantes": total_postulantes,
            "top_n": top_n,
            "candidatos": candidatos,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo ranking para oferta {oferta_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/convocatorias/{oferta_id}/generar-informe")
async def generar_informe_candidatos(
    oferta_id: str,
    top_n: int = Query(default=3, ge=1, le=20, description="Candidatos a incluir en el informe"),
    current_user: dict = Depends(verify_admin_role)
):
    """
    Genera un informe PDF formal con el ranking de candidatos para una oferta.

    El documento incluye:
    - Portada institucional con número de referencia
    - Resumen ejecutivo con estadísticas
    - Detalle de la convocatoria
    - Parámetros de evaluación
    - Resultados y estadísticas
    - Ranking detallado con desglose por dimensión
    - Anexos: CVs en formato Harvard por cada candidato
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

    try:
        # Obtener oferta
        oferta_service = get_oferta_service()
        oferta = oferta_service.get_oferta(oferta_id)
        if not oferta:
            raise HTTPException(status_code=404, detail="Oferta no encontrada")

        # Complementar con datos institucionales si faltan
        inst_id = oferta.get('institutional_profile_id')
        if inst_id and not oferta.get('institution_name'):
            inst_resp = supabase.table("institutional_profiles") \
                .select("institution_name, sector") \
                .eq("id", inst_id) \
                .execute()
            if inst_resp.data:
                oferta['institution_name'] = inst_resp.data[0].get('institution_name')
                oferta['sector'] = inst_resp.data[0].get('sector')

        # Top N postulaciones ordenadas por puntaje
        posts_resp = supabase.table("postulaciones") \
            .select("*") \
            .eq("oferta_id", oferta_id) \
            .order("match_score", desc=True) \
            .limit(top_n) \
            .execute()
        posts = posts_resp.data or []

        # Total de postulantes
        total_resp = supabase.table("postulaciones") \
            .select("id", count="exact") \
            .eq("oferta_id", oferta_id) \
            .execute()
        total_postulantes = total_resp.count or len(posts)

        candidatos = []
        for rank, post in enumerate(posts, start=1):
            usuario_id = post["usuario_id"]

            # Perfil profesional con gemini_extraction para el CV Harvard
            perfil_resp = supabase.table("perfiles_profesionales") \
                .select(
                    "nombre_completo, email_contacto, telefono, direccion,"
                    " hard_skills, soft_skills, education_level, experience_years,"
                    " languages, cv_filename, completeness_score, gemini_extraction"
                ) \
                .eq("usuario_id", usuario_id) \
                .execute()
            perfil = perfil_resp.data[0] if perfil_resp.data else {}
            gemini_data = perfil.pop("gemini_extraction", None) or {}

            usuario_resp = supabase.table("usuarios") \
                .select("email, nombre_completo, rol") \
                .eq("id", usuario_id) \
                .execute()
            usuario = usuario_resp.data[0] if usuario_resp.data else {}

            candidatos.append({
                "rank": rank,
                "usuario_id": usuario_id,
                "match_score": post["match_score"],
                "clasificacion": post["clasificacion"],
                "scores_detalle": post.get("scores_detalle") or {},
                "fortalezas": post.get("fortalezas") or [],
                "debilidades": post.get("debilidades") or [],
                "match_details": post.get("match_details"),
                "estado_postulacion": post.get("estado", "pendiente"),
                "postulado_en": post.get("created_at"),
                "gemini_extraction": gemini_data,
                "perfil": {
                    "nombre_completo": (
                        perfil.get("nombre_completo")
                        or usuario.get("nombre_completo")
                        or "Sin nombre"
                    ),
                    "email": perfil.get("email_contacto") or usuario.get("email"),
                    "telefono": perfil.get("telefono"),
                    "direccion": perfil.get("direccion"),
                    "rol": usuario.get("rol"),
                    "hard_skills": perfil.get("hard_skills") or [],
                    "soft_skills": perfil.get("soft_skills") or [],
                    "education_level": perfil.get("education_level"),
                    "experience_years": perfil.get("experience_years") or 0,
                    "languages": perfil.get("languages") or [],
                    "completeness_score": perfil.get("completeness_score") or 0,
                    "cv_filename": perfil.get("cv_filename"),
                },
            })

        # Generar PDF
        from app.services.pdf_report_service import get_pdf_report_service
        pdf_service = get_pdf_report_service()
        pdf_bytes = pdf_service.generate_report(oferta, candidatos, total_postulantes, top_n)

        titulo_safe = (oferta.get('titulo', 'informe')[:30]
                       .replace(' ', '-')
                       .lower())
        filename = f"informe-evaluacion-{titulo_safe}.pdf"

        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Length": str(len(pdf_bytes)),
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generando informe para oferta {oferta_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
