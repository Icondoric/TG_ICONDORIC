-- ============================================================================
-- SETUP COMPLETO DE BASE DE DATOS - SISTEMA DE INTERMEDIACIÓN LABORAL
-- ============================================================================
-- Archivo:  setup_completo.sql
-- Versión:  Consolidada (schema base + migraciones v2 a v8)
-- Fecha:    2026-06-17
--
-- INSTRUCCIONES:
--   1. Abrir el SQL Editor de Supabase
--   2. Pegar TODO este archivo
--   3. Ejecutar (F5 o botón Run)
--   4. ¡Listo! La base de datos queda 100% operativa
--
-- NOTA: Este script es IDEMPOTENTE — puede ejecutarse varias veces sin
--       romper nada (usa IF NOT EXISTS, IF EXISTS, CREATE OR REPLACE, etc.)
-- ============================================================================
-- ============================================================================
-- 1. TABLA: usuarios
--    Autenticación personalizada (no usa Supabase Auth nativo)
-- ============================================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           TEXT UNIQUE NOT NULL,
    password_hash   TEXT NOT NULL,
    rol             TEXT NOT NULL CHECK (rol IN ('estudiante', 'titulado', 'administrador', 'admin', 'operador')),
    nombre_completo TEXT,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);
-- ============================================================================
-- 2. TABLA: perfiles_profesionales
--    Perfil completo del candidato (estudiante/titulado)
-- ============================================================================
CREATE TABLE IF NOT EXISTS perfiles_profesionales (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id          UUID REFERENCES usuarios(id) ON DELETE CASCADE,
    -- Datos JSONB legado (mantenido por compatibilidad)
    data                JSONB DEFAULT '{}'::jsonb,
    -- Campos estructurados de perfil profesional (migración v2)
    gemini_extraction   JSONB DEFAULT '{}'::jsonb,
    hard_skills         TEXT[] DEFAULT '{}',
    soft_skills         TEXT[] DEFAULT '{}',
    education_level     TEXT,
    experience_years    NUMERIC(4,2) DEFAULT 0,
    languages           TEXT[] DEFAULT '{}',
    cv_filename         TEXT,
    cv_uploaded_at      TIMESTAMP WITH TIME ZONE,
    is_complete         BOOLEAN DEFAULT FALSE,
    completeness_score  NUMERIC(3,2) DEFAULT 0,
    -- Información personal (migración v5)
    nombre_completo     TEXT,
    direccion           TEXT,
    telefono            TEXT,
    email_contacto      TEXT,
    nacionalidad        TEXT,
    -- Elegibilidad académica (migración v6)
    carrera             TEXT,
    semestre_actual     INTEGER CHECK (semestre_actual BETWEEN 1 AND 10),
    -- Timestamps
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),
    updated_at          TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);
-- Constraint de unicidad: un usuario solo tiene un perfil
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'perfiles_profesionales_usuario_id_unique'
    ) THEN
        ALTER TABLE perfiles_profesionales
        ADD CONSTRAINT perfiles_profesionales_usuario_id_unique UNIQUE (usuario_id);
    END IF;
END $$;
-- Comentarios descriptivos
COMMENT ON COLUMN perfiles_profesionales.nombre_completo IS 'Nombre completo extraído del CV (puede diferir del nombre de registro)';
COMMENT ON COLUMN perfiles_profesionales.direccion       IS 'Dirección/ubicación extraída del CV';
COMMENT ON COLUMN perfiles_profesionales.telefono        IS 'Teléfono de contacto extraído del CV';
COMMENT ON COLUMN perfiles_profesionales.email_contacto  IS 'Email de contacto del CV (puede diferir del email de login)';
COMMENT ON COLUMN perfiles_profesionales.nacionalidad    IS 'Nacionalidad extraída del CV';
COMMENT ON COLUMN perfiles_profesionales.carrera         IS 'Carrera EMI que estudia o estudió el candidato';
COMMENT ON COLUMN perfiles_profesionales.semestre_actual IS 'Semestre actual del estudiante (1-10); NULL para titulados';
-- ============================================================================
-- 3. TABLA: institutional_profiles
--    Perfiles de instituciones/empresas que publican convocatorias
-- ============================================================================
CREATE TABLE IF NOT EXISTS institutional_profiles (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    institution_name    TEXT UNIQUE NOT NULL,
    sector              TEXT NOT NULL,
    tipo_institucion    TEXT CHECK (tipo_institucion IN ('Pública', 'Privada', 'Mixta', 'ONG') OR tipo_institucion IS NULL),
    description         TEXT,
    ubicacion           TEXT,
    contact_phone       TEXT,
    contact_email       TEXT,
    is_active           BOOLEAN DEFAULT TRUE,
    created_by          UUID REFERENCES usuarios(id),
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),
    updated_at          TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);
