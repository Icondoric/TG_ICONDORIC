-- =====================================================
-- MIGRACION V2: SISTEMA DE RECOMENDACIONES MEJORADO
-- =====================================================
-- Ejecutar en Supabase SQL Editor
-- Fecha: 2026-01-31
-- =====================================================

-- =====================================================
-- 1. MODIFICAR TABLA perfiles_profesionales
-- =====================================================

-- Agregar nuevas columnas a la tabla existente
ALTER TABLE perfiles_profesionales
ADD COLUMN IF NOT EXISTS gemini_extraction JSONB DEFAULT '{}'::jsonb,
ADD COLUMN IF NOT EXISTS hard_skills TEXT[] DEFAULT '{}',
ADD COLUMN IF NOT EXISTS soft_skills TEXT[] DEFAULT '{}',
ADD COLUMN IF NOT EXISTS education_level TEXT,
ADD COLUMN IF NOT EXISTS experience_years NUMERIC(4,2) DEFAULT 0,
ADD COLUMN IF NOT EXISTS languages TEXT[] DEFAULT '{}',
ADD COLUMN IF NOT EXISTS cv_filename TEXT,
ADD COLUMN IF NOT EXISTS cv_uploaded_at TIMESTAMP WITH TIME ZONE,
ADD COLUMN IF NOT EXISTS is_complete BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS completeness_score NUMERIC(3,2) DEFAULT 0;

-- Crear indices para busqueda eficiente en arrays
CREATE INDEX IF NOT EXISTS idx_perfiles_hard_skills ON perfiles_profesionales USING GIN(hard_skills);
CREATE INDEX IF NOT EXISTS idx_perfiles_soft_skills ON perfiles_profesionales USING GIN(soft_skills);
CREATE INDEX IF NOT EXISTS idx_perfiles_education ON perfiles_profesionales(education_level);
CREATE INDEX IF NOT EXISTS idx_perfiles_experience ON perfiles_profesionales(experience_years);
CREATE INDEX IF NOT EXISTS idx_perfiles_complete ON perfiles_profesionales(is_complete);

-- Constraint de unicidad usuario_id
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

-- =====================================================
-- 2. CREAR TABLA ofertas_laborales
-- =====================================================

CREATE TABLE IF NOT EXISTS ofertas_laborales (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Relacion con perfil institucional
    institutional_profile_id UUID REFERENCES institutional_profiles(id) ON DELETE SET NULL,

    -- Informacion de la oferta
    titulo TEXT NOT NULL,
    descripcion TEXT,
    tipo TEXT NOT NULL CHECK (tipo IN ('pasantia', 'empleo')),
    modalidad TEXT CHECK (modalidad IN ('presencial', 'remoto', 'hibrido')),
    ubicacion TEXT,

    -- Requisitos especificos (pueden diferir del perfil institucional base)
    requisitos_especificos JSONB DEFAULT '{}'::jsonb,

    -- Estado y vigencia
    is_active BOOLEAN DEFAULT TRUE,
    fecha_inicio DATE,
    fecha_cierre DATE,
    cupos_disponibles INTEGER DEFAULT 1,

    -- Auditoria
    created_by UUID REFERENCES usuarios(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);

-- Indices para ofertas
CREATE INDEX IF NOT EXISTS idx_ofertas_tipo ON ofertas_laborales(tipo);
CREATE INDEX IF NOT EXISTS idx_ofertas_active ON ofertas_laborales(is_active);
CREATE INDEX IF NOT EXISTS idx_ofertas_fecha_cierre ON ofertas_laborales(fecha_cierre);
CREATE INDEX IF NOT EXISTS idx_ofertas_institutional ON ofertas_laborales(institutional_profile_id);

-- Politica RLS para ofertas
ALTER TABLE ofertas_laborales ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Permitir acceso total ofertas" ON ofertas_laborales;
CREATE POLICY "Permitir acceso total ofertas" ON ofertas_laborales
FOR ALL USING (true) WITH CHECK (true);

-- =====================================================
-- 3. CREAR TABLA recomendaciones
-- =====================================================

CREATE TABLE IF NOT EXISTS recomendaciones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
    oferta_id UUID REFERENCES ofertas_laborales(id) ON DELETE CASCADE,

    -- Resultado de la evaluacion
    match_score NUMERIC(4,3) CHECK (match_score >= 0 AND match_score <= 1),
    clasificacion TEXT CHECK (clasificacion IN ('APTO', 'CONSIDERADO', 'NO_APTO')),

    -- Detalle de scores
    scores_detalle JSONB,
    fortalezas TEXT[],
    debilidades TEXT[],

    -- Estado
    fue_vista BOOLEAN DEFAULT FALSE,
    vista_at TIMESTAMP WITH TIME ZONE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),

    -- Constraint unico: un usuario no puede tener multiples recomendaciones para la misma oferta
    CONSTRAINT unique_usuario_oferta UNIQUE (usuario_id, oferta_id)
);

