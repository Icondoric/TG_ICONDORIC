<script setup>
/**
 * ReportsView - Fase 7+
 * Vista de analitica y reportes con exportacion a PDF y filtros de fecha
 */
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/features/auth/store/auth.store'
import axios from 'axios'
import html2pdf from 'html2pdf.js'
import AppLayout from '@/shared/components/AppLayout.vue'
import { adminMenuItems } from '@/shared/constants/navigation'

// Charts
import UserDistributionChart from '../components/charts/UserDistributionChart.vue'
import UserGrowthChart from '../components/charts/UserGrowthChart.vue'
import SkillsBarChart from '../components/charts/SkillsBarChart.vue'

const router = useRouter()
const authStore = useAuthStore()
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// State
const loading = ref(true)
const error = ref(null)
const generatingPdf = ref(false)

// Date Filters
const dateRange = ref('last_30_days') // 'last_30_days', 'this_year', 'custom'
const customStartDate = ref('')
const customEndDate = ref('')

const usersSummary = ref(null)
const userGrowth = ref(null)
const skillsCloud = ref(null)
const profileStats = ref(null)

onMounted(async () => {
    if (!authStore.isAdmin) {
        router.push('/dashboard')
        return
    }
    // Set default dates based on selection
    updateCustomDatesFromRange()
    await loadData()
})

