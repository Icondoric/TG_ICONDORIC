export const MODULES = [
    { id: 'gestion_usuarios',         label: 'Gestión de Usuarios' },
    { id: 'digitalizacion_perfiles',  label: 'Digitalización de Perfiles' },
    { id: 'oferta_laboral',           label: 'Gestión de Convocatorias' },
    { id: 'perfiles_institucionales', label: 'Perfiles Institucionales' },
    { id: 'evaluacion_perfiles',      label: 'Evaluación de Perfiles' },
    { id: 'informes_reportes',        label: 'Informes y Reportes' },
]

// Sub-módulos de cada módulo (id, label)
export const SUB_MODULES = {
    gestion_usuarios: [
        { id: 'lista_usuarios', label: 'Lista de Usuarios' },
        { id: 'nuevo_usuario',  label: 'Nuevo Usuario' },
    ],
    digitalizacion_perfiles: [
        { id: 'subir_cv',        label: 'Subir CV' },
        { id: 'mi_perfil',       label: 'Mi Perfil Digitalizado' },
        { id: 'editar_perfil',   label: 'Editar Perfil' },
        { id: 'buscar_perfiles', label: 'Buscar Perfiles' },
    ],
    oferta_laboral: [
        { id: 'ver_ofertas',  label: 'Ver Convocatorias' },
        { id: 'nueva_oferta', label: 'Nueva / Editar Convocatoria' },
    ],
    perfiles_institucionales: [
        { id: 'ver_perfiles',  label: 'Ver Perfiles' },
        { id: 'nuevo_perfil',  label: 'Nuevo / Editar Perfil' },
    ],
    evaluacion_perfiles: [
        { id: 'correspondencia',    label: 'Correspondencia entre Perfiles' },
        { id: 'historial',          label: 'Historial de Postulaciones' },
        { id: 'ranking_candidatos', label: 'Evaluación de Candidatos' },
    ],
    informes_reportes: [
        { id: 'resumen_general',       label: 'Resumen General' },
        { id: 'reporte_usuarios',      label: 'Reporte de Usuarios' },
        { id: 'reporte_ofertas',       label: 'Reporte de Convocatorias' },
        { id: 'reporte_perfiles',      label: 'Reporte de Perfiles' },
        { id: 'reporte_cumplimiento',  label: 'Cumplimiento por Convocatoria' },
        { id: 'reporte_cargos',        label: 'Cargos por Tipo de Institución' },
    ],
}

// Permisos de roles fijos. Formato: { moduleId: [submoduleId, ...] }
export const FIXED_ROLE_MODULES = {
    administrador: {
        gestion_usuarios:         ['lista_usuarios', 'nuevo_usuario'],
        digitalizacion_perfiles:  ['subir_cv', 'mi_perfil', 'editar_perfil', 'buscar_perfiles'],
        oferta_laboral:           ['ver_ofertas', 'nueva_oferta'],
        perfiles_institucionales: ['ver_perfiles', 'nuevo_perfil'],
        evaluacion_perfiles:      ['correspondencia', 'historial', 'ranking_candidatos'],
        informes_reportes:        ['resumen_general', 'reporte_usuarios', 'reporte_ofertas', 'reporte_perfiles', 'reporte_cumplimiento', 'reporte_cargos'],
    },
    operador: {
        gestion_usuarios:         ['lista_usuarios', 'nuevo_usuario'],
        digitalizacion_perfiles:  ['buscar_perfiles'],
        oferta_laboral:           ['ver_ofertas', 'nueva_oferta'],
        perfiles_institucionales: ['ver_perfiles', 'nuevo_perfil'],
        informes_reportes:        ['resumen_general', 'reporte_usuarios', 'reporte_ofertas', 'reporte_perfiles', 'reporte_cumplimiento', 'reporte_cargos'],
    },
    estudiante: {
        digitalizacion_perfiles: ['subir_cv', 'mi_perfil', 'editar_perfil'],
        evaluacion_perfiles:     ['correspondencia', 'historial'],
    },
    titulado: {
        digitalizacion_perfiles: ['subir_cv', 'mi_perfil', 'editar_perfil'],
        evaluacion_perfiles:     ['correspondencia', 'historial'],
    },
}
