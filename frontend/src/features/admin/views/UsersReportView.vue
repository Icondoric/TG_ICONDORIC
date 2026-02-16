<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/features/auth/store/auth.store'
import axios from 'axios'
import html2pdf from 'html2pdf.js'
import AppLayout from '@/shared/components/AppLayout.vue'

const router = useRouter()
const authStore = useAuthStore()
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const loading = ref(true)
const error = ref(null)
const generatingPdf = ref(false)

// Filters
const startDate = ref('')
const endDate = ref('')
const roleFilter = ref('')
const hasCvFilter = ref('')
const profileCompleteFilter = ref('')

// Data
const reportData = ref(null)

onMounted(async () => {
    if (!authStore.isAdminOrOperator) {
        router.push('/dashboard')
        return
    }
    // Default: last 90 days
    const end = new Date()
    const start = new Date()
    start.setDate(end.getDate() - 90)
    endDate.value = end.toISOString().split('T')[0]
    startDate.value = start.toISOString().split('T')[0]
    await loadData()
})

const loadData = async () => {
    loading.value = true
    error.value = null
    try {
        const headers = { Authorization: `Bearer ${authStore.token}` }
        const params = {
            start_date: startDate.value || undefined,
            end_date: endDate.value || undefined,
            role: roleFilter.value || undefined,
            has_cv: hasCvFilter.value !== '' ? hasCvFilter.value === 'true' : undefined,
            profile_complete: profileCompleteFilter.value !== '' ? profileCompleteFilter.value === 'true' : undefined
        }
        const res = await axios.get(`${API_URL}/api/analytics/users-report`, { headers, params })
        reportData.value = res.data
    } catch (err) {
        console.error('Error loading users report:', err)
        error.value = 'Error al cargar el reporte de usuarios.'
    } finally {
        loading.value = false
    }
}

const applyFilters = () => {
    loadData()
}

