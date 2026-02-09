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

/**
 * Returns sidebar menu items based on user role.
 * Items can have a `path` (direct link) or `children` (submenu).
 */
export function getMenuItems(role) {
    switch (role) {
        case 'admin':
        case 'administrador':
            return [
                { label: 'Gestión de Usuarios', path: '/admin/users', icon: icons.users },
                { label: 'Digitalización de Perfiles', path: '/mi-perfil', icon: icons.profile },
                {
                    label: 'Evaluación de Perfiles', icon: icons.evaluation, children: [
                        { label: 'Evaluar CV', path: '/evaluation' },
                        { label: 'Dashboard', path: '/admin' },
                    ]
                },
                { label: 'Gestión de Oferta Laboral', path: '/admin/ofertas', icon: icons.ofertas },
                { label: 'Perfiles Institucionales', path: '/admin/profiles', icon: icons.instituciones },
                { label: 'Informes y Reportes', path: '/admin/reports', icon: icons.reports },
            ]

        case 'operador':
            return [
                { label: 'Gestión de Usuarios', path: '/admin/users', icon: icons.users },
                { label: 'Gestión de Oferta Laboral', path: '/admin/ofertas', icon: icons.ofertas },
                { label: 'Perfiles Institucionales', path: '/admin/profiles', icon: icons.instituciones },
                { label: 'Informes y Reportes', path: '/admin/reports', icon: icons.reports },
            ]

        case 'estudiante':
        case 'titulado':
        default:
            return [
                { label: 'Gestión de Usuarios', path: '/configuracion-cuenta', icon: icons.settings },
                { label: 'Digitalización de Perfiles', path: '/mi-perfil', icon: icons.profile },
                {
                    label: 'Evaluación de Perfiles', icon: icons.evaluation, children: [
                        { label: 'Evaluar CV', path: '/evaluation' },
                        { label: 'Historial', path: '/history' },
                        { label: 'Recomendaciones', path: '/mis-recomendaciones' },
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
