const AccountSettingsView = () => import('@/features/account/views/AccountSettingsView.vue')

export default [
    {
        path: '/configuracion-cuenta',
        name: 'configuracion-cuenta',
        component: AccountSettingsView,
        meta: { requiresAuth: true, hideNavbar: true }
    }
]
