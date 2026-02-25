-- =====================================================
-- MIGRACION V3: CONTACTO Y CONFIG POR OFERTA
-- =====================================================
-- Ejecutar en Supabase SQL Editor
-- Fecha: 2026-02-24
-- =====================================================

-- =====================================================
-- 1. CAMPOS DE CONTACTO EN institutional_profiles
--    (area solo pertenece a la oferta, no al perfil)
-- =====================================================

ALTER TABLE institutional_profiles
  ADD COLUMN IF NOT EXISTS contact_phone TEXT,
  ADD COLUMN IF NOT EXISTS contact_email TEXT,
  ADD COLUMN IF NOT EXISTS ubicacion TEXT;

-- =====================================================
-- 2. CAMPOS EN ofertas_laborales
--    - Configuracion propia (weights/thresholds/requirements)
--      Si son NULL, se hereda del perfil institucional
--    - Contacto y area especificos de la oferta
-- =====================================================

ALTER TABLE ofertas_laborales
  ADD COLUMN IF NOT EXISTS weights      JSONB,
  ADD COLUMN IF NOT EXISTS thresholds   JSONB,
  ADD COLUMN IF NOT EXISTS requirements JSONB,
  ADD COLUMN IF NOT EXISTS contact_phone TEXT,
  ADD COLUMN IF NOT EXISTS contact_email TEXT,
  ADD COLUMN IF NOT EXISTS area TEXT;

-- =====================================================
-- FIN DE MIGRACION V3
-- =====================================================