-- ============================================================================
-- 4. TABLA: convocatorias_laborales
--    Ofertas/convocatorias de pasantía o empleo publicadas por instituciones
--    (Anteriormente llamada "ofertas_laborales", renombrada en migración v8)
-- ============================================================================
CREATE TABLE IF NOT EXISTS convocatorias_laborales (
    id                        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- Relación con perfil institucional
    institutional_profile_id  UUID REFERENCES institutional_profiles(id) ON DELETE SET NULL,
    -- Información de la convocatoria
    titulo                    TEXT NOT NULL,
    descripcion               TEXT,
    tipo                      TEXT NOT NULL CHECK (tipo IN ('pasantia', 'empleo')),
    modalidad                 TEXT CHECK (modalidad IN ('presencial', 'remoto', 'hibrido')),
    ubicacion                 TEXT,
    area                      TEXT,
    -- Requisitos específicos (JSONB flexible)
    requisitos_especificos    JSONB DEFAULT '{}'::jsonb,
    -- Configuración de evaluación ML por convocatoria (migración v3)
    weights                   JSONB,
    thresholds                JSONB,
    requirements              JSONB,
    -- Contacto directo de la convocatoria (migración v3)
    contact_phone             TEXT,
    contact_email             TEXT,
    -- Estado y vigencia
    is_active                 BOOLEAN DEFAULT TRUE,
    fecha_inicio              DATE,
    fecha_cierre              DATE,
    cupos_disponibles         INTEGER DEFAULT 1,
    -- Auditoría
    created_by                UUID REFERENCES usuarios(id),
    created_at                TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),
    updated_at                TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);
