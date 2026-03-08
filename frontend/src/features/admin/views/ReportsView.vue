<script setup>
/**
 * ReportsView - Fase 7+
 * Vista de analitica y reportes con exportacion a PDF y filtros de fecha
 */
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/features/auth/store/auth.store'
import axios from 'axios'
import html2pdf from 'html2pdf.js'
import AppLayout from '@/shared/components/AppLayout.vue'

// Charts
import UserDistributionChart from '../components/charts/UserDistributionChart.vue'
import UserGrowthChart from '../components/charts/UserGrowthChart.vue'
import SkillsBarChart from '../components/charts/SkillsBarChart.vue'

const authStore = useAuthStore()
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// State
const loading = ref(true)
const error = ref(null)
const generatingPdf = ref(false)

// Date Filters
const dateRange = ref('last_30_days')
const customStartDate = ref('')
const customEndDate = ref('')

const usersSummary = ref(null)
const userGrowth = ref(null)
const skillsCloud = ref(null)
const profileStats = ref(null)

onMounted(async () => {
    updateCustomDatesFromRange()
    await loadData()
})

const updateCustomDatesFromRange = () => {
    const end = new Date()
    const start = new Date()

    if (dateRange.value === 'last_30_days') {
        start.setDate(end.getDate() - 30)
    } else if (dateRange.value === 'this_year') {
        start.setMonth(0, 1)
    } else {
        return
    }

    customEndDate.value = end.toISOString().split('T')[0]
    customStartDate.value = start.toISOString().split('T')[0]
}

const onRangeChange = () => {
    if (dateRange.value !== 'custom') {
        updateCustomDatesFromRange()
        loadData()
    }
}

const onCustomDateChange = () => {
    if (dateRange.value === 'custom' && customStartDate.value && customEndDate.value) {
        loadData()
    }
}

const loadData = async () => {
    loading.value = true
    error.value = null
    try {
        const headers = { Authorization: `Bearer ${authStore.token}` }
        const params = {
            start_date: customStartDate.value,
            end_date: customEndDate.value
        }

        const [summaryRes, growthRes, skillsRes, statsRes] = await Promise.all([
            axios.get(`${API_URL}/api/analytics/users-summary`, { headers, params }),
            axios.get(`${API_URL}/api/analytics/user-growth`, { headers, params }),
            axios.get(`${API_URL}/api/analytics/skills-cloud`, { headers, params }),
            axios.get(`${API_URL}/api/analytics/profile-completion`, { headers, params })
        ])

        usersSummary.value = summaryRes.data
        userGrowth.value = growthRes.data
        skillsCloud.value = skillsRes.data
        profileStats.value = statsRes.data

    } catch (err) {
        console.error('Error loading reports:', err)
        error.value = 'Error al cargar los datos del reporte.'
    } finally {
        loading.value = false
    }
}

