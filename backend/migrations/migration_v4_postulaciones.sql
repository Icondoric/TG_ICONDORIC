-- =====================================================
-- MIGRACION V4: TABLA POSTULACIONES
-- =====================================================
-- Ejecutar en Supabase SQL Editor
-- Fecha: 2026-02-24
-- =====================================================
-- Almacena las postulaciones explícitas de usuarios a ofertas.
-- Una postulacion = el usuario eligió una oferta y fue evaluado contra ella.
-- Diferente a "recomendaciones" (sistema automático).
-- =====================================================

CREATE TABLE IF NOT EXISTS postulaciones (
    id             UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    usuario_id     UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    oferta_id      UUID NOT NULL REFERENCES ofertas_laborales(id) ON DELETE CASCADE,

    -- Resultado de evaluación ML
    match_score    NUMERIC(4,3) CHECK (match_score >= 0 AND match_score <= 1),
    clasificacion  TEXT CHECK (clasificacion IN ('APTO', 'CONSIDERADO', 'NO_APTO')),
    scores_detalle JSONB,
    fortalezas     TEXT[],
    debilidades    TEXT[],
    match_details  JSONB,

    -- Estado de la postulación (para vista de admin - fase posterior)
    estado         TEXT DEFAULT 'pendiente'
                   CHECK (estado IN ('pendiente', 'en_revision', 'aceptado', 'rechazado')),

    created_at     TIMESTAMPTZ DEFAULT NOW(),
    updated_at     TIMESTAMPTZ DEFAULT NOW(),

    -- Un usuario solo puede postular una vez por oferta
    UNIQUE (usuario_id, oferta_id)
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_postulaciones_usuario
    ON postulaciones(usuario_id);

CREATE INDEX IF NOT EXISTS idx_postulaciones_oferta
    ON postulaciones(oferta_id);

CREATE INDEX IF NOT EXISTS idx_postulaciones_score
    ON postulaciones(match_score DESC);

CREATE INDEX IF NOT EXISTS idx_postulaciones_clasificacion
    ON postulaciones(clasificacion);

CREATE INDEX IF NOT EXISTS idx_postulaciones_estado
    ON postulaciones(estado);

CREATE INDEX IF NOT EXISTS idx_postulaciones_created
    ON postulaciones(created_at DESC);

-- =====================================================
-- FIN DE MIGRACION V4
-- =====================================================
