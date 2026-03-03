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
const sectorFilter = ref('')

// Data
const reportData = ref(null)

onMounted(async () => {
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
            sector: sectorFilter.value || undefined
        }
        const res = await axios.get(`${API_URL}/api/analytics/profiles-report`, { headers, params })
        reportData.value = res.data
    } catch (err) {
        console.error('Error loading profiles report:', err)
        error.value = 'Error al cargar el reporte de perfiles.'
    } finally {
        loading.value = false
    }
}

const applyFilters = () => {
    loadData()
}

const generatePDF = async () => {
    generatingPdf.value = true
    const element = document.getElementById('profiles-report-container')
    const opt = {
        margin: [10, 10, 10, 10],
        filename: `reporte-perfiles-${startDate.value}_${endDate.value}.pdf`,
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
                        <h1 class="text-3xl font-bold text-slate-800">Reporte de Perfiles Institucionales</h1>
                        <p class="mt-1 text-slate-600">Detalle de perfiles institucionales registrados.</p>
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
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
                    <div>
                        <label class="block text-xs font-medium text-slate-500 mb-1">Desde</label>
                        <input type="date" v-model="startDate" class="w-full px-3 py-2 border border-slate-300 rounded-md text-sm" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-500 mb-1">Hasta</label>
                        <input type="date" v-model="endDate" class="w-full px-3 py-2 border border-slate-300 rounded-md text-sm" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-500 mb-1">Sector</label>
                        <input type="text" v-model="sectorFilter" placeholder="Filtrar por sector..." class="w-full px-3 py-2 border border-slate-300 rounded-md text-sm" />
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
            <div v-else id="profiles-report-container" class="space-y-6">
                <!-- Summary Cards -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-100">
                        <p class="text-sm font-medium text-slate-500 uppercase">Total Perfiles</p>
                        <p class="text-3xl font-bold text-slate-800 mt-1">{{ reportData?.stats.total }}</p>
                    </div>
                    <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-100">
                        <p class="text-sm font-medium text-slate-500 uppercase">Activos</p>
                        <p class="text-3xl font-bold text-green-600 mt-1">{{ reportData?.stats.activos }}</p>
                    </div>
                    <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-100">
                        <p class="text-sm font-medium text-slate-500 uppercase">Por Sector</p>
                        <div class="mt-1 text-sm space-y-1">
                            <div v-for="(count, sec) in reportData?.stats.by_sector" :key="sec" class="flex justify-between">
                                <span class="capitalize truncate mr-2">{{ sec }}</span>
                                <span class="font-bold">{{ count }}</span>
                            </div>
                            <p v-if="!Object.keys(reportData?.stats.by_sector || {}).length" class="text-slate-400">Sin datos</p>
                        </div>
                    </div>
                </div>

                <!-- Top Skills Required -->
                <div v-if="reportData?.stats.top_skills_required?.length" class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                    <h3 class="font-semibold text-slate-800 mb-4">Top Skills Requeridos</h3>
                    <div class="flex flex-wrap gap-2">
                        <span v-for="skill in reportData.stats.top_skills_required" :key="skill.name"
                              class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-50 text-blue-700 border border-blue-200">
                            {{ skill.name }}
                            <span class="ml-1 text-xs text-blue-500">({{ skill.count }})</span>
                        </span>
                    </div>
                </div>

                <!-- Table -->
                <div class="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-slate-200">
                            <thead class="bg-slate-50">
                                <tr>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Institucion</th>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Sector</th>
                                    <th class="px-4 py-3 text-center text-xs font-medium text-slate-500 uppercase">Estado</th>
                                    <th class="px-4 py-3 text-center text-xs font-medium text-slate-500 uppercase">Score Min</th>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Creado</th>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase">Actualizado</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-100">
                                <tr v-for="profile in reportData?.profiles" :key="profile.id" class="hover:bg-slate-50">
                                    <td class="px-4 py-3 text-sm text-slate-800 font-medium">{{ profile.institution_name || '-' }}</td>
                                    <td class="px-4 py-3 text-sm text-slate-600 capitalize">{{ profile.sector || '-' }}</td>
                                    <td class="px-4 py-3 text-center">
                                        <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
                                              :class="profile.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'">
                                            {{ profile.is_active ? 'Activo' : 'Inactivo' }}
                                        </span>
                                    </td>
                                    <td class="px-4 py-3 text-sm text-center text-slate-600">{{ profile.min_score ?? '-' }}</td>
                                    <td class="px-4 py-3 text-sm text-slate-600">{{ formatDate(profile.created_at) }}</td>
                                    <td class="px-4 py-3 text-sm text-slate-600">{{ formatDate(profile.updated_at) }}</td>
                                </tr>
                                <tr v-if="!reportData?.profiles?.length">
                                    <td colspan="6" class="px-4 py-8 text-center text-slate-400">No se encontraron perfiles con los filtros seleccionados.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </AppLayout>
</template>