const generatePDF = async () => {
    generatingPdf.value = true
    const element = document.getElementById('report-container')

    const dateDisplay = document.getElementById('pdf-date-range')
    if (dateDisplay) dateDisplay.style.display = 'block'

    const opt = {
        margin: [10, 10, 10, 10],
        filename: `reporte-${customStartDate.value}_${customEndDate.value}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
        pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
    }

    try {
        await html2pdf().set(opt).from(element).save()
    } catch (err) {
        console.error('Error generating PDF:', err)
        alert('Hubo un error al generar el PDF.')
    } finally {
        if (dateDisplay) dateDisplay.style.display = 'none'
        generatingPdf.value = false
    }
}

const formatDate = (dateStr) => {
    if (!dateStr) return ''
    return new Date(dateStr).toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>

<template>
    <AppLayout>
        <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">

            <!-- Header & Filters -->
            <header class="mb-8">
                <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-5">
                    <div>
                        <h1 class="text-3xl font-bold text-emi-navy-500">Reportes y Analítica</h1>
                        <p class="mt-1 text-gray-600">
                            Visión general del estado de la plataforma y el talento.
                        </p>
                    </div>

                    <button
                        @click="generatePDF"
                        :disabled="loading || generatingPdf"
                        class="h-10 px-5 bg-emi-navy-600 text-white rounded-lg hover:bg-emi-navy-700 transition-colors text-sm font-medium inline-flex items-center gap-2 disabled:opacity-50 whitespace-nowrap self-start sm:self-auto"
                    >
                        <svg v-if="!generatingPdf" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <div v-else class="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                        {{ generatingPdf ? 'Generando PDF...' : 'Descargar PDF' }}
                    </button>
                </div>

                <!-- Filters -->
                <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-200">
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Período</label>
                            <select
                                v-model="dateRange"
                                @change="onRangeChange"
                                class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none bg-gray-50"
                            >
                                <option value="last_30_days">Últimos 30 días</option>
                                <option value="this_year">Este Año</option>
                                <option value="custom">Personalizado</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Desde</label>
                            <input
                                type="date"
                                v-model="customStartDate"
                                @change="onCustomDateChange"
                                :disabled="dateRange !== 'custom'"
                                class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none disabled:bg-gray-100 disabled:text-gray-400"
                            />
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Hasta</label>
                            <input
                                type="date"
                                v-model="customEndDate"
                                @change="onCustomDateChange"
                                :disabled="dateRange !== 'custom'"
                                class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none disabled:bg-gray-100 disabled:text-gray-400"
                            />
                        </div>
                    </div>
                </div>
            </header>

            <!-- Loading -->
            <div v-if="loading" class="bg-white rounded-xl shadow-sm p-12 text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emi-navy-500 mx-auto"></div>
                <p class="mt-4 text-gray-500">Generando analítica...</p>
            </div>

            <!-- Error -->
            <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                <p class="text-red-700">{{ error }}</p>
            </div>

            <!-- Report Content -->
            <div v-else id="report-container" class="space-y-8">

                <!-- Hidden Date for PDF -->
                <div id="pdf-date-range" class="hidden mb-4 text-center">
                    <p class="text-lg font-bold text-gray-700">Reporte del Período</p>
                    <p class="text-gray-500">{{ formatDate(customStartDate) }} - {{ formatDate(customEndDate) }}</p>
                </div>

                <!-- Summary Cards -->
                <section>
                    <h2 class="text-lg font-semibold text-emi-navy-500 mb-4 flex flex-col sm:flex-row sm:justify-between sm:items-baseline gap-1">
                        <span>Resumen del Período</span>
                        <span class="text-xs font-normal text-gray-500">
                            {{ formatDate(customStartDate) }} — {{ formatDate(customEndDate) }}
                        </span>
                    </h2>
                    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
                        <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
                            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Usuarios Totales</p>
                            <p class="text-3xl font-bold text-emi-navy-500 mt-2">{{ usersSummary?.total_users }}</p>
                            <p class="text-xs text-green-600 mt-1 flex items-center">
                                <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>
                                +{{ usersSummary?.new_users_in_period }} en este período
                            </p>
                        </div>

                        <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
                            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Perfiles Activos</p>
                            <p class="text-3xl font-bold text-blue-600 mt-2">{{ profileStats?.profiles_active_in_period }}</p>
                            <p class="text-xs text-gray-400 mt-1">Con actividad en fecha</p>
                        </div>

                        <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
                            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Perfiles Completos</p>
                            <p class="text-3xl font-bold text-green-600 mt-2">{{ profileStats?.profiles_completed }}</p>
                            <p class="text-xs text-gray-400 mt-1">De los activos en período</p>
                        </div>

                        <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
                            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Estudiantes vs Titulados</p>
                            <div class="mt-2 text-sm">
                                <div class="flex justify-between mb-1">
                                    <span class="text-gray-600">Estudiantes</span>
                                    <span class="font-bold text-gray-800">{{ usersSummary?.roles.estudiante }}</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-gray-600">Titulados</span>
                                    <span class="font-bold text-gray-800">{{ usersSummary?.roles.titulado }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- Charts Row -->
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                        <h3 class="font-semibold text-gray-800 mb-6">Crecimiento de Usuarios</h3>
                        <UserGrowthChart v-if="userGrowth" :data="userGrowth" />
                    </div>

                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                        <h3 class="font-semibold text-gray-800 mb-6">Distribución por Rol</h3>
                        <UserDistributionChart v-if="usersSummary" :data="usersSummary" />
                    </div>
                </div>

                <!-- Skills Analysis -->
                <section>
                    <h2 class="text-lg font-semibold text-emi-navy-500 mb-4">Análisis de Talento (IA Extract)</h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                            <h3 class="font-semibold text-gray-800 mb-2 flex items-center gap-2">
                                <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                                Top Habilidades Técnicas
                            </h3>
                            <p class="text-xs text-gray-400 mb-6">Las herramientas y tecnologías más frecuentes en perfiles actualizados</p>
                            <SkillsBarChart v-if="skillsCloud?.hard_skills" :data="skillsCloud.hard_skills" color="#3B82F6" />
                        </div>

                        <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                            <h3 class="font-semibold text-gray-800 mb-2 flex items-center gap-2">
                                <span class="w-2 h-2 rounded-full bg-green-500"></span>
                                Top Habilidades Blandas
                            </h3>
                            <p class="text-xs text-gray-400 mb-6">Las competencias interpersonales más destacadas</p>
                            <SkillsBarChart v-if="skillsCloud?.soft_skills" :data="skillsCloud.soft_skills" color="#10B981" />
                        </div>
                    </div>
                </section>

                <!-- Footer for PDF -->
                <div class="text-center text-gray-400 text-xs mt-8 pb-4 print-only">
                    Reporte generado automáticamente por la plataforma de intermediación laboral.
                    {{ new Date().toLocaleDateString() }}
                </div>
            </div>
        </div>
    </AppLayout>
</template>

<style scoped>
.print-only {
    display: none;
}
</style>
