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

const adminMeta = { requiresAuth: true, requiresAdmin: true, hideNavbar: true }
const adminOnlyMeta = { requiresAuth: true, requiresAdminOnly: true, hideNavbar: true }

export default [
    {
        path: '/admin',
        name: 'admin',
        component: AdminDashboardView,
        meta: adminOnlyMeta
    },
    {
        path: '/admin/profiles',
        name: 'admin-profiles',
        component: ProfilesAdminView,
        meta: adminMeta
    },
    {
        path: '/admin/profiles/new',
        name: 'admin-profiles-new',
        component: ProfileFormView,
        meta: adminMeta
    },
    {
        path: '/admin/profiles/:id/edit',
        name: 'admin-profiles-edit',
        component: ProfileFormView,
        meta: adminMeta
    },
    {
        path: '/admin/users',
        name: 'admin-users',
        component: UsersAdminView,
        meta: adminMeta
    },
    {
        path: '/admin/users/new',
        name: 'admin-users-new',
        component: UserFormView,
        meta: adminMeta
    },
    {
        path: '/admin/users/:id',
        name: 'admin-users-detail',
        component: UserDetailView,
        meta: adminMeta
    },
    {
        path: '/admin/reports',
        name: 'admin-reports',
        component: ReportsView,
        meta: adminMeta
    },
    {
        path: '/admin/reports/users',
        name: 'admin-reports-users',
        component: UsersReportView,
        meta: adminMeta
    },
    {
        path: '/admin/reports/offers',
        name: 'admin-reports-offers',
        component: OffersReportView,
        meta: adminMeta
    },
    {
        path: '/admin/reports/profiles',
        name: 'admin-reports-profiles',
        component: ProfilesReportView,
        meta: adminMeta
    },
    {
        path: '/admin/ofertas',
        name: 'admin-ofertas',
        component: OfertasAdminView,
        meta: adminMeta
    },
    {
        path: '/admin/ofertas/new',
        name: 'admin-ofertas-new',
        component: OfertaFormView,
        meta: adminMeta
    },
    {
        path: '/admin/ofertas/edit/:id',
        name: 'admin-ofertas-edit',
        component: OfertaFormView,
        meta: adminMeta
    },
    {
        path: '/admin/ranking-candidatos',
        name: 'admin-ranking-candidatos',
        component: RankingCandidatosView,
        meta: adminMeta
    }
]
