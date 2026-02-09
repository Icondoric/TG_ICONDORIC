<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/features/auth/store/auth.store'
import { useUiStore } from '@/shared/stores/ui'

const props = defineProps({
    menuItems: {
        type: Array,
        required: true
    },
    variant: {
        type: String,
        default: 'light',
        validator: (v) => ['light', 'dark'].includes(v)
    }
})

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUiStore()

const expandedItem = ref(null)

const isDark = props.variant === 'dark'

const isActive = (path) => route.path === path || route.path.startsWith(path + '/')

const isChildActive = (item) => {
    if (!item.children) return false
    return item.children.some(child => isActive(child.path))
}

const toggleSubmenu = (label) => {
    expandedItem.value = expandedItem.value === label ? null : label
}

const handleLogout = () => {
    authStore.logout()
    router.push('/login')
}

// Item styling helpers
const getItemClasses = (item) => {
    const active = item.path ? isActive(item.path) : isChildActive(item)
    return [
        'group flex items-center px-3 py-3 text-sm font-medium rounded-md transition-colors duration-150',
        active
            ? isDark
                ? 'bg-emi-navy-700 text-white'
                : 'bg-emi-navy-500 text-white'
            : isDark
                ? 'text-gray-300 hover:bg-emi-navy-700 hover:text-white'
                : 'text-gray-700 hover:bg-gray-100 hover:text-emi-navy-500',
        !uiStore.isSidebarOpen ? 'justify-center' : ''
    ]
}

const getIconClasses = (item) => {
    const active = item.path ? isActive(item.path) : isChildActive(item)
    return [
        'h-6 w-6 flex-shrink-0',
        active
            ? isDark ? 'text-white' : 'text-current'
            : isDark
                ? 'text-gray-400 group-hover:text-white'
                : 'text-gray-500 group-hover:text-emi-navy-500',
        uiStore.isSidebarOpen ? 'mr-3' : ''
    ]
}

const getChildClasses = (child) => {
    return [
        'flex items-center px-3 py-2 text-xs font-medium rounded-md transition-colors duration-150 ml-9',
        isActive(child.path)
            ? isDark
                ? 'bg-emi-navy-600 text-white'
                : 'bg-emi-navy-100 text-emi-navy-700'
            : isDark
                ? 'text-gray-400 hover:bg-emi-navy-700 hover:text-white'
                : 'text-gray-600 hover:bg-gray-100 hover:text-emi-navy-500'
    ]
}
</script>

