<script setup>
import { computed } from 'vue'
import AppSidebar from './AppSidebar.vue'
import { useUiStore } from '@/shared/stores/ui'
import { useAuthStore } from '@/features/auth/store/auth.store'
import { getMenuItems, getSidebarVariant } from '@/shared/constants/navigation'

const uiStore = useUiStore()
const authStore = useAuthStore()

const menuItems = computed(() => getMenuItems(authStore.user?.rol))
const variant = computed(() => getSidebarVariant(authStore.user?.rol))
</script>

<template>
    <div class="min-h-screen bg-slate-50">
        <div class="flex">
            <AppSidebar :menuItems="menuItems" :variant="variant" />
            <main
                class="flex-1 transition-all duration-300 min-h-screen"
                :class="uiStore.isSidebarOpen ? 'lg:ml-64' : 'lg:ml-20'"
            >
                <slot />
            </main>
        </div>
    </div>
</template>
