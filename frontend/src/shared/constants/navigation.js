// SVG path icons
const icons = {
    users: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z',
    profile: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
    evaluation: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4',
    ofertas: 'M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
    instituciones: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4',
    reports: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
    settings: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z',
}

// Mapa completo: módulo ID → definición de menú con submoduleId en cada child.
// Usado para construir dinámicamente el menú de roles personalizados.
const MODULE_MENU_ITEMS = {
    gestion_usuarios: {
        label: 'Gestión de Usuarios', icon: icons.users, children: [
            { label: 'Lista de Usuarios', path: '/admin/users', submoduleId: 'lista_usuarios' },
            { label: 'Nuevo Usuario', path: '/admin/users/new', submoduleId: 'nuevo_usuario' },
        ]
    },
    digitalizacion_perfiles: {
        label: 'Digitalización de Perfiles', icon: icons.profile, children: [
            { label: 'Subir CV', path: '/digitalizacion/subir-cv', submoduleId: 'subir_cv' },
            { label: 'Mi Perfil Digitalizado', path: '/digitalizacion/mi-perfil', submoduleId: 'mi_perfil' },
            { label: 'Editar Perfil', path: '/digitalizacion/editar', submoduleId: 'editar_perfil' },
            { label: 'Buscar Perfiles', path: '/digitalizacion/buscar-perfiles', submoduleId: 'buscar_perfiles' },
        ]
    },
    oferta_laboral: {
        label: 'Gestión de Oferta Laboral', icon: icons.ofertas, children: [
            { label: 'Lista de Ofertas Laborales', path: '/admin/ofertas', submoduleId: 'ver_ofertas' },
            { label: 'Nueva Oferta', path: '/admin/ofertas/new', submoduleId: 'nueva_oferta' },
        ]
    },
    perfiles_institucionales: {
        label: 'Perfiles Institucionales', icon: icons.instituciones, children: [
            { label: 'Lista de Perfiles Institucionales', path: '/admin/profiles', submoduleId: 'ver_perfiles' },
            { label: 'Nuevo Perfil', path: '/admin/profiles/new', submoduleId: 'nuevo_perfil' },
        ]
    },
    evaluacion_perfiles: {
        label: 'Evaluación de Perfiles', icon: icons.evaluation, children: [
            { label: 'Lista de Perfiles Calificados', path: '/mis-recomendaciones', submoduleId: 'correspondencia' },
            { label: 'Correspondencia entre Perfiles', path: '/correspondencia-perfiles', submoduleId: 'correspondencia' },
            { label: 'Historial de Postulaciones', path: '/historial-postulaciones', submoduleId: 'historial' },
            { label: 'Evaluación de Candidatos', path: '/admin/ranking-candidatos', submoduleId: 'ranking_candidatos' },
        ]
    },
    informes_reportes: {
        label: 'Informes y Reportes', icon: icons.reports, children: [
            { label: 'Resumen General', path: '/admin/reports', submoduleId: 'resumen_general' },
            { label: 'Reporte de Usuarios', path: '/admin/reports/users', submoduleId: 'reporte_usuarios' },
            { label: 'Reporte de Ofertas', path: '/admin/reports/offers', submoduleId: 'reporte_ofertas' },
            { label: 'Reporte de Perfiles', path: '/admin/reports/profiles', submoduleId: 'reporte_perfiles' },
        ]
    },
}

const FIXED_ROLES = ['admin', 'administrador', 'operador', 'estudiante', 'titulado']

/**
 * Returns sidebar menu items based on user role.
 * @param {string} role
 * @param {Object|null} allowedModules - { moduleId: [submoduleId, ...] } para roles personalizados
 */
