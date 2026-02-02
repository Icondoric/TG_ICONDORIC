<script setup>
/**
 * DashboardLayout - Layout de dos columnas para dashboard
 * Sidebar izquierdo fijo (~280px) + Panel principal derecho (flex-1)
 * Responsive: sidebar colapsable en movil
 */
import { ref } from 'vue'

defineProps({
    sidebarTitle: {
        type: String,
        default: ''
    }
})

const isSidebarOpen = ref(false)

const toggleSidebar = () => {
    isSidebarOpen.value = !isSidebarOpen.value
}

const closeSidebar = () => {
    isSidebarOpen.value = false
}
</script>

<template>
    <div class="dashboard-bg min-h-screen pt-16">
        <!-- Mobile sidebar toggle -->
        <button
            @click="toggleSidebar"
            class="lg:hidden fixed bottom-4 right-4 z-40 p-3 bg-emi-navy-500 text-white rounded-full shadow-lg hover:bg-emi-navy-600 transition-colors"
        >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="!isSidebarOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
        </button>

        <!-- Overlay for mobile -->
        <div
            v-if="isSidebarOpen"
            @click="closeSidebar"
            class="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-30"
        ></div>

        <div class="flex">
            <!-- Sidebar -->
            <aside
                :class="[
                    'fixed lg:sticky top-16 left-0 z-40 w-[280px] h-[calc(100vh-4rem)] bg-white border-r border-gray-200 overflow-y-auto transition-transform duration-300 ease-in-out',
                    isSidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
                ]"
            >
                <div class="p-6">
                    <h2 v-if="sidebarTitle" class="text-lg font-semibold text-emi-navy-500 mb-6">
                        {{ sidebarTitle }}
                    </h2>
                    <slot name="sidebar"></slot>
                </div>
            </aside>

            <!-- Main Content -->
            <main class="flex-1 min-h-[calc(100vh-4rem)] lg:ml-0">
                <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    <slot></slot>
                </div>
            </main>
        </div>
    </div>
</template>
