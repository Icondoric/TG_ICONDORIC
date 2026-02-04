<script setup>
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { useUiStore } from '../../stores/ui'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUiStore()

const isActive = (path) => route.path === path || route.path.startsWith(path + '/')

const menuItems = [
    {
        label: 'Digitalización de Perfiles',
        path: '/mi-perfil',
        icon: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
    },
    {
        label: 'Mis Recomendaciones',
        path: '/mis-recomendaciones',
        icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4',
    }
]

const handleLogout = () => {
    authStore.logout()
    router.push('/login')
}
</script>

<template>
    <aside 
        class="hidden lg:flex flex-col fixed inset-y-0 left-0 bg-white border-r border-gray-200 transition-all duration-300 transform z-40 shadow-sm"
        :class="uiStore.isSidebarOpen ? 'w-64' : 'w-20'"
    >
        <!-- Header -->
        <div class="flex items-center justify-between h-16 border-b border-gray-200 px-4">
            <img 
                v-if="uiStore.isSidebarOpen" 
                src="@/assets/icons/logoEmi.png" 
                alt="Logo EMI" 
                class="h-10 w-auto cursor-pointer hover:opacity-80 transition-opacity" 
                @click="router.push('/')"
            />
            <button 
                @click="uiStore.toggleSidebar" 
                class="text-gray-600 hover:text-emi-navy-500 focus:outline-none ml-auto"
                :title="uiStore.isSidebarOpen ? 'Contraer sidebar' : 'Expandir sidebar'"
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
            </button>
        </div>

        <!-- Menu Items -->
        <div class="flex-1 overflow-y-auto py-4">
            <nav class="space-y-1 px-2">
                <router-link
                    v-for="item in menuItems"
                    :key="item.path"
                    :to="item.path"
                    :title="!uiStore.isSidebarOpen ? item.label : ''"
                    :class="[
                        'group flex items-center px-3 py-3 text-sm font-medium rounded-md transition-colors duration-150',
                        isActive(item.path) 
                            ? item.path === '/mi-perfil'
                                ? 'bg-emi-navy-500 text-white'
                                : 'bg-emi-gold-500 text-emi-navy-800'
                            : 'text-gray-700 hover:bg-gray-100 hover:text-emi-navy-500',
                        !uiStore.isSidebarOpen ? 'justify-center' : ''
                    ]"
                >
                    <svg 
                        class="h-6 w-6 flex-shrink-0" 
                        :class="[
                            isActive(item.path) ? 'text-current' : 'text-gray-500 group-hover:text-emi-navy-500',
                            uiStore.isSidebarOpen ? 'mr-3' : ''
                        ]"
                        fill="none" 
                        stroke="currentColor" 
                        viewBox="0 0 24 24"
                    >
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
                    </svg>
                    <span v-if="uiStore.isSidebarOpen" class="truncate">{{ item.label }}</span>
                </router-link>
            </nav>
        </div>

        <!-- Footer / Logout -->
        <div class="p-4 border-t border-gray-200">
            <button 
                @click="handleLogout"
                class="w-full flex items-center px-3 py-2 text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 transition-colors duration-150 shadow-sm"
                :class="!uiStore.isSidebarOpen ? 'justify-center' : ''"
                :title="!uiStore.isSidebarOpen ? 'Cerrar Sesión' : ''"
            >
                <svg class="h-5 w-5" :class="uiStore.isSidebarOpen ? 'mr-2' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                     <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                <span v-if="uiStore.isSidebarOpen">Cerrar Sesión</span>
            </button>
        </div>
    </aside>

    <!-- Mobile Sidebar -->
    <div
        v-if="uiStore.isMobileSidebarOpen"
        class="lg:hidden fixed inset-0 z-50 bg-gray-900 bg-opacity-50"
        @click="uiStore.closeMobileSidebar"
    >
        <aside
            class="fixed inset-y-0 left-0 w-64 bg-white shadow-xl transform transition-transform duration-300"
            @click.stop
        >
            <!-- Mobile Header -->
            <div class="flex items-center justify-between h-16 border-b border-gray-200 px-4">
                <img src="@/assets/icons/logoEmi.png" alt="Logo EMI" class="h-10 w-auto" />
                <button 
                    @click="uiStore.closeMobileSidebar" 
                    class="text-gray-600 hover:text-emi-navy-500"
                >
                    <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            <!-- Mobile Menu -->
            <div class="py-4">
                <nav class="space-y-1 px-2">
                    <router-link
                        v-for="item in menuItems"
                        :key="item.path"
                        :to="item.path"
                        @click="uiStore.closeMobileSidebar"
                        :class="[
                            'group flex items-center px-3 py-3 text-sm font-medium rounded-md transition-colors',
                            isActive(item.path) 
                                ? item.path === '/mi-perfil'
                                    ? 'bg-emi-navy-500 text-white'
                                    : 'bg-emi-gold-500 text-emi-navy-800'
                                : 'text-gray-700 hover:bg-gray-100'
                        ]"
                    >
                        <svg class="h-6 w-6 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
                        </svg>
                        <span>{{ item.label }}</span>
                    </router-link>
                </nav>
            </div>

            <!-- Mobile Logout -->
            <div class="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200">
                <button 
                    @click="handleLogout"
                    class="w-full flex items-center justify-center px-3 py-2 text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 transition-colors shadow-sm"
                >
                    <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    Cerrar Sesión
                </button>
            </div>
        </aside>
    </div>

    <!-- Mobile Toggle Button -->
    <button
        @click="uiStore.toggleMobileSidebar"
        class="lg:hidden fixed bottom-4 right-4 z-40 p-3 bg-emi-navy-500 text-white rounded-full shadow-lg hover:bg-emi-navy-600 transition-colors"
    >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
    </button>
</template>