export function getMenuItems(role, allowedModules = null) {
    // Rol personalizado: construir menú dinámico filtrando módulos Y sub-módulos permitidos
    if (allowedModules !== null && !FIXED_ROLES.includes(role)) {
        return Object.entries(allowedModules)
            .filter(([id]) => MODULE_MENU_ITEMS[id])
            .map(([id, allowedSubs]) => {
                const item = MODULE_MENU_ITEMS[id]
                const children = item.children.filter(c => allowedSubs.includes(c.submoduleId))
                return { ...item, children }
            })
            .filter(item => item.children.length > 0)
    }

    switch (role) {
        case 'admin':
        case 'administrador':
            return [
                {
                    label: 'Gestión de Usuarios', icon: icons.users, children: [
                        { label: 'Lista de Usuarios', path: '/admin/users' },
                        { label: 'Nuevo Usuario', path: '/admin/users/new' },
                    ]
                },
                {
                    label: 'Digitalización de Perfiles', icon: icons.profile, children: [
                        { label: 'Subir CV', path: '/digitalizacion/subir-cv' },
                        { label: 'Mi Perfil Digitalizado', path: '/digitalizacion/mi-perfil' },
                        { label: 'Editar Perfil', path: '/digitalizacion/editar' },
                        { label: 'Buscar Perfiles', path: '/digitalizacion/buscar-perfiles' },
                    ]
                },
                {
                    label: 'Gestión de Oferta Laboral', icon: icons.ofertas, children: [
                        { label: 'Lista de Ofertas Laborales', path: '/admin/ofertas' },
                        { label: 'Nueva Oferta', path: '/admin/ofertas/new' },
                    ]
                },
                {
                    label: 'Perfiles Institucionales', icon: icons.instituciones, children: [
                        { label: 'Lista de Perfiles Institucionales', path: '/admin/profiles' },
                        { label: 'Nuevo Perfil', path: '/admin/profiles/new' },
                    ]
                },
                {
                    label: 'Evaluación de Perfiles', icon: icons.evaluation, children: [
                        { label: 'Lista de Perfiles Calificados', path: '/mis-recomendaciones' },
                        { label: 'Correspondencia entre Perfiles', path: '/correspondencia-perfiles' },
                        { label: 'Historial de Postulaciones', path: '/historial-postulaciones' },
                        { label: 'Evaluación de Candidatos', path: '/admin/ranking-candidatos' },
                    ]
                },
                {
                    label: 'Informes y Reportes', icon: icons.reports, children: [
                        { label: 'Resumen General', path: '/admin/reports' },
                        { label: 'Reporte de Usuarios', path: '/admin/reports/users' },
                        { label: 'Reporte de Ofertas', path: '/admin/reports/offers' },
                        { label: 'Reporte de Perfiles', path: '/admin/reports/profiles' },
                    ]
                },
                {
                    label: 'Gestión de Sistema', icon: icons.settings, children: [
                        { label: 'Roles', path: '/admin/system/roles' },
                    ]
                },
            ]

        case 'operador':
            return [
                {
                    label: 'Gestión de Usuarios', icon: icons.users, children: [
                        { label: 'Ver Usuarios', path: '/admin/users' },
                        { label: 'Nuevo Usuario', path: '/admin/users/new' },
                    ]
                },
                {
                    label: 'Digitalización de Perfiles', icon: icons.profile, children: [
                        { label: 'Buscar Perfiles', path: '/digitalizacion/buscar-perfiles' },
                    ]
                },
                {
                    label: 'Gestión de Oferta Laboral', icon: icons.ofertas, children: [
                        { label: 'Lista de Ofertas Laborales', path: '/admin/ofertas' },
                        { label: 'Nueva Oferta', path: '/admin/ofertas/new' },
                    ]
                },
                {
                    label: 'Perfiles Institucionales', icon: icons.instituciones, children: [
                        { label: 'Lista de Perfiles Institucionales', path: '/admin/profiles' },
                        { label: 'Nuevo Perfil', path: '/admin/profiles/new' },
                    ]
                },
                {
                    label: 'Informes y Reportes', icon: icons.reports, children: [
                        { label: 'Resumen General', path: '/admin/reports' },
                        { label: 'Reporte de Usuarios', path: '/admin/reports/users' },
                        { label: 'Reporte de Ofertas', path: '/admin/reports/offers' },
                        { label: 'Reporte de Perfiles', path: '/admin/reports/profiles' },
                    ]
                },
            ]

        case 'estudiante':
        case 'titulado':
        default:
            return [
                {
                    label: 'Digitalización de Perfiles', icon: icons.profile, children: [
                        { label: 'Subir CV', path: '/digitalizacion/subir-cv' },
                        { label: 'Mi Perfil Digitalizado', path: '/digitalizacion/mi-perfil' },
                        { label: 'Editar Perfil', path: '/digitalizacion/editar' },
                    ]
                },
                {
                    label: 'Evaluación de Perfiles', icon: icons.evaluation, children: [
                        { label: 'Lista de Perfiles Calificados', path: '/mis-recomendaciones' },
                        { label: 'Correspondencia entre Perfiles', path: '/correspondencia-perfiles' },
                        { label: 'Historial de Postulaciones', path: '/historial-postulaciones' },
                    ]
                },
            ]
    }
}

/**
 * Returns sidebar color variant based on user role.
 */
export function getSidebarVariant(role) {
    return ['admin', 'administrador', 'operador'].includes(role) ? 'dark' : 'light'
}

// Backward compat exports (used by views that haven't been updated yet)
export const adminMenuItems = getMenuItems('administrador')
export const studentMenuItems = getMenuItems('estudiante')
