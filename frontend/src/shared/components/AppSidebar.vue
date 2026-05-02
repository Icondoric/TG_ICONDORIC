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
const hoveredItem = ref(null)
const hoveredItemObj = ref(null)
const hoveredRect = ref(null)
let hideTimer = null

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

// Tooltip handlers — usamos getBoundingClientRect() para posicionamiento fixed
// que escapa del overflow-y:auto del contenedor de nav
const onNavItemEnter = (item, event) => {
    clearTimeout(hideTimer)
    hoveredItem.value = item.label
    hoveredItemObj.value = item
    hoveredRect.value = event.currentTarget.getBoundingClientRect()
}

const onNavItemLeave = () => {
    // Pequeño delay para que el mouse pueda llegar al popover de hijos sin que desaparezca
    hideTimer = setTimeout(() => {
        hoveredItem.value = null
        hoveredItemObj.value = null
        hoveredRect.value = null
    }, 80)
}

const onPopoverEnter = () => clearTimeout(hideTimer)

const onPopoverLeave = () => {
    hoveredItem.value = null
    hoveredItemObj.value = null
    hoveredRect.value = null
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
        'h-6 w-6 flex-shrink-0 transition-transform duration-150 group-hover:scale-110',
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
                : 'bg-gradient-to-b from-white via-white to-slate-50 border-r border-gray-200 text-gray-700 shadow-sm'
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
                class="h-11 w-auto cursor-pointer hover:opacity-80 transition-opacity"
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
            <!-- Bienvenida usuario -->
            <div
                v-if="uiStore.isSidebarOpen && authStore.user"
                class="mx-3 mb-3 pl-3 border-l-2 border-emi-gold-500"
            >
                <p class="text-xs font-medium mb-0.5"
                   :class="isDark ? 'text-gray-400' : 'text-gray-500'"
                >
                    Bienvenido
                </p>
                <p class="text-sm font-semibold leading-tight truncate"
                   :class="isDark ? 'text-white' : 'text-emi-navy-700'"
                >
                    {{ authStore.user.nombre_completo }}
                </p>
                <p class="text-xs font-medium leading-tight truncate mt-0.5"
                   :class="isDark ? 'text-emi-gold-400' : 'text-emi-gold-600'"
                >
                    {{ authStore.user.rol?.charAt(0).toUpperCase() + authStore.user.rol?.slice(1) }}
                </p>
            </div>

            <nav class="space-y-1 px-2">
                <template v-for="item in menuItems" :key="item.label">
                    <!-- Simple item (no children) -->
                    <div
                        v-if="!item.children"
                        class="relative"
                        @mouseenter="onNavItemEnter(item, $event)"
                        @mouseleave="onNavItemLeave"
                    >
                        <!-- Barra activa izquierda -->
                        <span
                            v-if="isActive(item.path)"
                            class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-7 rounded-r-full bg-emi-gold-500 z-10"
                        ></span>
                        <router-link :to="item.path" :class="getItemClasses(item)">
                            <svg :class="getIconClasses(item)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
                            </svg>
                            <span v-if="uiStore.isSidebarOpen" class="leading-tight">{{ item.label }}</span>
                        </router-link>
                    </div>

                    <!-- Item with submenu -->
                    <div
                        v-else
                        class="relative"
                        @mouseenter="onNavItemEnter(item, $event)"
                        @mouseleave="onNavItemLeave"
                    >
                        <!-- Barra activa izquierda -->
                        <span
                            v-if="isChildActive(item)"
                            class="absolute left-0 top-3.5 w-1 h-7 rounded-r-full bg-emi-gold-500 z-10"
                        ></span>
                        <button @click="toggleSubmenu(item.label)" :class="getItemClasses(item)" class="w-full">
                            <svg :class="getIconClasses(item)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="item.icon" />
                            </svg>
                            <span v-if="uiStore.isSidebarOpen" class="flex-1 text-left leading-tight">{{ item.label }}</span>
                            <svg
                                v-if="uiStore.isSidebarOpen"
                                class="h-4 w-4 ml-auto transition-transform duration-200"
                                :class="expandedItem === item.label ? 'rotate-180' : ''"
                                fill="none" stroke="currentColor" viewBox="0 0 24 24"
                            >
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                            </svg>
                        </button>

                        <!-- Submenu children (sidebar expandido) -->
                        <transition name="submenu">
                            <div
                                v-if="uiStore.isSidebarOpen && expandedItem === item.label"
                                class="mt-1 space-y-1 overflow-hidden"
                            >
                                <router-link
                                    v-for="child in item.children"
                                    :key="child.path"
                                    :to="child.path"
                                    :class="getChildClasses(child)"
                                >
                                    <span class="w-1.5 h-1.5 rounded-full mr-2 flex-shrink-0"
                                        :class="isActive(child.path)
                                            ? isDark ? 'bg-white' : 'bg-emi-gold-500'
                                            : isDark ? 'bg-gray-500' : 'bg-gray-400'"
                                    ></span>
                                    {{ child.label }}
                                </router-link>
                            </div>
                        </transition>
                    </div>
                </template>
            </nav>
        </div>

        <!-- Footer: Mi Cuenta + Logout -->
        <div :class="isDark ? 'border-t border-emi-navy-700 bg-emi-navy-800' : 'border-t border-gray-200'">
            <!-- Mi Cuenta Section -->
            <div class="px-2 pt-3 pb-2">
                <div
                    class="relative"
                    @mouseenter="onNavItemEnter({ label: 'Mi Cuenta', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z', children: [{ label: 'Ver Mi Cuenta', path: '/ver-mi-cuenta' }, { label: 'Configurar Mi Cuenta', path: '/configurar-cuenta' }] }, $event)"
                    @mouseleave="onNavItemLeave"
                >
                    <button
                        @click="toggleSubmenu('Mi Cuenta')"
                        :class="[
                            'group flex items-center px-3 py-3 text-sm font-medium rounded-md transition-colors duration-150 w-full',
                            isActive('/ver-mi-cuenta') || isActive('/configurar-cuenta')
                                ? isDark ? 'bg-emi-navy-700 text-white' : 'bg-emi-navy-500 text-white'
                                : isDark ? 'text-gray-300 hover:bg-emi-navy-700 hover:text-white' : 'text-gray-700 hover:bg-gray-100 hover:text-emi-navy-500',
                            !uiStore.isSidebarOpen ? 'justify-center' : ''
                        ]"
                    >
                        <svg
                            :class="[
                                'h-6 w-6 flex-shrink-0 transition-transform duration-150 group-hover:scale-110',
                                isActive('/ver-mi-cuenta') || isActive('/configurar-cuenta')
                                    ? isDark ? 'text-white' : 'text-current'
                                    : isDark ? 'text-gray-400 group-hover:text-white' : 'text-gray-500 group-hover:text-emi-navy-500',
                                uiStore.isSidebarOpen ? 'mr-3' : ''
                            ]"
                            fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        <span v-if="uiStore.isSidebarOpen" class="flex-1 text-left leading-tight">Mi Cuenta</span>
                        <svg
                            v-if="uiStore.isSidebarOpen"
                            class="h-4 w-4 ml-auto transition-transform duration-200"
                            :class="expandedItem === 'Mi Cuenta' ? 'rotate-180' : ''"
                            fill="none" stroke="currentColor" viewBox="0 0 24 24"
                        >
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                        </svg>
                    </button>

                    <!-- Submenu children (sidebar expandido) -->
                    <transition name="submenu">
                        <div
                            v-if="uiStore.isSidebarOpen && expandedItem === 'Mi Cuenta'"
                            class="mt-1 space-y-1 overflow-hidden"
                        >
                            <router-link
                                to="/ver-mi-cuenta"
                                :class="getChildClasses({ path: '/ver-mi-cuenta' })"
                            >
                                <span class="w-1.5 h-1.5 rounded-full mr-2 flex-shrink-0"
                                    :class="isActive('/ver-mi-cuenta')
                                        ? isDark ? 'bg-white' : 'bg-emi-gold-500'
                                        : isDark ? 'bg-gray-500' : 'bg-gray-400'"
                                ></span>
                                Ver Mi Cuenta
                            </router-link>
                            <router-link
                                to="/configurar-cuenta"
                                :class="getChildClasses({ path: '/configurar-cuenta' })"
                            >
                                <span class="w-1.5 h-1.5 rounded-full mr-2 flex-shrink-0"
                                    :class="isActive('/configurar-cuenta')
                                        ? isDark ? 'bg-white' : 'bg-emi-gold-500'
                                        : isDark ? 'bg-gray-500' : 'bg-gray-400'"
                                ></span>
                                Configurar Mi Cuenta
                            </router-link>
                        </div>
                    </transition>
                </div>
            </div>

            <!-- Logout -->
            <div class="px-4 pb-4 pt-2">
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
        </div>
    </aside>

    <!--
        Tooltips/popovers renderizados en <body> via Teleport.
        Razón: el nav está dentro de overflow-y:auto que, por spec CSS, también clipa
        el overflow-x, ocultando cualquier tooltip posicionado absolutamente fuera
        del sidebar. Con position:fixed + getBoundingClientRect() escapamos el clipping.
    -->

    <!-- Tooltip: item simple (solo icono, sidebar colapsado) -->
    <Teleport to="body">
        <transition name="tooltip-global">
            <div
                v-if="!uiStore.isSidebarOpen && hoveredItem && !hoveredItemObj?.children && hoveredRect"
                class="fixed z-[200] px-3 py-2 text-xs font-medium rounded-md shadow-lg whitespace-nowrap pointer-events-none"
                :class="isDark ? 'bg-emi-navy-700 text-white' : 'bg-gray-800 text-white'"
                :style="{
                    left: hoveredRect.right + 12 + 'px',
                    top: (hoveredRect.top + hoveredRect.height / 2) + 'px',
                    transform: 'translateY(-50%)'
                }"
            >
                {{ hoveredItem }}
                <div
                    class="absolute right-full top-1/2 -translate-y-1/2 w-0 h-0 border-t-4 border-b-4 border-r-4 border-transparent"
                    :class="isDark ? 'border-r-emi-navy-700' : 'border-r-gray-800'"
                ></div>
            </div>
        </transition>
    </Teleport>

    <!-- Popover: item con hijos (sidebar colapsado) — muestra label + lista de hijos -->
    <Teleport to="body">
        <transition name="tooltip-global">
            <div
                v-if="!uiStore.isSidebarOpen && hoveredItem && hoveredItemObj?.children && hoveredRect"
                class="fixed z-[200] py-2 px-1 rounded-lg shadow-xl min-w-[180px]"
                :class="isDark ? 'bg-emi-navy-800 border border-emi-navy-600' : 'bg-white border border-gray-200 shadow-lg'"
                :style="{
                    left: hoveredRect.right + 12 + 'px',
                    top: hoveredRect.top + 'px'
                }"
                @mouseenter="onPopoverEnter"
                @mouseleave="onPopoverLeave"
            >
                <div class="px-3 py-1.5 text-xs font-semibold uppercase tracking-wide mb-1 text-gray-400">
                    {{ hoveredItem }}
                </div>
                <router-link
                    v-for="child in hoveredItemObj.children"
                    :key="child.path"
                    :to="child.path"
                    @click="hoveredItem = null"
                    :class="[
                        'block px-3 py-2 text-xs font-medium rounded-md transition-colors',
                        isActive(child.path)
                            ? isDark ? 'bg-emi-navy-600 text-white' : 'bg-emi-navy-100 text-emi-navy-700'
                            : isDark ? 'text-gray-300 hover:bg-emi-navy-700' : 'text-gray-600 hover:bg-gray-100'
                    ]"
                >
                    {{ child.label }}
                </router-link>
                <!-- Arrow -->
                <div
                    class="absolute right-full top-4 w-0 h-0 border-t-[6px] border-b-[6px] border-r-[6px] border-transparent"
                    :class="isDark ? 'border-r-emi-navy-800' : 'border-r-white'"
                ></div>
            </div>
        </transition>
    </Teleport>

    <!-- Mobile Sidebar -->
    <div
        v-if="uiStore.isMobileSidebarOpen"
        class="lg:hidden fixed inset-0 z-50 bg-gray-900 bg-opacity-50"
        @click="uiStore.closeMobileSidebar"
    >
        <aside
            class="fixed inset-y-0 left-0 w-64 shadow-xl transform transition-transform duration-300 flex flex-col"
            :class="isDark ? 'bg-emi-navy-900' : 'bg-white'"
            @click.stop
        >
            <!-- Mobile Header -->
            <div class="flex-shrink-0 flex items-center justify-between h-16 px-4" :class="isDark ? 'border-b border-emi-navy-700' : 'border-b border-gray-200'">
                <img src="@/shared/assets/icons/logoEmi.png" alt="Logo EMI" class="h-11 w-auto" />
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
            <div class="flex-1 overflow-y-auto py-4">
                <!-- Bienvenida usuario mobile -->
                <div
                    v-if="authStore.user"
                    class="mx-3 mb-3 pl-3 border-l-2 border-emi-gold-500"
                >
                    <p class="text-xs font-medium mb-0.5"
                       :class="isDark ? 'text-gray-400' : 'text-gray-500'"
                    >
                        Bienvenido
                    </p>
                    <p class="text-sm font-semibold leading-tight truncate"
                       :class="isDark ? 'text-white' : 'text-emi-navy-700'"
                    >
                        {{ authStore.user.nombre_completo }}
                    </p>
                    <p class="text-xs font-medium leading-tight truncate mt-0.5"
                       :class="isDark ? 'text-emi-gold-400' : 'text-emi-gold-600'"
                    >
                        {{ authStore.user.rol?.charAt(0).toUpperCase() + authStore.user.rol?.slice(1) }}
                    </p>
                </div>

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
                            <svg class="h-6 w-6 mr-3 flex-shrink-0 transition-transform duration-150 group-hover:scale-110" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
                                <svg class="h-6 w-6 mr-3 flex-shrink-0 transition-transform duration-150 group-hover:scale-110" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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

                            <!-- Submenu animation mobile -->
                            <transition name="submenu">
                                <div v-if="expandedItem === item.label" class="mt-1 space-y-1 overflow-hidden">
                                    <router-link
                                        v-for="child in item.children"
                                        :key="child.path"
                                        :to="child.path"
                                        @click="uiStore.closeMobileSidebar"
                                        :class="getChildClasses(child)"
                                    >
                                        <span class="w-1.5 h-1.5 rounded-full mr-2 flex-shrink-0"
                                            :class="isActive(child.path)
                                                ? isDark ? 'bg-white' : 'bg-emi-gold-500'
                                                : isDark ? 'bg-gray-500' : 'bg-gray-400'"
                                        ></span>
                                        {{ child.label }}
                                    </router-link>
                                </div>
                            </transition>
                        </div>
                    </template>
                </nav>
            </div>

            <!-- Mobile Footer: Mi Cuenta + Logout -->
            <div class="flex-shrink-0" :class="isDark ? 'border-t border-emi-navy-700' : 'border-t border-gray-200'">
                <!-- Mi Cuenta Section (mobile) -->
                <div class="px-2 pt-3 pb-2">
                    <div>
                        <button
                            @click="toggleSubmenu('Mi Cuenta')"
                            :class="[
                                'w-full group flex items-center px-3 py-3 text-sm font-medium rounded-md transition-colors',
                                isActive('/ver-mi-cuenta') || isActive('/configurar-cuenta')
                                    ? isDark ? 'bg-emi-navy-700 text-white' : 'bg-emi-navy-500 text-white'
                                    : isDark ? 'text-gray-300 hover:bg-emi-navy-700' : 'text-gray-700 hover:bg-gray-100'
                            ]"
                        >
                            <svg class="h-6 w-6 mr-3 flex-shrink-0 transition-transform duration-150 group-hover:scale-110" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                            <span class="flex-1 text-left">Mi Cuenta</span>
                            <svg
                                class="h-4 w-4 ml-auto transition-transform duration-200"
                                :class="expandedItem === 'Mi Cuenta' ? 'rotate-180' : ''"
                                fill="none" stroke="currentColor" viewBox="0 0 24 24"
                            >
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                            </svg>
                        </button>

                        <transition name="submenu">
                            <div v-if="expandedItem === 'Mi Cuenta'" class="mt-1 space-y-1 overflow-hidden">
                                <router-link
                                    to="/ver-mi-cuenta"
                                    @click="uiStore.closeMobileSidebar"
                                    :class="getChildClasses({ path: '/ver-mi-cuenta' })"
                                >
                                    <span class="w-1.5 h-1.5 rounded-full mr-2 flex-shrink-0"
                                        :class="isActive('/ver-mi-cuenta')
                                            ? isDark ? 'bg-white' : 'bg-emi-gold-500'
                                            : isDark ? 'bg-gray-500' : 'bg-gray-400'"
                                    ></span>
                                    Ver Mi Cuenta
                                </router-link>
                                <router-link
                                    to="/configurar-cuenta"
                                    @click="uiStore.closeMobileSidebar"
                                    :class="getChildClasses({ path: '/configurar-cuenta' })"
                                >
                                    <span class="w-1.5 h-1.5 rounded-full mr-2 flex-shrink-0"
                                        :class="isActive('/configurar-cuenta')
                                            ? isDark ? 'bg-white' : 'bg-emi-gold-500'
                                            : isDark ? 'bg-gray-500' : 'bg-gray-400'"
                                    ></span>
                                    Configurar Mi Cuenta
                                </router-link>
                            </div>
                        </transition>
                    </div>
                </div>

                <!-- Logout -->
                <div class="px-4 pb-4 pt-2">
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

<!-- Global: necesario para elementos teleportados a <body> (fuera del scope del componente) -->
<style>
.tooltip-global-enter-active {
    transition: opacity 0.15s ease, transform 0.15s ease;
}
.tooltip-global-leave-active {
    transition: opacity 0.1s ease, transform 0.1s ease;
}
.tooltip-global-enter-from {
    opacity: 0;
    transform: translateX(-4px) translateY(-50%);
}
.tooltip-global-leave-to {
    opacity: 0;
    transform: translateX(-4px) translateY(-50%);
}
</style>

<style scoped>
/* Submenu slide animation */
.submenu-enter-active {
    transition: max-height 0.25s ease-out, opacity 0.2s ease-out;
    max-height: 500px;
}
.submenu-leave-active {
    transition: max-height 0.2s ease-in, opacity 0.15s ease-in;
    max-height: 500px;
}
.submenu-enter-from {
    max-height: 0;
    opacity: 0;
}
.submenu-leave-to {
    max-height: 0;
    opacity: 0;
}
</style>
