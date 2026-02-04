<script setup>
import StudentSidebar from './StudentSidebar.vue'
import { useUiStore } from '../../stores/ui'

const uiStore = useUiStore()
</script>

<template>
    <div class="min-h-screen bg-slate-50">
        <div class="flex">
            <StudentSidebar />
            <main 
                class="flex-1 transition-all duration-300 min-h-screen"
                :class="uiStore.isSidebarOpen ? 'lg:ml-64' : 'lg:ml-20'"
            >
                <slot />
            </main>
        </div>
    </div>
</template>
