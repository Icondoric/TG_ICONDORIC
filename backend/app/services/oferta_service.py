"""
Oferta Service - Sistema de Recomendaciones v2
Servicio para gestionar ofertas laborales (pasantias y empleos)
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, date

from app.db.client import supabase

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OfertaService:
    """
    Servicio para gestionar ofertas laborales.

    Funcionalidades:
    - CRUD de ofertas (pasantias y empleos)
    - Filtrado por tipo, sector, estado
    - Vinculacion con perfiles institucionales
    - Gestion de vigencia
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def create_oferta(self, data: Dict, created_by: str) -> Dict:
        """
        Crea una nueva oferta laboral.

        Args:
            data: Datos de la oferta
            created_by: ID del usuario admin que crea

        Returns:
            Dict con la oferta creada
        """
        if not supabase:
            raise ValueError("Base de datos no configurada")

        try:
            oferta_data = {
                'institutional_profile_id': data.get('institutional_profile_id'),
                'titulo': data['titulo'],
                'descripcion': data.get('descripcion'),
                'tipo': data['tipo'],
                'modalidad': data.get('modalidad'),
                'ubicacion': data.get('ubicacion'),
                'requisitos_especificos': data.get('requisitos_especificos', {}),
                'is_active': True,
                'fecha_inicio': data.get('fecha_inicio'),
                'fecha_cierre': data.get('fecha_cierre'),
                'cupos_disponibles': data.get('cupos_disponibles', 1),
                'created_by': created_by
            }

            response = supabase.table("ofertas_laborales") \
                .insert(oferta_data) \
                .execute()

            if response.data:
                logger.info(f"Oferta creada: {response.data[0]['id']}")
                return self._enrich_oferta(response.data[0])

            raise ValueError("No se pudo crear la oferta")

        except Exception as e:
            logger.error(f"Error creando oferta: {e}")
            raise

    def update_oferta(self, oferta_id: str, data: Dict) -> Dict:
        """
        Actualiza una oferta existente.

        Args:
            oferta_id: ID de la oferta
            data: Campos a actualizar

        Returns:
            Dict con la oferta actualizada
        """
        if not supabase:
            raise ValueError("Base de datos no configurada")

        # Verificar que existe
        existing = self.get_oferta(oferta_id)
        if not existing:
            raise ValueError("Oferta no encontrada")

        try:
            update_data = {'updated_at': datetime.utcnow().isoformat()}

            # Campos permitidos para actualizar
            allowed_fields = [
                'institutional_profile_id', 'titulo', 'descripcion',
                'tipo', 'modalidad', 'ubicacion', 'requisitos_especificos',
                'is_active', 'fecha_inicio', 'fecha_cierre', 'cupos_disponibles'
            ]

            for field in allowed_fields:
                if field in data and data[field] is not None:
                    update_data[field] = data[field]

            response = supabase.table("ofertas_laborales") \
                .update(update_data) \
                .eq("id", oferta_id) \
                .execute()

            if response.data:
                logger.info(f"Oferta actualizada: {oferta_id}")
                return self._enrich_oferta(response.data[0])

            raise ValueError("No se pudo actualizar la oferta")

        except Exception as e:
            logger.error(f"Error actualizando oferta: {e}")
            raise

    def get_oferta(self, oferta_id: str) -> Optional[Dict]:
        """
        Obtiene una oferta por ID.

        Args:
            oferta_id: ID de la oferta

        Returns:
            Dict con la oferta o None
        """
        if not supabase:
            raise ValueError("Base de datos no configurada")

        try:
            response = supabase.table("ofertas_laborales") \
                .select("*, institutional_profiles(institution_name, sector)") \
                .eq("id", oferta_id) \
                .execute()

            if not response.data:
                return None

            return self._enrich_oferta(response.data[0])

        except Exception as e:
            logger.error(f"Error obteniendo oferta {oferta_id}: {e}")
            raise

    def list_ofertas(
        self,
        tipo: str = None,
        is_active: bool = None,
        sector: str = None,
        include_expired: bool = False,
        page: int = 1,
        page_size: int = 20
    ) -> Dict:
        """
        Lista ofertas con filtros.

        Args:
            tipo: Filtrar por tipo ('pasantia' o 'empleo')
            is_active: Filtrar por estado activo
            sector: Filtrar por sector
            include_expired: Incluir ofertas expiradas
            page: Numero de pagina
            page_size: Tamano de pagina

        Returns:
            Dict con ofertas y metadata de paginacion
        """
        if not supabase:
            raise ValueError("Base de datos no configurada")

        try:
            query = supabase.table("ofertas_laborales") \
                .select("*, institutional_profiles(institution_name, sector)", count="exact")

            # Aplicar filtros
            if tipo:
                query = query.eq("tipo", tipo)

            if is_active is not None:
                query = query.eq("is_active", is_active)

            if not include_expired:
                today = date.today().isoformat()
                query = query.or_(f"fecha_cierre.is.null,fecha_cierre.gte.{today}")

            # Ordenar por fecha de creacion
            query = query.order("created_at", desc=True)

            # Paginacion
            offset = (page - 1) * page_size
            query = query.range(offset, offset + page_size - 1)

            response = query.execute()

            # Filtrar por sector si se especifica (ya que es un campo del perfil institucional)
            ofertas = response.data or []
            if sector:
                ofertas = [
                    o for o in ofertas
                    if o.get('institutional_profiles', {}).get('sector') == sector
                ]

            # Enriquecer ofertas
            ofertas_enriched = [self._enrich_oferta(o) for o in ofertas]

            return {
                'ofertas': ofertas_enriched,
                'total': response.count or len(ofertas_enriched),
                'page': page,
                'page_size': page_size
            }

        except Exception as e:
            logger.error(f"Error listando ofertas: {e}")
            raise

    def delete_oferta(self, oferta_id: str) -> bool:
        """
        Desactiva una oferta (soft delete).

        Args:
            oferta_id: ID de la oferta

        Returns:
            True si se desactivo correctamente
        """
        if not supabase:
            raise ValueError("Base de datos no configurada")

        try:
            response = supabase.table("ofertas_laborales") \
                .update({
                    'is_active': False,
                    'updated_at': datetime.utcnow().isoformat()
                }) \
                .eq("id", oferta_id) \
                .execute()

            if response.data:
                logger.info(f"Oferta desactivada: {oferta_id}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error desactivando oferta: {e}")
            raise

    def activate_oferta(self, oferta_id: str) -> Dict:
        """
        Reactiva una oferta desactivada.

        Args:
            oferta_id: ID de la oferta

        Returns:
            Dict con la oferta reactivada
        """
        if not supabase:
            raise ValueError("Base de datos no configurada")

        try:
            response = supabase.table("ofertas_laborales") \
                .update({
                    'is_active': True,
                    'updated_at': datetime.utcnow().isoformat()
                }) \
                .eq("id", oferta_id) \
                .execute()

            if response.data:
                logger.info(f"Oferta reactivada: {oferta_id}")
                return self._enrich_oferta(response.data[0])

            raise ValueError("Oferta no encontrada")

        except Exception as e:
            logger.error(f"Error reactivando oferta: {e}")
            raise

    def get_ofertas_for_user_role(
        self,
        user_role: str,
        top_n: int = 50
    ) -> List[Dict]:
        """
        Obtiene ofertas filtradas segun el rol del usuario.

        Args:
            user_role: 'estudiante' o 'titulado'
            top_n: Numero maximo de ofertas

        Returns:
            Lista de ofertas activas del tipo correspondiente
        """
        # Determinar tipo segun rol
        if user_role == 'estudiante':
            tipo = 'pasantia'
        elif user_role == 'titulado':
            tipo = 'empleo'
        else:
            # Admin u otro rol no recibe ofertas
            return []

        result = self.list_ofertas(
            tipo=tipo,
            is_active=True,
            include_expired=False,
            page_size=top_n
        )

        return result['ofertas']

    def get_statistics(self) -> Dict:
        """
        Obtiene estadisticas de ofertas para el dashboard admin.

        Returns:
            Dict con estadisticas
        """
        if not supabase:
            raise ValueError("Base de datos no configurada")

        try:
            # Total por tipo
            pasantias = supabase.table("ofertas_laborales") \
                .select("id", count="exact") \
                .eq("tipo", "pasantia") \
                .eq("is_active", True) \
                .execute()

            empleos = supabase.table("ofertas_laborales") \
                .select("id", count="exact") \
                .eq("tipo", "empleo") \
                .eq("is_active", True) \
                .execute()

            # Expiradas
            today = date.today().isoformat()
            expiradas = supabase.table("ofertas_laborales") \
                .select("id", count="exact") \
                .lt("fecha_cierre", today) \
                .execute()

            # Total inactivas
            inactivas = supabase.table("ofertas_laborales") \
                .select("id", count="exact") \
                .eq("is_active", False) \
                .execute()

            return {
                'pasantias_activas': pasantias.count or 0,
                'empleos_activos': empleos.count or 0,
                'ofertas_expiradas': expiradas.count or 0,
                'ofertas_inactivas': inactivas.count or 0,
                'total_activas': (pasantias.count or 0) + (empleos.count or 0)
            }

        except Exception as e:
            logger.error(f"Error obteniendo estadisticas: {e}")
            return {}

    def _enrich_oferta(self, oferta: Dict) -> Dict:
        """
        Enriquece una oferta con datos del perfil institucional.

        Args:
            oferta: Dict de la oferta

        Returns:
            Dict enriquecido
        """
        inst_profile = oferta.pop('institutional_profiles', None) or {}

        return {
            **oferta,
            'institution_name': inst_profile.get('institution_name'),
            'sector': inst_profile.get('sector')
        }


# Singleton instance
_oferta_service_instance = None


def get_oferta_service() -> OfertaService:
    """
    Obtiene la instancia singleton del servicio de ofertas.

    Returns:
        Instancia de OfertaService
    """
    global _oferta_service_instance
    if _oferta_service_instance is None:
        _oferta_service_instance = OfertaService()
    return _oferta_service_instance