<template>
    <!-- Desktop Sidebar -->
    <aside
        class="hidden lg:flex flex-col fixed inset-y-0 left-0 transition-all duration-300 transform z-50 shadow-lg"
        :class="[
            uiStore.isSidebarOpen ? 'w-64' : 'w-20',
            isDark
                ? 'bg-emi-navy-900 text-white'
                : 'bg-white border-r border-gray-200 text-gray-700 shadow-sm'
        ]"
    >
        <!-- Header -->
        <div
            class="flex items-center justify-between h-16 px-4"
            :class="isDark ? 'border-b border-emi-navy-700 bg-emi-navy-800' : 'border-b border-gray-200'"
        >
            <img
                v-if="uiStore.isSidebarOpen"
                src="@/shared/assets/icons/logoEmi.png"
                alt="Logo EMI"
                class="h-10 w-auto cursor-pointer hover:opacity-80 transition-opacity"
                @click="router.push('/')"
            />
            <button
                @click="uiStore.toggleSidebar"
                class="focus:outline-none ml-auto"
                :class="isDark ? 'text-white hover:text-gray-300' : 'text-gray-600 hover:text-emi-navy-500'"
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
                <template v-for="item in menuItems" :key="item.label">
                    <!-- Simple item (no children) -->
                    <router-link
                        v-if="!item.children"
                        :to="item.path"
                        :title="!uiStore.isSidebarOpen ? item.label : ''"
                        :class="getItemClasses(item)"
                    >
                        <svg :class="getIconClasses(item)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
                        </svg>
                        <span v-if="uiStore.isSidebarOpen" class="truncate">{{ item.label }}</span>
                    </router-link>

                    <!-- Item with submenu -->
                    <div v-else>
                        <button
                            @click="toggleSubmenu(item.label)"
                            :title="!uiStore.isSidebarOpen ? item.label : ''"
                            :class="getItemClasses(item)"
                            class="w-full"
                        >
                            <svg :class="getIconClasses(item)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
                            </svg>
                            <span v-if="uiStore.isSidebarOpen" class="truncate flex-1 text-left">{{ item.label }}</span>
                            <svg
                                v-if="uiStore.isSidebarOpen"
                                class="h-4 w-4 ml-auto transition-transform duration-200"
                                :class="expandedItem === item.label ? 'rotate-180' : ''"
                                fill="none" stroke="currentColor" viewBox="0 0 24 24"
                            >
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                            </svg>
                        </button>

                        <!-- Submenu children (expanded sidebar) -->
                        <div
                            v-if="uiStore.isSidebarOpen && expandedItem === item.label"
                            class="mt-1 space-y-1"
                        >
                            <router-link
                                v-for="child in item.children"
                                :key="child.path"
                                :to="child.path"
                                :class="getChildClasses(child)"
                            >
                                <span class="w-1.5 h-1.5 rounded-full mr-2 flex-shrink-0"
                                    :class="isActive(child.path)
                                        ? isDark ? 'bg-white' : 'bg-emi-navy-500'
                                        : isDark ? 'bg-gray-500' : 'bg-gray-400'"
                                ></span>
                                {{ child.label }}
                            </router-link>
                        </div>

                        <!-- Collapsed sidebar: show children as tooltip on hover -->
                        <div
                            v-if="!uiStore.isSidebarOpen && expandedItem === item.label"
                            class="absolute left-20 mt-[-48px] z-50 py-2 px-1 rounded-lg shadow-xl min-w-[160px]"
                            :class="isDark ? 'bg-emi-navy-800 border border-emi-navy-600' : 'bg-white border border-gray-200'"
                        >
                            <router-link
                                v-for="child in item.children"
                                :key="child.path"
                                :to="child.path"
                                @click="expandedItem = null"
                                :class="[
                                    'block px-3 py-2 text-xs font-medium rounded-md transition-colors',
                                    isActive(child.path)
                                        ? isDark ? 'bg-emi-navy-600 text-white' : 'bg-emi-navy-100 text-emi-navy-700'
                                        : isDark ? 'text-gray-300 hover:bg-emi-navy-700' : 'text-gray-600 hover:bg-gray-100'
                                ]"
                            >
                                {{ child.label }}
                            </router-link>
                        </div>
                    </div>
                </template>
            </nav>
        </div>

        <!-- Footer / Logout -->
        <div class="p-4" :class="isDark ? 'border-t border-emi-navy-700 bg-emi-navy-800' : 'border-t border-gray-200'">
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
            class="fixed inset-y-0 left-0 w-64 shadow-xl transform transition-transform duration-300"
            :class="isDark ? 'bg-emi-navy-900' : 'bg-white'"
            @click.stop
        >
            <!-- Mobile Header -->
            <div class="flex items-center justify-between h-16 px-4" :class="isDark ? 'border-b border-emi-navy-700' : 'border-b border-gray-200'">
                <img src="@/shared/assets/icons/logoEmi.png" alt="Logo EMI" class="h-10 w-auto" />
                <button
                    @click="uiStore.closeMobileSidebar"
                    :class="isDark ? 'text-white hover:text-gray-300' : 'text-gray-600 hover:text-emi-navy-500'"
                >
                    <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            <!-- Mobile Menu -->
            <div class="py-4 overflow-y-auto" style="max-height: calc(100vh - 128px)">
                <nav class="space-y-1 px-2">
                    <template v-for="item in menuItems" :key="item.label">
                        <!-- Simple item -->
                        <router-link
                            v-if="!item.children"
                            :to="item.path"
                            @click="uiStore.closeMobileSidebar"
                            :class="[
                                'group flex items-center px-3 py-3 text-sm font-medium rounded-md transition-colors',
                                isActive(item.path)
                                    ? isDark ? 'bg-emi-navy-700 text-white' : 'bg-emi-navy-500 text-white'
                                    : isDark ? 'text-gray-300 hover:bg-emi-navy-700' : 'text-gray-700 hover:bg-gray-100'
                            ]"
                        >
                            <svg class="h-6 w-6 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
                            </svg>
                            <span>{{ item.label }}</span>
                        </router-link>

                        <!-- Item with submenu (mobile) -->
                        <div v-else>
                            <button
                                @click="toggleSubmenu(item.label)"
                                :class="[
                                    'w-full group flex items-center px-3 py-3 text-sm font-medium rounded-md transition-colors',
                                    isChildActive(item)
                                        ? isDark ? 'bg-emi-navy-700 text-white' : 'bg-emi-navy-500 text-white'
                                        : isDark ? 'text-gray-300 hover:bg-emi-navy-700' : 'text-gray-700 hover:bg-gray-100'
                                ]"
                            >
                                <svg class="h-6 w-6 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
                                </svg>
                                <span class="flex-1 text-left">{{ item.label }}</span>
                                <svg
                                    class="h-4 w-4 ml-auto transition-transform duration-200"
                                    :class="expandedItem === item.label ? 'rotate-180' : ''"
                                    fill="none" stroke="currentColor" viewBox="0 0 24 24"
                                >
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                                </svg>
                            </button>

                            <div v-if="expandedItem === item.label" class="mt-1 space-y-1">
                                <router-link
                                    v-for="child in item.children"
                                    :key="child.path"
                                    :to="child.path"
                                    @click="uiStore.closeMobileSidebar"
                                    :class="getChildClasses(child)"
                                >
                                    <span class="w-1.5 h-1.5 rounded-full mr-2 flex-shrink-0"
                                        :class="isActive(child.path)
                                            ? isDark ? 'bg-white' : 'bg-emi-navy-500'
                                            : isDark ? 'bg-gray-500' : 'bg-gray-400'"
                                    ></span>
                                    {{ child.label }}
                                </router-link>
                            </div>
                        </div>
                    </template>
                </nav>
            </div>

            <!-- Mobile Logout -->
            <div class="absolute bottom-0 left-0 right-0 p-4" :class="isDark ? 'border-t border-emi-navy-700' : 'border-t border-gray-200'">
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
        class="lg:hidden fixed bottom-4 right-4 z-40 p-3 text-white rounded-full shadow-lg transition-colors"
        :class="isDark ? 'bg-emi-navy-700 hover:bg-emi-navy-800' : 'bg-emi-navy-500 hover:bg-emi-navy-600'"
    >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
    </button>
</template>
