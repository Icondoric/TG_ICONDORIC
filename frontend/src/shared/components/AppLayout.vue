<script setup>
import { computed } from 'vue'
import AppSidebar from './AppSidebar.vue'
import { useUiStore } from '@/shared/stores/ui'
import { useAuthStore } from '@/features/auth/store/auth.store'
import { getMenuItems, getSidebarVariant } from '@/shared/constants/navigation'

const uiStore = useUiStore()
const authStore = useAuthStore()

const menuItems = computed(() => getMenuItems(authStore.user?.rol, authStore.allowedModules))
const variant = computed(() => getSidebarVariant(authStore.user?.rol))
const isDark = computed(() => getSidebarVariant(authStore.user?.rol) === 'dark')
</script>

<template>
    <div class="min-h-screen bg-slate-50">
        <!-- Mobile Topbar (visible solo en < lg) -->
        <header
            class="lg:hidden fixed top-0 left-0 right-0 z-40 h-14 flex items-center justify-between px-4 shadow-sm"
            :class="isDark ? 'bg-emi-navy-900 border-b border-emi-navy-700' : 'bg-white border-b border-gray-200'"
        >
            <button
                @click="uiStore.toggleMobileSidebar"
                class="p-1.5 rounded-md focus:outline-none"
                :class="isDark ? 'text-white hover:bg-emi-navy-700' : 'text-gray-600 hover:bg-gray-100'"
                aria-label="Abrir menú"
            >
                <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
            </button>
            <img
                src="@/shared/assets/icons/logoEmi.png"
                alt="Logo EMI"
                class="h-9 w-auto"
            />
            <div class="w-9" /><!-- spacer para centrar logo -->
        </header>

        <div class="flex">
            <AppSidebar :menuItems="menuItems" :variant="variant" />
            <main
                class="flex-1 min-w-0 overflow-x-auto transition-all duration-300 min-h-screen pt-14 lg:pt-0"
                :class="uiStore.isSidebarOpen ? 'lg:ml-64' : 'lg:ml-20'"
            >
                <slot />
            </main>
        </div>
    </div>
</template>
