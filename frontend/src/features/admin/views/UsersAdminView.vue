<script setup>
/**
 * UsersAdminView - Fase 7+
 * Vista para listar y gestionar usuarios (Estudiantes, Titulados, Admins)
 */
import { ref, onMounted, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUsersStore } from '@/features/admin/store/users.store'
import { useAuthStore } from '@/features/auth/store/auth.store'
import AppLayout from '@/shared/components/AppLayout.vue'

const router = useRouter()
const usersStore = useUsersStore()
const authStore = useAuthStore()

// State
const currentPage = ref(1)
const search = ref('')
const roleFilter = ref('')
const debounceTimeout = ref(null)

// Constants
const ROLES = [
    { value: 'estudiante', label: 'Estudiante' },
    { value: 'titulado', label: 'Titulado' },
    { value: 'operador', label: 'Operador' },
    { value: 'administrador', label: 'Administrador' }
]

onMounted(async () => {
    if (!authStore.isAdminOrOperator) {
        router.push('/dashboard')
        return
    }
    await loadUsers()
})

// Methods
const loadUsers = async () => {
    await usersStore.loadUsers({
        page: currentPage.value,
        role: roleFilter.value || null,
        search: search.value || null
    })
}

const onSearch = () => {
    if (debounceTimeout.value) clearTimeout(debounceTimeout.value)

    debounceTimeout.value = setTimeout(() => {
        currentPage.value = 1
        loadUsers()
    }, 500)
}

const onFilterChange = () => {
    currentPage.value = 1
    loadUsers()
}

const changePage = (page) => {
    if (page < 1 || page > totalPages.value) return
    currentPage.value = page
    loadUsers()
}

const viewUser = (userId) => {
    router.push(`/admin/users/${userId}`)
}

const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    return new Date(dateString).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

// PDF Generation
import html2pdf from 'html2pdf.js'

const generateReport = () => {
    const element = document.getElementById('users-report-content')
    const opt = {
        margin: 10,
        filename: 'reporte-usuarios-emi.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'landscape' }
    }
    html2pdf().set(opt).from(element).save()
}

// Computed helper for total pages (simple approximation based on Store total)
// Assuming page size is 20 as per store default
const totalPages = computed(() => Math.ceil(usersStore.totalUsers / 20))

</script>