-- ============================================================================
-- 5. TABLA: recomendaciones
--    Evaluaciones automáticas del sistema ML (match candidato ↔ convocatoria)
-- ============================================================================
CREATE TABLE IF NOT EXISTS recomendaciones (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id      UUID REFERENCES usuarios(id) ON DELETE CASCADE,
    oferta_id       UUID REFERENCES convocatorias_laborales(id) ON DELETE CASCADE,
    -- Resultado de la evaluación
    match_score     NUMERIC(4,3) CHECK (match_score >= 0 AND match_score <= 1),
    clasificacion   TEXT CHECK (clasificacion IN ('APTO', 'CONSIDERADO', 'NO_APTO')),
    -- Detalle de scores
    scores_detalle  JSONB,
    match_details   JSONB,
    fortalezas      TEXT[],
    debilidades     TEXT[],
    -- Estado de lectura
    fue_vista       BOOLEAN DEFAULT FALSE,
    vista_at        TIMESTAMP WITH TIME ZONE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),
    -- Un usuario no puede tener múltiples recomendaciones para la misma convocatoria
    CONSTRAINT unique_usuario_oferta UNIQUE (usuario_id, oferta_id)
);
COMMENT ON COLUMN recomendaciones.match_details IS 'Detalle del match ML: scores por dimensión, eligibility_reason si aplica';
-- ============================================================================
-- 6. TABLA: postulaciones
--    Aplicaciones explícitas de candidatos a convocatorias
-- ============================================================================
CREATE TABLE IF NOT EXISTS postulaciones (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id      UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    oferta_id       UUID NOT NULL REFERENCES convocatorias_laborales(id) ON DELETE CASCADE,
    -- Resultado de evaluación ML
    match_score     NUMERIC(4,3) CHECK (match_score >= 0 AND match_score <= 1),
    clasificacion   TEXT CHECK (clasificacion IN ('APTO', 'CONSIDERADO', 'NO_APTO')),
    scores_detalle  JSONB,
    fortalezas      TEXT[],
    debilidades     TEXT[],
    match_details   JSONB,
    -- Estado de la postulación (gestión administrativa)
    estado          TEXT DEFAULT 'pendiente'
                    CHECK (estado IN ('pendiente', 'en_revision', 'aceptado', 'rechazado')),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    -- Un usuario solo puede postular una vez por convocatoria
    UNIQUE (usuario_id, oferta_id)
);
-- ============================================================================
-- 7. ÍNDICES
-- ============================================================================
-- Perfiles profesionales
CREATE INDEX IF NOT EXISTS idx_perfiles_data          ON perfiles_profesionales USING GIN (data);
CREATE INDEX IF NOT EXISTS idx_perfiles_hard_skills   ON perfiles_profesionales USING GIN (hard_skills);
CREATE INDEX IF NOT EXISTS idx_perfiles_soft_skills   ON perfiles_profesionales USING GIN (soft_skills);
CREATE INDEX IF NOT EXISTS idx_perfiles_education     ON perfiles_profesionales (education_level);
CREATE INDEX IF NOT EXISTS idx_perfiles_experience    ON perfiles_profesionales (experience_years);
CREATE INDEX IF NOT EXISTS idx_perfiles_complete      ON perfiles_profesionales (is_complete);
-- Convocatorias laborales
CREATE INDEX IF NOT EXISTS idx_convocatorias_tipo            ON convocatorias_laborales (tipo);
CREATE INDEX IF NOT EXISTS idx_convocatorias_active          ON convocatorias_laborales (is_active);
CREATE INDEX IF NOT EXISTS idx_convocatorias_fecha_cierre    ON convocatorias_laborales (fecha_cierre);
CREATE INDEX IF NOT EXISTS idx_convocatorias_institutional   ON convocatorias_laborales (institutional_profile_id);
-- Recomendaciones
CREATE INDEX IF NOT EXISTS idx_recomendaciones_usuario       ON recomendaciones (usuario_id);
CREATE INDEX IF NOT EXISTS idx_recomendaciones_oferta        ON recomendaciones (oferta_id);
CREATE INDEX IF NOT EXISTS idx_recomendaciones_score         ON recomendaciones (match_score DESC);
CREATE INDEX IF NOT EXISTS idx_recomendaciones_clasificacion ON recomendaciones (clasificacion);
CREATE INDEX IF NOT EXISTS idx_recomendaciones_vista         ON recomendaciones (fue_vista);
-- Postulaciones
CREATE INDEX IF NOT EXISTS idx_postulaciones_usuario         ON postulaciones (usuario_id);
CREATE INDEX IF NOT EXISTS idx_postulaciones_oferta          ON postulaciones (oferta_id);
CREATE INDEX IF NOT EXISTS idx_postulaciones_score           ON postulaciones (match_score DESC);
CREATE INDEX IF NOT EXISTS idx_postulaciones_clasificacion   ON postulaciones (clasificacion);
CREATE INDEX IF NOT EXISTS idx_postulaciones_estado          ON postulaciones (estado);
CREATE INDEX IF NOT EXISTS idx_postulaciones_created         ON postulaciones (created_at DESC);
-- ============================================================================
-- 8. ROW LEVEL SECURITY (RLS)
--    Políticas permisivas para uso con API key anon.
--    La seguridad se gestiona a nivel de backend (JWT custom).
-- ============================================================================
ALTER TABLE usuarios                ENABLE ROW LEVEL SECURITY;
ALTER TABLE perfiles_profesionales  ENABLE ROW LEVEL SECURITY;
ALTER TABLE institutional_profiles  ENABLE ROW LEVEL SECURITY;
ALTER TABLE convocatorias_laborales ENABLE ROW LEVEL SECURITY;
ALTER TABLE recomendaciones         ENABLE ROW LEVEL SECURITY;
ALTER TABLE postulaciones           ENABLE ROW LEVEL SECURITY;
-- Políticas: acceso total vía API (la autenticación/autorización se hace en el backend)
DROP POLICY IF EXISTS "Permitir acceso total api anon"            ON usuarios;
DROP POLICY IF EXISTS "Permitir acceso total api anon perfiles"   ON perfiles_profesionales;
DROP POLICY IF EXISTS "Permitir acceso total instituciones"       ON institutional_profiles;
DROP POLICY IF EXISTS "Permitir acceso total convocatorias"       ON convocatorias_laborales;
DROP POLICY IF EXISTS "Permitir acceso total recomendaciones"     ON recomendaciones;
DROP POLICY IF EXISTS "Permitir acceso total postulaciones"       ON postulaciones;
CREATE POLICY "Permitir acceso total api anon"          ON usuarios                FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Permitir acceso total api anon perfiles" ON perfiles_profesionales  FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Permitir acceso total instituciones"     ON institutional_profiles  FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Permitir acceso total convocatorias"     ON convocatorias_laborales FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Permitir acceso total recomendaciones"   ON recomendaciones         FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Permitir acceso total postulaciones"     ON postulaciones           FOR ALL USING (true) WITH CHECK (true);
-- ============================================================================
-- 9. FUNCIONES Y TRIGGERS
-- ============================================================================
-- Función genérica para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = timezone('utc', now());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
-- Triggers de updated_at
DROP TRIGGER IF EXISTS update_perfiles_profesionales_updated_at ON perfiles_profesionales;
CREATE TRIGGER update_perfiles_profesionales_updated_at
    BEFORE UPDATE ON perfiles_profesionales
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
DROP TRIGGER IF EXISTS update_convocatorias_laborales_updated_at ON convocatorias_laborales;
CREATE TRIGGER update_convocatorias_laborales_updated_at
    BEFORE UPDATE ON convocatorias_laborales
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
DROP TRIGGER IF EXISTS update_institutional_profiles_updated_at ON institutional_profiles;
CREATE TRIGGER update_institutional_profiles_updated_at
    BEFORE UPDATE ON institutional_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
