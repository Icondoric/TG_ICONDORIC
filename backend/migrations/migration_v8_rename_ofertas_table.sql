-- Migration v8: Rename ofertas_laborales → convocatorias_laborales
-- This aligns the database table name with the updated frontend/backend terminology.
-- Date: 2026-03-08

-- 1. Rename the main table
ALTER TABLE ofertas_laborales RENAME TO convocatorias_laborales;

-- 2. Rename the sequence (if exists, auto-created by Supabase for bigint PKs)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_sequences WHERE sequencename = 'ofertas_laborales_id_seq') THEN
        ALTER SEQUENCE ofertas_laborales_id_seq RENAME TO convocatorias_laborales_id_seq;
    END IF;
END $$;

-- 3. Rename indexes that reference the old table name (if any)
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN
        SELECT indexname FROM pg_indexes
        WHERE tablename = 'convocatorias_laborales'
          AND indexname LIKE 'ofertas_laborales%'
    LOOP
        EXECUTE format('ALTER INDEX %I RENAME TO %I',
            r.indexname,
            replace(r.indexname, 'ofertas_laborales', 'convocatorias_laborales'));
    END LOOP;
END $$;
