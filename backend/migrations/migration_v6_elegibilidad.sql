-- Migration v6: Campos de elegibilidad en perfiles y ofertas
-- Agrega carrera y semestre_actual al perfil del candidato

ALTER TABLE perfiles_profesionales
    ADD COLUMN IF NOT EXISTS carrera TEXT,
    ADD COLUMN IF NOT EXISTS semestre_actual INTEGER CHECK (semestre_actual BETWEEN 1 AND 10);

COMMENT ON COLUMN perfiles_profesionales.carrera         IS 'Carrera EMI que estudia o estudió el candidato';
COMMENT ON COLUMN perfiles_profesionales.semestre_actual IS 'Semestre actual del estudiante (1-10); NULL para titulados';

-- Los campos de elegibilidad de la oferta (carreras_aceptadas, semestre_minimo,
-- semestre_maximo) se almacenan en el JSONB requirements de ofertas_laborales,
-- por lo que no requieren columnas nuevas.

-- Comentario sobre el uso esperado:
-- perfiles_profesionales.carrera      → carrera de la EMI que estudia/estudió el candidato
-- perfiles_profesionales.semestre_actual → semestre actual (1-10), solo para rol 'estudiante'
--
-- ofertas_laborales.requirements.carreras_aceptadas  → lista de carreras válidas ([] = todas)
-- ofertas_laborales.requirements.semestre_minimo     → semestre mínimo requerido (opcional)
-- ofertas_laborales.requirements.semestre_maximo     → semestre máximo requerido (opcional)

-- ─────────────────────────────────────────────────────────────────────────────
-- Fix 1: columna match_details faltante en recomendaciones
-- El servicio guarda eligibility_reason dentro de match_details, pero la
-- columna no existía en el schema original.
-- ─────────────────────────────────────────────────────────────────────────────
ALTER TABLE recomendaciones
    ADD COLUMN IF NOT EXISTS match_details JSONB;

COMMENT ON COLUMN recomendaciones.match_details IS 'Detalle del match ML: scores por dimensión, eligibility_reason si aplica';

-- ─────────────────────────────────────────────────────────────────────────────
-- Fix 2: institutional_profiles - eliminar columnas de evaluación
-- La nueva arquitectura asigna pesos/requisitos/umbrales a nivel de cada oferta.
-- institutional_profiles solo guarda datos de identidad de la institución.
-- ─────────────────────────────────────────────────────────────────────────────
ALTER TABLE institutional_profiles
    DROP COLUMN IF EXISTS weights,
    DROP COLUMN IF EXISTS requirements,
    DROP COLUMN IF EXISTS thresholds;
