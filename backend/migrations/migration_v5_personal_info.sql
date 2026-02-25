-- ============================================================
-- Migration v5: Información Personal en perfiles_profesionales
-- Agrega campos de datos personales extraídos del CV
-- Ejecutar en: Supabase Dashboard → SQL Editor
-- ============================================================

ALTER TABLE perfiles_profesionales
  ADD COLUMN IF NOT EXISTS nombre_completo  TEXT,
  ADD COLUMN IF NOT EXISTS direccion        TEXT,
  ADD COLUMN IF NOT EXISTS telefono         TEXT,
  ADD COLUMN IF NOT EXISTS email_contacto   TEXT,
  ADD COLUMN IF NOT EXISTS nacionalidad     TEXT;

-- Comentarios descriptivos
COMMENT ON COLUMN perfiles_profesionales.nombre_completo IS 'Nombre completo extraído del CV (puede diferir del nombre de registro)';
COMMENT ON COLUMN perfiles_profesionales.direccion       IS 'Dirección/ubicación extraída del CV';
COMMENT ON COLUMN perfiles_profesionales.telefono        IS 'Teléfono de contacto extraído del CV';
COMMENT ON COLUMN perfiles_profesionales.email_contacto  IS 'Email de contacto del CV (puede diferir del email de login)';
COMMENT ON COLUMN perfiles_profesionales.nacionalidad    IS 'Nacionalidad extraída del CV';
