import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUiStore = defineStore('ui', () => {
    const isSidebarOpen = ref(true)
    const isMobileSidebarOpen = ref(false)

    function toggleSidebar() {
        isSidebarOpen.value = !isSidebarOpen.value
    }

    function toggleMobileSidebar() {
        isMobileSidebarOpen.value = !isMobileSidebarOpen.value
    }

    function closeMobileSidebar() {
        isMobileSidebarOpen.value = false
    }

    return {
        isSidebarOpen,
        isMobileSidebarOpen,
        toggleSidebar,
        toggleMobileSidebar,
        closeMobileSidebar
    }
})
