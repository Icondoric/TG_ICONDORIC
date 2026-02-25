const AccountProfileView = () => import('@/features/account/views/AccountProfileView.vue')
const AccountSettingsView = () => import('@/features/account/views/AccountSettingsView.vue')

export default [
    {
        path: '/ver-mi-cuenta',
        name: 'ver-mi-cuenta',
        component: AccountProfileView,
        meta: { requiresAuth: true, hideNavbar: true }
    },
    {
        path: '/configurar-cuenta',
        name: 'configurar-cuenta',
        component: AccountSettingsView,
        meta: { requiresAuth: true, hideNavbar: true }
    }
]
