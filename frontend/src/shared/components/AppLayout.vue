<script setup>
import AppSidebar from './AppSidebar.vue'
import { useUiStore } from '@/shared/stores/ui'

defineProps({
    menuItems: {
        type: Array,
        required: true
    },
    variant: {
        type: String,
        default: 'light'
    }
})

const uiStore = useUiStore()
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