const generatePDF = async () => {
    generatingPdf.value = true
    const element = document.getElementById('users-report-container')
    const opt = {
        margin: [10, 10, 10, 10],
        filename: `reporte-usuarios-${startDate.value}_${endDate.value}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'landscape' },
        pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
    }
    try {
        await html2pdf().set(opt).from(element).save()
    } catch (err) {
        console.error('Error generating PDF:', err)
    } finally {
        generatingPdf.value = false
    }
}

const formatDate = (dateStr) => {
    if (!dateStr) return '-'
    return new Date(dateStr).toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>

<template>
    <AppLayout>
        <div class="max-w-7xl mx-auto py-8 px-4">
            <!-- Header -->
            <header class="mb-8">
                <router-link to="/admin/reports" class="text-blue-600 hover:text-blue-800 flex items-center mb-4">
                    <svg class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                    Volver a Reportes
                </router-link>
                <div class="flex flex-col xl:flex-row xl:items-end justify-between gap-4">
                    <div>
                        <h1 class="text-3xl font-bold text-slate-800">Reporte de Usuarios</h1>
                        <p class="mt-1 text-slate-600">Detalle de usuarios registrados en la plataforma.</p>
                    </div>
                    <button
                        @click="generatePDF"
                        :disabled="loading || generatingPdf"
                        class="h-[46px] px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium flex items-center gap-2 disabled:opacity-50 whitespace-nowrap self-start"
                    >
                        <svg v-if="!generatingPdf" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <div v-else class="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                        {{ generatingPdf ? 'PDF...' : 'Exportar PDF' }}
                    </button>
                </div>
            </header>

            <!-- Filters -->
            <div class="bg-white p-4 rounded-lg shadow-sm border border-slate-200 mb-6">
                <div class="grid grid-cols-1 md:grid-cols-5 gap-4 items-end">
                    <div>
                        <label class="block text-xs font-medium text-slate-500 mb-1">Desde</label>
                        <input type="date" v-model="startDate" class="w-full px-3 py-2 border border-slate-300 rounded-md text-sm" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-500 mb-1">Hasta</label>
                        <input type="date" v-model="endDate" class="w-full px-3 py-2 border border-slate-300 rounded-md text-sm" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-500 mb-1">Rol</label>
                        <select v-model="roleFilter" class="w-full px-3 py-2 border border-slate-300 rounded-md text-sm">
                            <option value="">Todos</option>
                            <option value="estudiante">Estudiante</option>
                            <option value="titulado">Titulado</option>
                            <option value="operador">Operador</option>
                            <option value="administrador">Administrador</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-500 mb-1">CV</label>
                        <select v-model="hasCvFilter" class="w-full px-3 py-2 border border-slate-300 rounded-md text-sm">
                            <option value="">Todos</option>
                            <option value="true">Con CV</option>
                            <option value="false">Sin CV</option>
                        </select>
                    </div>
                    <button @click="applyFilters" class="px-4 py-2 bg-slate-800 text-white rounded-md text-sm hover:bg-slate-700">
                        Filtrar
                    </button>
                </div>
            </div>

            <!-- Loading -->
            <div v-if="loading" class="bg-white rounded-xl shadow-md p-12 text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p class="mt-4 text-slate-500">Cargando reporte...</p>
            </div>

            <!-- Error -->
            <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                <p class="text-red-700">{{ error }}</p>
            </div>

            <!-- Report Content -->
            <div v-else id="users-report-container" class="space-y-6">
                <!-- Summary Cards -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-100">
                        <p class="text-sm font-medium text-slate-500 uppercase">Total Usuarios</p>
                        <p class="text-3xl font-bold text-slate-800 mt-1">{{ reportData?.stats.total }}</p>
                    </div>
                    <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-100">
                        <p class="text-sm font-medium text-slate-500 uppercase">Con CV</p>
                        <p class="text-3xl font-bold text-blue-600 mt-1">{{ reportData?.stats.with_cv }}</p>
                        <p class="text-xs text-slate-400 mt-1">{{ reportData?.stats.with_cv_pct }}%</p>
                    </div>
                    <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-100">
                        <p class="text-sm font-medium text-slate-500 uppercase">Perfil Completo</p>
                        <p class="text-3xl font-bold text-green-600 mt-1">{{ reportData?.stats.profile_complete }}</p>
                        <p class="text-xs text-slate-400 mt-1">{{ reportData?.stats.profile_complete_pct }}%</p>
                    </div>
                    <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-100">
                        <p class="text-sm font-medium text-slate-500 uppercase">Por Rol</p>
                        <div class="mt-1 text-sm space-y-1">
                            <div v-for="(count, rol) in reportData?.stats.by_role" :key="rol" class="flex justify-between">
                                <span class="capitalize">{{ rol }}</span>
                                <span class="font-bold">{{ count }}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Table -->
                <div class="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-slate-200">
                            <thead class="bg-slate-50">
                                <tr>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Nombre</th>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Email</th>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Rol</th>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Registro</th>
                                    <th class="px-4 py-3 text-center text-xs font-medium text-slate-500 uppercase">CV</th>
                                    <th class="px-4 py-3 text-center text-xs font-medium text-slate-500 uppercase">Perfil</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-100">
                                <tr v-for="user in reportData?.users" :key="user.id" class="hover:bg-slate-50">
                                    <td class="px-4 py-3 text-sm text-slate-800">{{ user.nombre_completo || '-' }}</td>
                                    <td class="px-4 py-3 text-sm text-slate-600">{{ user.email }}</td>
                                    <td class="px-4 py-3">
                                        <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium capitalize"
                                              :class="{
                                                  'bg-blue-100 text-blue-800': user.rol === 'estudiante',
                                                  'bg-purple-100 text-purple-800': user.rol === 'titulado',
                                                  'bg-yellow-100 text-yellow-800': user.rol === 'operador',
                                                  'bg-red-100 text-red-800': user.rol === 'administrador',
                                              }">
                                            {{ user.rol }}
                                        </span>
                                    </td>
                                    <td class="px-4 py-3 text-sm text-slate-600">{{ formatDate(user.fecha_registro) }}</td>
                                    <td class="px-4 py-3 text-center">
                                        <span v-if="user.tiene_cv" class="text-green-600">Si</span>
                                        <span v-else class="text-slate-400">No</span>
                                    </td>
                                    <td class="px-4 py-3 text-center">
                                        <span v-if="user.perfil_completo" class="text-green-600">Completo</span>
                                        <span v-else class="text-slate-400">{{ Math.round(user.completeness_score) }}%</span>
                                    </td>
                                </tr>
                                <tr v-if="!reportData?.users?.length">
                                    <td colspan="6" class="px-4 py-8 text-center text-slate-400">No se encontraron usuarios con los filtros seleccionados.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </AppLayout>
</template>
