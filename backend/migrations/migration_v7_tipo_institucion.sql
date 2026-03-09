-- Migration v7: Agregar tipo_institucion a perfiles institucionales
-- Opciones: Pública, Privada, Mixta, ONG

ALTER TABLE institutional_profiles
  ADD COLUMN IF NOT EXISTS tipo_institucion TEXT
    CHECK (tipo_institucion IN ('Pública', 'Privada', 'Mixta', 'ONG') OR tipo_institucion IS NULL);