DROP TRIGGER IF EXISTS update_postulaciones_updated_at ON postulaciones;
CREATE TRIGGER update_postulaciones_updated_at
    BEFORE UPDATE ON postulaciones
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
-- ============================================================================
-- 10. VISTA: admin_estadisticas
--     Resumen rápido para el dashboard administrativo
-- ============================================================================
CREATE OR REPLACE VIEW admin_estadisticas AS
SELECT
    (SELECT COUNT(*) FROM usuarios WHERE rol = 'estudiante')                              AS total_estudiantes,
    (SELECT COUNT(*) FROM usuarios WHERE rol = 'titulado')                                AS total_titulados,
    (SELECT COUNT(*) FROM usuarios WHERE rol IN ('administrador', 'admin'))                AS total_admins,
    (SELECT COUNT(*) FROM perfiles_profesionales WHERE is_complete = true)                 AS perfiles_completos,
    (SELECT COUNT(*) FROM convocatorias_laborales WHERE is_active = true AND tipo = 'pasantia') AS pasantias_activas,
    (SELECT COUNT(*) FROM convocatorias_laborales WHERE is_active = true AND tipo = 'empleo')   AS empleos_activos,
    (SELECT COUNT(*) FROM recomendaciones)                                                 AS total_recomendaciones,
    (SELECT AVG(match_score) FROM recomendaciones)                                         AS promedio_match_score,
    (SELECT COUNT(*) FROM institutional_profiles WHERE is_active = true)                   AS perfiles_institucionales_activos;
-- ============================================================================
-- ¡SETUP COMPLETO! La base de datos está lista para usar.
-- ============================================================================