const updateCustomDatesFromRange = () => {
    const end = new Date()
    const start = new Date()

    if (dateRange.value === 'last_30_days') {
        start.setDate(end.getDate() - 30)
    } else if (dateRange.value === 'this_year') {
        start.setMonth(0, 1) // Jan 1st
    } else {
        return // Keep custom
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

        // Fetch all data in parallel
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

    // Show dates in PDF
    const dateDisplay = document.getElementById('pdf-date-range')
    if(dateDisplay) dateDisplay.style.display = 'block'

    const opt = {
        margin: [10, 10, 10, 10], // top, left, bottom, right
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
        if(dateDisplay) dateDisplay.style.display = 'none'
        generatingPdf.value = false
    }
}

const formatDate = (dateStr) => {
    if (!dateStr) return ''
    return new Date(dateStr).toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>

<template>
    <AppLayout :menuItems="adminMenuItems" variant="dark">
        <div class="max-w-7xl mx-auto py-8 px-4">
            <!-- Header & Filters -->
            <header class="mb-8 flex flex-col xl:flex-row xl:items-end justify-between gap-6">
                <div>
                    <h1 class="text-3xl font-bold text-slate-800">Reportes y Analitica</h1>
                    <p class="mt-1 text-slate-600">
                        Vision general del estado de la plataforma y el talento.
                    </p>
                </div>

                <div class="flex flex-col md:flex-row gap-4 items-end">
                    <!-- Filters -->
                    <div class="bg-white p-3 rounded-lg shadow-sm border border-slate-200 flex flex-col md:flex-row gap-3 items-center">
                        <select
                            v-model="dateRange"
                            @change="onRangeChange"
                            class="px-3 py-2 border border-slate-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 bg-slate-50"
                        >
                            <option value="last_30_days">Ultimos 30 dias</option>
                            <option value="this_year">Este Ano</option>
                            <option value="custom">Personalizado</option>
                        </select>

                        <div class="flex items-center gap-2">
                            <input
                                type="date"
                                v-model="customStartDate"
                                @change="onCustomDateChange"
                                :disabled="dateRange !== 'custom'"
                                class="px-2 py-1 border border-slate-300 rounded-md text-sm disabled:bg-slate-100 disabled:text-slate-400"
                            />
                            <span class="text-slate-400">-</span>
                            <input
                                type="date"
                                v-model="customEndDate"
                                @change="onCustomDateChange"
                                :disabled="dateRange !== 'custom'"
                                class="px-2 py-1 border border-slate-300 rounded-md text-sm disabled:bg-slate-100 disabled:text-slate-400"
                            />
                        </div>
                    </div>

                    <button
                        @click="generatePDF"
                        :disabled="loading || generatingPdf"
                        class="h-[46px] px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium flex items-center gap-2 disabled:opacity-50 whitespace-nowrap"
                    >
                        <svg v-if="!generatingPdf" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <div v-else class="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                        {{ generatingPdf ? 'PDF...' : 'Descargar' }}
                    </button>
                </div>
            </header>

            <!-- Loading -->
            <div v-if="loading" class="bg-white rounded-xl shadow-md p-12 text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p class="mt-4 text-slate-500">Generando analitica...</p>
            </div>

            <!-- Error -->
            <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                <p class="text-red-700">{{ error }}</p>
            </div>

            <!-- Report Content -->
            <div v-else id="report-container" class="space-y-8 bg-slate-50 p-4 -mx-4 sm:p-0 sm:mx-0 sm:bg-transparent">

                <!-- Hidden Date for PDF -->
                <div id="pdf-date-range" class="hidden mb-4 text-center">
                    <p class="text-lg font-bold text-slate-700">Reporte del Periodo</p>
                    <p class="text-slate-500">{{ formatDate(customStartDate) }} - {{ formatDate(customEndDate) }}</p>
                </div>

                <!-- Summary Cards -->
                <section>
                    <h2 class="text-lg font-semibold text-slate-800 mb-4 px-1 flex justify-between items-baseline">
                        <span>Resumen del Periodo</span>
                            <span class="text-xs font-normal text-slate-500">
                            {{ formatDate(customStartDate) }} - {{ formatDate(customEndDate) }}
                        </span>
                    </h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                        <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                            <p class="text-sm font-medium text-slate-500 uppercase">Usuarios Totales</p>
                            <p class="text-3xl font-bold text-slate-800 mt-2">{{ usersSummary?.total_users }}</p>
                            <p class="text-xs text-green-600 mt-1 flex items-center">
                                <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>
                                +{{ usersSummary?.new_users_in_period }} en este periodo
                            </p>
                        </div>

                        <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                            <p class="text-sm font-medium text-slate-500 uppercase">Perfiles Activos</p>
                            <p class="text-3xl font-bold text-blue-600 mt-2">{{ profileStats?.profiles_active_in_period }}</p>
                            <p class="text-xs text-slate-400 mt-1">Con actividad en fecha</p>
                        </div>

                        <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                            <p class="text-sm font-medium text-slate-500 uppercase">Perfiles Completos</p>
                            <p class="text-3xl font-bold text-green-600 mt-2">{{ profileStats?.profiles_completed }}</p>
                            <p class="text-xs text-slate-400 mt-1">De los activos en periodo</p>
                        </div>

                            <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                            <p class="text-sm font-medium text-slate-500 uppercase">Estudiantes vs Titulados</p>
                            <div class="mt-2 text-sm">
                                <div class="flex justify-between mb-1">
                                    <span>Estudiantes</span>
                                    <span class="font-bold">{{ usersSummary?.roles.estudiante }}</span>
                                </div>
                                <div class="flex justify-between">
                                    <span>Titulados</span>
                                    <span class="font-bold">{{ usersSummary?.roles.titulado }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- Charts Row 1 -->
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 break-inside-avoid">
                    <!-- User Growth -->
                    <div class="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                        <h3 class="font-semibold text-slate-800 mb-6">Crecimiento de Usuarios</h3>
                        <UserGrowthChart v-if="userGrowth" :data="userGrowth" />
                    </div>

                    <!-- User Distribution -->
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                        <h3 class="font-semibold text-slate-800 mb-6">Distribucion por Rol</h3>
                        <UserDistributionChart v-if="usersSummary" :data="usersSummary" />
                    </div>
                </div>

                <!-- Skills Analysis -->
                <section class="break-before-page">
                    <h2 class="text-lg font-semibold text-slate-800 mb-4 px-1 mt-8">Analisis de Talento (IA Extract)</h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <!-- Hard Skills -->
                        <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                            <h3 class="font-semibold text-slate-800 mb-2 flex items-center gap-2">
                                    <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                                    Top Habilidades Tecnicas
                            </h3>
                            <p class="text-xs text-slate-400 mb-6">Las herramientas y tecnologias mas frecuentes en perfiles actualizados</p>
                            <SkillsBarChart v-if="skillsCloud?.hard_skills" :data="skillsCloud.hard_skills" color="#3B82F6" />
                        </div>

                        <!-- Soft Skills -->
                        <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                            <h3 class="font-semibold text-slate-800 mb-2 flex items-center gap-2">
                                    <span class="w-2 h-2 rounded-full bg-green-500"></span>
                                    Top Habilidades Blandas
                            </h3>
                                <p class="text-xs text-slate-400 mb-6">Las competencias interpersonales mas destacadas</p>
                            <SkillsBarChart v-if="skillsCloud?.soft_skills" :data="skillsCloud.soft_skills" color="#10B981" />
                        </div>
                    </div>
                </section>

                    <!-- Footer for PDF -->
                <div class="text-center text-slate-400 text-xs mt-8 pb-4 print-only">
                    Reporte generado automaticamente por la plataforma de intermediacion laboral.
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