-- Indices para recomendaciones
CREATE INDEX IF NOT EXISTS idx_recomendaciones_usuario ON recomendaciones(usuario_id);
CREATE INDEX IF NOT EXISTS idx_recomendaciones_oferta ON recomendaciones(oferta_id);
CREATE INDEX IF NOT EXISTS idx_recomendaciones_score ON recomendaciones(match_score DESC);
CREATE INDEX IF NOT EXISTS idx_recomendaciones_clasificacion ON recomendaciones(clasificacion);
CREATE INDEX IF NOT EXISTS idx_recomendaciones_vista ON recomendaciones(fue_vista);

-- Politica RLS para recomendaciones
ALTER TABLE recomendaciones ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Permitir acceso total recomendaciones" ON recomendaciones;
CREATE POLICY "Permitir acceso total recomendaciones" ON recomendaciones
FOR ALL USING (true) WITH CHECK (true);

-- =====================================================
-- 4. AGREGAR CAMPO nombre_completo A usuarios (si no existe)
-- =====================================================

ALTER TABLE usuarios
ADD COLUMN IF NOT EXISTS nombre_completo TEXT;

-- =====================================================
-- 5. FUNCIONES DE UTILIDAD
-- =====================================================

-- Funcion para actualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = timezone('utc', now());
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para perfiles_profesionales
DROP TRIGGER IF EXISTS update_perfiles_profesionales_updated_at ON perfiles_profesionales;
CREATE TRIGGER update_perfiles_profesionales_updated_at
    BEFORE UPDATE ON perfiles_profesionales
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para ofertas_laborales
DROP TRIGGER IF EXISTS update_ofertas_laborales_updated_at ON ofertas_laborales;
CREATE TRIGGER update_ofertas_laborales_updated_at
    BEFORE UPDATE ON ofertas_laborales
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- 6. VISTA PARA ESTADISTICAS ADMIN
-- =====================================================

CREATE OR REPLACE VIEW admin_estadisticas AS
SELECT
    (SELECT COUNT(*) FROM usuarios WHERE rol = 'estudiante') as total_estudiantes,
    (SELECT COUNT(*) FROM usuarios WHERE rol = 'titulado') as total_titulados,
    (SELECT COUNT(*) FROM usuarios WHERE rol IN ('administrador', 'admin')) as total_admins,
    (SELECT COUNT(*) FROM perfiles_profesionales WHERE is_complete = true) as perfiles_completos,
    (SELECT COUNT(*) FROM ofertas_laborales WHERE is_active = true AND tipo = 'pasantia') as pasantias_activas,
    (SELECT COUNT(*) FROM ofertas_laborales WHERE is_active = true AND tipo = 'empleo') as empleos_activos,
    (SELECT COUNT(*) FROM recomendaciones) as total_recomendaciones,
    (SELECT AVG(match_score) FROM recomendaciones) as promedio_match_score,
    (SELECT COUNT(*) FROM institutional_profiles WHERE is_active = true) as perfiles_institucionales_activos;

-- =====================================================
-- 7. INSERTAR DATOS DE PRUEBA (OPCIONAL)
-- =====================================================

-- Descomenta las siguientes lineas para insertar ofertas de prueba
-- despues de haber creado perfiles institucionales

/*
-- Ejemplo: Insertar oferta de pasantia para AGETIC
INSERT INTO ofertas_laborales (
    institutional_profile_id,
    titulo,
    descripcion,
    tipo,
    modalidad,
    ubicacion,
    fecha_inicio,
    fecha_cierre,
    cupos_disponibles
) VALUES (
    (SELECT id FROM institutional_profiles WHERE institution_name = 'AGETIC' LIMIT 1),
    'Pasantia en Desarrollo Web',
    'Buscamos estudiantes para pasantia en desarrollo de aplicaciones web con React y Python.',
    'pasantia',
    'hibrido',
    'La Paz, Bolivia',
    CURRENT_DATE,
    CURRENT_DATE + INTERVAL '3 months',
    3
);
*/

-- =====================================================
-- FIN DE MIGRACION
-- =====================================================