<template>
    <AppLayout>
        <div class="max-w-7xl mx-auto py-8 px-4">
            <!-- Header -->
            <header class="mb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                    <h1 class="text-3xl font-bold text-slate-800">Gestion de Usuarios</h1>
                    <p class="mt-1 text-slate-600">
                        Administra las cuentas de estudiantes, titulados y administradores.
                    </p>
                </div>
                <button
                    @click="generateReport"
                    class="flex items-center px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors shadow-sm"
                >
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Generar Reporte
                </button>
            </header>

            <!-- Filters -->
            <div class="bg-white rounded-xl shadow-md p-4 mb-6">
                <div class="flex flex-col md:flex-row gap-4">
                    <!-- Search -->
                    <div class="flex-1">
                        <div class="relative">
                            <span class="absolute inset-y-0 left-0 flex items-center pl-3">
                                <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                </svg>
                            </span>
                            <input
                                v-model="search"
                                @input="onSearch"
                                type="text"
                                placeholder="Buscar por nombre o email..."
                                class="w-full pl-10 px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            />
                        </div>
                    </div>

                    <!-- Role Filter -->
                    <div class="w-full md:w-64">
                        <select
                            v-model="roleFilter"
                            @change="onFilterChange"
                            class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                            <option value="">Todos los roles</option>
                            <option v-for="role in ROLES" :key="role.value" :value="role.value">
                                {{ role.label }}
                            </option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Loading -->
            <div v-if="usersStore.loading" class="bg-white rounded-xl shadow-md p-12 text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p class="mt-4 text-slate-500">Cargando usuarios...</p>
            </div>

            <!-- Error -->
            <div v-else-if="usersStore.error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                <p class="text-red-700">{{ usersStore.error }}</p>
            </div>

            <!-- Users Table -->
            <div v-else id="users-report-content" class="bg-white rounded-xl shadow-md overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-50 border-b border-slate-200">
                                <th class="px-6 py-4 font-semibold text-slate-700 text-sm">Usuario</th>
                                <th class="px-6 py-4 font-semibold text-slate-700 text-sm">Rol</th>
                                <th class="px-6 py-4 font-semibold text-slate-700 text-sm">Estado Perfil</th>
                                <th class="px-6 py-4 font-semibold text-slate-700 text-sm">Fecha Registro</th>
                                <th class="px-6 py-4 font-semibold text-slate-700 text-sm text-right">Acciones</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            <tr v-if="usersStore.users.length === 0">
                                <td colspan="5" class="px-6 py-8 text-center text-slate-500">
                                    No se encontraron usuarios con los filtros seleccionados.
                                </td>
                            </tr>
                            <tr v-for="user in usersStore.users" :key="user.id" class="hover:bg-slate-50 transition-colors">
                                <td class="px-6 py-4">
                                    <div>
                                        <p class="font-medium text-slate-800">{{ user.nombre_completo || 'Sin nombre' }}</p>
                                        <p class="text-sm text-slate-500">{{ user.email }}</p>
                                    </div>
                                </td>
                                <td class="px-6 py-4">
                                    <span :class="[
                                        'px-2.5 py-1 rounded-full text-xs font-medium capitalize',
                                        user.rol === 'administrador' ? 'bg-purple-100 text-purple-700' :
                                        user.rol === 'operador' ? 'bg-orange-100 text-orange-700' :
                                        user.rol === 'titulado' ? 'bg-indigo-100 text-indigo-700' :
                                        'bg-blue-100 text-blue-700'
                                    ]">
                                        {{ user.rol }}
                                    </span>
                                </td>
                                <td class="px-6 py-4">
                                    <template v-if="user.rol !== 'administrador'">
                                        <div v-if="user.tiene_perfil" class="flex items-center gap-2">
                                             <div class="w-16 bg-slate-200 rounded-full h-2 overflow-hidden">
                                                <div
                                                    class="h-full rounded-full"
                                                    :class="user.perfil_completo ? 'bg-green-500' : 'bg-yellow-500'"
                                                    :style="{ width: `${user.completeness_score * 100}%` }"
                                                ></div>
                                            </div>
                                            <span class="text-xs text-slate-600">
                                                {{ Math.round(user.completeness_score * 100) }}%
                                            </span>
                                        </div>
                                        <span v-else class="text-xs text-slate-400 italic">
                                            Sin perfil
                                        </span>
                                    </template>
                                    <span v-else class="text-xs text-slate-400">-</span>
                                </td>
                                <td class="px-6 py-4 text-sm text-slate-600">
                                    {{ formatDate(user.created_at) }}
                                </td>
                                <td class="px-6 py-4 text-right">
                                    <button
                                        @click="viewUser(user.id)"
                                        class="text-blue-600 hover:text-blue-800 font-medium text-sm"
                                    >
                                        Ver Detalle
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Pagination -->
                <div class="px-6 py-4 border-t border-slate-200 flex items-center justify-between">
                    <div class="text-sm text-slate-500">
                        Mostrando usuarios {{ (currentPage - 1) * 20 + 1 }} - {{ Math.min(currentPage * 20, usersStore.totalUsers) }} de {{ usersStore.totalUsers }}
                    </div>
                    <div class="flex gap-2">
                        <button
                            @click="changePage(currentPage - 1)"
                            :disabled="currentPage === 1"
                            class="px-3 py-1 border border-slate-300 rounded hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            Anterior
                        </button>
                        <button
                             @click="changePage(currentPage + 1)"
                             :disabled="currentPage >= totalPages"
                             class="px-3 py-1 border border-slate-300 rounded hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            Siguiente
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </AppLayout>
</template>
