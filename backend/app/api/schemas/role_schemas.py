from pydantic import BaseModel, field_validator
from typing import Dict, List, Optional

VALID_SUBMODULES: Dict[str, List[str]] = {
    "gestion_usuarios":         ["lista_usuarios", "nuevo_usuario"],
    "digitalizacion_perfiles":  ["subir_cv", "mi_perfil", "editar_perfil", "buscar_perfiles"],
    "oferta_laboral":           ["ver_ofertas", "nueva_oferta"],
    "perfiles_institucionales": ["ver_perfiles", "nuevo_perfil"],
    "evaluacion_perfiles":      ["correspondencia", "historial", "ranking_candidatos"],
    "informes_reportes":        ["resumen_general", "reporte_usuarios", "reporte_ofertas", "reporte_perfiles", "reporte_cumplimiento", "reporte_cargos"],
}

VALID_MODULES = list(VALID_SUBMODULES.keys())


def _validate_permisos(v: Dict[str, List[str]]) -> Dict[str, List[str]]:
    for mod_id, sub_ids in v.items():
        if mod_id not in VALID_MODULES:
            raise ValueError(f"Módulo inválido: '{mod_id}'")
        valid_subs = VALID_SUBMODULES[mod_id]
        invalid = [s for s in sub_ids if s not in valid_subs]
        if invalid:
            raise ValueError(f"Submódulos inválidos para '{mod_id}': {', '.join(invalid)}")
    return v


class RoleCreateRequest(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    # { moduleId: [submoduleId, ...] }  — claves = módulos habilitados
    modulos_permitidos: Dict[str, List[str]]

    @field_validator("modulos_permitidos")
    @classmethod
    def validate_modules(cls, v):
        return _validate_permisos(v)

    @field_validator("nombre")
    @classmethod
    def validate_nombre(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El nombre no puede estar vacío")
        if v in ("estudiante", "titulado", "operador", "administrador"):
            raise ValueError("No puedes usar el nombre de un rol del sistema")
        return v


class RoleUpdateRequest(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    modulos_permitidos: Optional[Dict[str, List[str]]] = None

    @field_validator("modulos_permitidos")
    @classmethod
    def validate_modules(cls, v):
        if v is None:
            return v
        return _validate_permisos(v)

    @field_validator("nombre")
    @classmethod
    def validate_nombre(cls, v):
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("El nombre no puede estar vacío")
        if v in ("estudiante", "titulado", "operador", "administrador"):
            raise ValueError("No puedes usar el nombre de un rol del sistema")
        return v


class RoleResponse(BaseModel):
    id: str
    nombre: str
    descripcion: Optional[str]
    modulos_permitidos: Dict[str, List[str]]
    created_at: str
