const AdminDashboardView = () => import('@/features/admin/views/AdminDashboardView.vue')
const ProfilesAdminView = () => import('@/features/admin/views/ProfilesAdminView.vue')
const ProfileFormView = () => import('@/features/admin/views/ProfileFormView.vue')
const UsersAdminView = () => import('@/features/admin/views/UsersAdminView.vue')
const UserDetailView = () => import('@/features/admin/views/UserDetailView.vue')
const UserFormView = () => import('@/features/admin/views/UserFormView.vue')
const ReportsView = () => import('@/features/admin/views/ReportsView.vue')
const UsersReportView = () => import('@/features/admin/views/UsersReportView.vue')
const OffersReportView = () => import('@/features/admin/views/OffersReportView.vue')
const ProfilesReportView = () => import('@/features/admin/views/ProfilesReportView.vue')
const OfertasAdminView = () => import('@/features/admin/views/OfertasAdminView.vue')
const OfertaFormView = () => import('@/features/admin/views/OfertaFormView.vue')
const RankingCandidatosView = () => import('@/features/admin/views/RankingCandidatosView.vue')
const RankingDetalleView = () => import('@/features/admin/views/RankingDetalleView.vue')
const CandidatoPerfilAdminView = () => import('@/features/admin/views/CandidatoPerfilAdminView.vue')

const base = { requiresAuth: true, hideNavbar: true }

export default [
    {
        path: '/admin',
        name: 'admin',
        component: AdminDashboardView,
        meta: { ...base, requiresAdminOnly: true }
    },

    // Gestión de Usuarios
    {
        path: '/admin/users',
        name: 'admin-users',
        component: UsersAdminView,
        meta: { ...base, requiresAdmin: true, moduleId: 'gestion_usuarios', submoduleId: 'lista_usuarios' }
    },
    {
        path: '/admin/users/new',
        name: 'admin-users-new',
        component: UserFormView,
        meta: { ...base, requiresAdmin: true, moduleId: 'gestion_usuarios', submoduleId: 'nuevo_usuario' }
    },
    {
        path: '/admin/users/:id',
        name: 'admin-users-detail',
        component: UserDetailView,
        meta: { ...base, requiresAdmin: true, moduleId: 'gestion_usuarios', submoduleId: 'lista_usuarios' }
    },

    // Perfiles Institucionales
    {
        path: '/admin/profiles',
        name: 'admin-profiles',
        component: ProfilesAdminView,
        meta: { ...base, requiresAdmin: true, moduleId: 'perfiles_institucionales', submoduleId: 'ver_perfiles' }
    },
    {
        path: '/admin/profiles/new',
        name: 'admin-profiles-new',
        component: ProfileFormView,
        meta: { ...base, requiresAdmin: true, moduleId: 'perfiles_institucionales', submoduleId: 'nuevo_perfil' }
    },
    {
        path: '/admin/profiles/:id/edit',
        name: 'admin-profiles-edit',
        component: ProfileFormView,
        meta: { ...base, requiresAdmin: true, moduleId: 'perfiles_institucionales', submoduleId: 'nuevo_perfil' }
    },

    // Informes y Reportes
    {
        path: '/admin/reports',
        name: 'admin-reports',
        component: ReportsView,
        meta: { ...base, requiresAdmin: true, moduleId: 'informes_reportes', submoduleId: 'resumen_general' }
    },
    {
        path: '/admin/reports/users',
        name: 'admin-reports-users',
        component: UsersReportView,
        meta: { ...base, requiresAdmin: true, moduleId: 'informes_reportes', submoduleId: 'reporte_usuarios' }
    },
    {
        path: '/admin/reports/offers',
        name: 'admin-reports-offers',
        component: OffersReportView,
        meta: { ...base, requiresAdmin: true, moduleId: 'informes_reportes', submoduleId: 'reporte_ofertas' }
    },
    {
        path: '/admin/reports/profiles',
        name: 'admin-reports-profiles',
        component: ProfilesReportView,
        meta: { ...base, requiresAdmin: true, moduleId: 'informes_reportes', submoduleId: 'reporte_perfiles' }
    },

    // Gestión de Oferta Laboral
    {
        path: '/admin/ofertas',
        name: 'admin-ofertas',
        component: OfertasAdminView,
        meta: { ...base, requiresAdmin: true, moduleId: 'oferta_laboral', submoduleId: 'ver_ofertas' }
    },
    {
        path: '/admin/ofertas/new',
        name: 'admin-ofertas-new',
        component: OfertaFormView,
        meta: { ...base, requiresAdmin: true, moduleId: 'oferta_laboral', submoduleId: 'nueva_oferta' }
    },
    {
        path: '/admin/ofertas/edit/:id',
        name: 'admin-ofertas-edit',
        component: OfertaFormView,
        meta: { ...base, requiresAdmin: true, moduleId: 'oferta_laboral', submoduleId: 'nueva_oferta' }
    },

    // Evaluación de Perfiles — ranking (admin only)
    {
        path: '/admin/ranking-candidatos',
        name: 'admin-ranking-candidatos',
        component: RankingCandidatosView,
        meta: { ...base, requiresAdmin: true, moduleId: 'evaluacion_perfiles', submoduleId: 'ranking_candidatos' }
    },
    {
        path: '/admin/ranking-candidatos/:id',
        name: 'admin-ranking-detalle',
        component: RankingDetalleView,
        meta: { ...base, requiresAdmin: true, moduleId: 'evaluacion_perfiles', submoduleId: 'ranking_candidatos' }
    },
    {
        path: '/admin/candidato/:userId/perfil',
        name: 'admin-candidato-perfil',
        component: CandidatoPerfilAdminView,
        meta: { ...base, requiresAdmin: true, moduleId: 'evaluacion_perfiles', submoduleId: 'ranking_candidatos' }
    }
]
