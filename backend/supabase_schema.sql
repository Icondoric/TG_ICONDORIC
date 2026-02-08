-- COPIA Y PEGA ESTO EN EL SQL EDITOR DE SUPABASE

-- 1. Tabla de Usuarios (Auth personalizada)
CREATE TABLE IF NOT EXISTS usuarios (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    rol TEXT NOT NULL CHECK (rol IN ('estudiante', 'titulado', 'administrador', 'admin', 'operador')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);

-- 2. Tabla de Perfiles Profesionales (JSONB)
CREATE TABLE IF NOT EXISTS perfiles_profesionales (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE, -- Si se borra el user, se borra el perfil
    data JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now())
);

-- 3. Índices para búsqueda rápida dentro del JSONB
CREATE INDEX IF NOT EXISTS idx_perfiles_data ON perfiles_profesionales USING GIN (data);

-- 4. Políticas de seguridad (Row Level Security - RLS)
-- Habilitamos RLS
ALTER TABLE usuarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE perfiles_profesionales ENABLE ROW LEVEL SECURITY;

-- Política simple: Permitir todo acceso 'anon' (público) por ahora,
-- ya que nuestra API gestiona la seguridad. 
-- Supabase por defecto bloquea todo si RLS está ON y no hay policies.
-- En producción, restringiríamos esto para que solo la API key de servicio ("service_role") pueda escribir,
-- o crearíamos policies basadas en auth.uid() de Supabase Auth (pero nosotros usamos Auth custom).
-- Para no bloquearnos con errores "permission denied" usando la 'anon' key desde el backend:
CREATE POLICY "Permitir acceso total api anon" ON usuarios
FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Permitir acceso total api anon perfiles" ON perfiles_profesionales
FOR ALL USING (true) WITH CHECK (true);

-- Nota: Como estamos haciendo Auth custom en el Backend, el Backend actuará con privilegios.
-- Si usas la 'anon' key, estas policies 'true' son necesarias.
-- Lo ideal sería usar la 'service_role' key en el Backend para saltarse RLS,
-- pero para empezar 'anon' + policies permisivas funciona bien.
