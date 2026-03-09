<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/features/auth/store/auth.store'
import axios from 'axios'
import html2pdf from 'html2pdf.js'
import AppLayout from '@/shared/components/AppLayout.vue'
import UserDistributionChart from '../components/charts/UserDistributionChart.vue'
import UserGrowthChart from '../components/charts/UserGrowthChart.vue'
import SkillsBarChart from '../components/charts/SkillsBarChart.vue'

const authStore = useAuthStore()
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// ── Tab ────────────────────────────────────────────────────────────────────
const activeTab = ref('listado')

// ── TAB 1: Listado de Usuarios ─────────────────────────────────────────────
const loading = ref(true)
const error = ref(null)
const generatingPdf = ref(false)
const pdfMode = ref(false)
const showPdfConfig = ref(false)

const startDate = ref('')
const endDate = ref('')
const roleFilter = ref('')
const hasCvFilter = ref('')
const profileCompleteFilter = ref('')
const completenessMinFilter = ref('')
const cvUpdatedSinceFilter = ref('')
const carreraFilter = ref('')

const reportData = ref(null)

const PDF_COLUMNS = [
    { key: 'usuario',           label: 'Usuario (Nombre + Email)', locked: true },
    { key: 'rol',               label: 'Rol' },
    { key: 'carrera',           label: 'Carrera' },
    { key: 'registro',          label: 'Fecha de registro' },
    { key: 'cv',                label: 'CV (tiene o no)' },
    { key: 'cv_uploaded_at',    label: 'Última carga de CV' },
    { key: 'perfil_updated_at', label: 'Última actualización de perfil' },
    { key: 'completitud',       label: 'Score de completitud' },
]
const pdfColEnabled = ref(Object.fromEntries(PDF_COLUMNS.map(c => [c.key, true])))
const colVisible = (key) => !pdfMode.value || pdfColEnabled.value[key]

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
            role: roleFilter.value || undefined,
            has_cv: hasCvFilter.value !== '' ? hasCvFilter.value === 'true' : undefined,
            profile_complete: profileCompleteFilter.value !== '' ? profileCompleteFilter.value === 'true' : undefined,
            completeness_min: completenessMinFilter.value !== '' ? Number(completenessMinFilter.value) : undefined,
            cv_updated_since: cvUpdatedSinceFilter.value || undefined,
            carrera: carreraFilter.value || undefined,
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

const resetFilters = () => {
    roleFilter.value = ''
    hasCvFilter.value = ''
    profileCompleteFilter.value = ''
    completenessMinFilter.value = ''
    cvUpdatedSinceFilter.value = ''
    carreraFilter.value = ''
    const end = new Date()
    const start = new Date()
    start.setDate(end.getDate() - 90)
    endDate.value = end.toISOString().split('T')[0]
    startDate.value = start.toISOString().split('T')[0]
    loadData()
}

const openPdfConfig = () => { showPdfConfig.value = true }

const confirmAndGeneratePDF = async () => {
    showPdfConfig.value = false
    generatingPdf.value = true
    pdfMode.value = true
    await new Promise(r => setTimeout(r, 150))
    const element = document.getElementById('users-report-container')
    const opt = {
        margin: [12, 8, 12, 8],
        filename: `reporte-usuarios-${startDate.value}_${endDate.value}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true, logging: false },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'landscape' },
        pagebreak: { mode: ['css', 'legacy'] }
    }
    try {
        await html2pdf().set(opt).from(element).save()
    } catch (err) {
        console.error('Error generating PDF:', err)
    } finally {
        pdfMode.value = false
        generatingPdf.value = false
    }
}

const scoreColor = (score) => {
    if (score >= 70) return 'bg-green-500'
    if (score >= 40) return 'bg-yellow-400'
    return 'bg-red-400'
}
const scoreTextColor = (score) => {
    if (score >= 70) return 'text-green-700'
    if (score >= 40) return 'text-yellow-700'
    return 'text-red-600'
}
const rolBadge = (rol) => {
    const map = {
        estudiante:    'bg-blue-100 text-blue-700 border border-blue-200',
        titulado:      'bg-purple-100 text-purple-700 border border-purple-200',
        operador:      'bg-orange-100 text-orange-700 border border-orange-200',
        administrador: 'bg-red-100 text-red-700 border border-red-200',
    }
    return map[rol] || 'bg-gray-100 text-gray-600 border border-gray-200'
}

const activeFiltersCount = computed(() => {
    let n = 0
    if (roleFilter.value) n++
    if (hasCvFilter.value !== '') n++
    if (profileCompleteFilter.value !== '') n++
    if (completenessMinFilter.value !== '') n++
    if (cvUpdatedSinceFilter.value) n++
    if (carreraFilter.value) n++
    return n
})

const enabledPdfColCount = computed(() =>
    PDF_COLUMNS.filter(c => pdfColEnabled.value[c.key]).length
)

// ── TAB 2: Analítica General ───────────────────────────────────────────────
const analyticsLoaded = ref(false)
const analyticsLoading = ref(false)
const analyticsError = ref(null)
const generatingAnalyticsPdf = ref(false)

const dateRange = ref('last_30_days')
const customStartDate = ref('')
const customEndDate = ref('')

const usersSummary = ref(null)
const userGrowth = ref(null)
const skillsCloud = ref(null)
const profileStats = ref(null)

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
        loadAnalytics()
    }
}

const onCustomDateChange = () => {
    if (dateRange.value === 'custom' && customStartDate.value && customEndDate.value) {
        loadAnalytics()
    }
}

const loadAnalytics = async () => {
    analyticsLoading.value = true
    analyticsError.value = null
    try {
        const headers = { Authorization: `Bearer ${authStore.token}` }
        const params = { start_date: customStartDate.value, end_date: customEndDate.value }
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
        analyticsLoaded.value = true
    } catch (err) {
        console.error('Error loading analytics:', err)
        analyticsError.value = 'Error al cargar los datos de analítica.'
    } finally {
        analyticsLoading.value = false
    }
}

const switchTab = (tab) => {
    activeTab.value = tab
    if (tab === 'analitica' && !analyticsLoaded.value) {
        updateCustomDatesFromRange()
        loadAnalytics()
    }
}

const generateAnalyticsPDF = async () => {
    generatingAnalyticsPdf.value = true
    const element = document.getElementById('analytics-container')
    const opt = {
        margin: [10, 10, 10, 10],
        filename: `analitica-general-${customStartDate.value}_${customEndDate.value}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
        pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
    }
    try {
        await html2pdf().set(opt).from(element).save()
    } catch (err) {
        console.error('Error generating PDF:', err)
    } finally {
        generatingAnalyticsPdf.value = false
    }
}

const formatDate = (dateStr) => {
    if (!dateStr) return '-'
    return new Date(dateStr).toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>

<template>
    <AppLayout>
        <div class="py-6 px-4 sm:px-6 lg:px-8 min-w-0">

            <!-- ── Header ──────────────────────────────────────────────── -->
            <header class="mb-4" :class="{ 'hidden': pdfMode }">
                <div class="flex flex-col xl:flex-row xl:items-center justify-between gap-4">
                    <div>
                        <h1 class="text-2xl font-bold text-emi-navy-500">Reporte de Usuarios</h1>
                        <p class="mt-0.5 text-sm text-gray-500">Listado y analítica de usuarios registrados en la plataforma.</p>
                    </div>
                    <!-- PDF button: only show on active tab -->
                    <button v-if="activeTab === 'listado'"
                        @click="openPdfConfig"
                        :disabled="loading || generatingPdf"
                        class="h-10 px-5 bg-emi-navy-600 text-white rounded-lg hover:bg-emi-navy-700 transition-colors text-sm font-medium inline-flex items-center gap-2 disabled:opacity-50 whitespace-nowrap self-start xl:self-auto"
                    >
                        <svg v-if="!generatingPdf" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <div v-else class="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                        {{ generatingPdf ? 'Generando PDF...' : 'Exportar PDF' }}
                    </button>
                    <button v-if="activeTab === 'analitica'"
                        @click="generateAnalyticsPDF"
                        :disabled="analyticsLoading || generatingAnalyticsPdf || !analyticsLoaded"
                        class="h-10 px-5 bg-emi-navy-600 text-white rounded-lg hover:bg-emi-navy-700 transition-colors text-sm font-medium inline-flex items-center gap-2 disabled:opacity-50 whitespace-nowrap self-start xl:self-auto"
                    >
                        <svg v-if="!generatingAnalyticsPdf" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <div v-else class="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                        {{ generatingAnalyticsPdf ? 'Generando PDF...' : 'Descargar PDF' }}
                    </button>
                </div>
            </header>

            <!-- ── Tab bar ─────────────────────────────────────────────── -->
            <div v-if="!pdfMode" class="flex border-b border-gray-200 mb-6">
                <button @click="switchTab('listado')"
                    class="px-5 py-2.5 text-sm font-medium border-b-2 transition-colors"
                    :class="activeTab === 'listado' ? 'border-emi-navy-600 text-emi-navy-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                >
                    Listado de Usuarios
                </button>
                <button @click="switchTab('analitica')"
                    class="px-5 py-2.5 text-sm font-medium border-b-2 transition-colors"
                    :class="activeTab === 'analitica' ? 'border-emi-navy-600 text-emi-navy-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                >
                    Analítica General
                </button>
            </div>

            <!-- ══════════════════════════════════════════════════════════ -->
            <!-- TAB 1: Listado de Usuarios                                -->
            <!-- ══════════════════════════════════════════════════════════ -->
            <template v-if="activeTab === 'listado' || pdfMode">

                <!-- Modal PDF config -->
                <Teleport to="body">
                    <div v-if="showPdfConfig" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
                        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4">
                            <div class="px-6 pt-5 pb-4 border-b border-gray-100 flex items-center justify-between">
                                <div>
                                    <h2 class="text-base font-semibold text-gray-800">Configurar exportación PDF</h2>
                                    <p class="text-xs text-gray-400 mt-0.5">Selecciona las columnas que aparecerán en el PDF</p>
                                </div>
                                <button @click="showPdfConfig = false" class="text-gray-400 hover:text-gray-600 p-1">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                                    </svg>
                                </button>
                            </div>
                            <div class="px-6 py-4 space-y-2">
                                <label v-for="col in PDF_COLUMNS" :key="col.key"
                                    class="flex items-center gap-3 p-2.5 rounded-lg cursor-pointer transition-colors"
                                    :class="col.locked ? 'bg-gray-50 cursor-not-allowed opacity-60' : 'hover:bg-gray-50'"
                                >
                                    <input type="checkbox" v-model="pdfColEnabled[col.key]" :disabled="col.locked" class="w-4 h-4 rounded border-gray-300 accent-blue-600" />
                                    <span class="text-sm text-gray-700">{{ col.label }}</span>
                                    <span v-if="col.locked" class="ml-auto text-xs text-gray-400 italic">obligatorio</span>
                                </label>
                            </div>
                            <div class="px-6 pb-5 pt-2 flex items-center justify-between border-t border-gray-100 mt-2">
                                <span class="text-xs text-gray-400">{{ enabledPdfColCount }} columnas seleccionadas</span>
                                <div class="flex gap-2">
                                    <button @click="showPdfConfig = false" class="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-200 rounded-lg">Cancelar</button>
                                    <button @click="confirmAndGeneratePDF" class="px-5 py-2 text-sm bg-emi-navy-600 text-white rounded-lg hover:bg-emi-navy-700 font-medium inline-flex items-center gap-1.5">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                                        </svg>
                                        Generar PDF
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </Teleport>

                <!-- Filtros -->
                <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-200 mb-6" :class="{ 'hidden': pdfMode }">
                    <div class="flex items-center justify-between mb-4">
                        <h2 class="text-sm font-semibold text-gray-700 inline-flex items-center gap-2">
                            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2a1 1 0 01-.293.707L13 13.414V19a1 1 0 01-.553.894l-4 2A1 1 0 017 21v-7.586L3.293 6.707A1 1 0 013 6V4z"/>
                            </svg>
                            Filtros
                            <span v-if="activeFiltersCount > 0" class="bg-emi-navy-100 text-emi-navy-700 text-xs font-bold px-2 py-0.5 rounded-full">
                                {{ activeFiltersCount }} activos
                            </span>
                        </h2>
                        <button @click="resetFilters" class="text-xs text-gray-400 hover:text-gray-600 underline">Limpiar todo</button>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-3">
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Registro desde</label>
                            <input type="date" v-model="startDate" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Registro hasta</label>
                            <input type="date" v-model="endDate" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Rol</label>
                            <select v-model="roleFilter" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none">
                                <option value="">Todos los roles</option>
                                <option value="estudiante">Estudiante</option>
                                <option value="titulado">Titulado</option>
                                <option value="operador">Operador</option>
                                <option value="administrador">Administrador</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">CV subido</label>
                            <select v-model="hasCvFilter" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none">
                                <option value="">Todos</option>
                                <option value="true">Con CV</option>
                                <option value="false">Sin CV</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 items-end">
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Estado del perfil</label>
                            <select v-model="profileCompleteFilter" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none">
                                <option value="">Todos</option>
                                <option value="true">Perfil completo</option>
                                <option value="false">Perfil incompleto</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Score mínimo</label>
                            <select v-model="completenessMinFilter" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none">
                                <option value="">Sin mínimo</option>
                                <option value="25">≥ 25%</option>
                                <option value="50">≥ 50%</option>
                                <option value="70">≥ 70%</option>
                                <option value="90">≥ 90%</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">CV actualizado desde</label>
                            <input type="date" v-model="cvUpdatedSinceFilter" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Carrera</label>
                            <input type="text" v-model="carreraFilter" placeholder="Ej: Sistemas, Civil..." class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                        </div>
                    </div>
                    <div class="mt-4 flex justify-end">
                        <button @click="loadData" :disabled="loading" class="px-5 py-2 bg-emi-navy-600 text-white rounded-lg text-sm hover:bg-emi-navy-700 disabled:opacity-50 font-medium">
                            Aplicar filtros
                        </button>
                    </div>
                </div>

                <!-- Loading -->
                <div v-if="loading" class="bg-white rounded-xl p-12 text-center">
                    <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-emi-navy-500 mx-auto"></div>
                    <p class="mt-4 text-sm text-gray-400">Cargando reporte...</p>
                </div>

                <!-- Error -->
                <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
                    <p class="text-sm text-red-700">{{ error }}</p>
                </div>

                <!-- Contenido -->
                <div v-else id="users-report-container" class="space-y-5">

                    <!-- Encabezado PDF -->
                    <div v-if="pdfMode" class="bg-emi-navy-700 text-white px-6 py-4 rounded-xl flex items-center justify-between">
                        <div>
                            <p class="text-[10px] text-blue-200 uppercase tracking-widest mb-1">Sistema de Bolsa Laboral — EMI</p>
                            <h1 class="text-xl font-bold">Reporte de Usuarios</h1>
                            <p class="text-xs text-blue-100 mt-0.5">Período: {{ formatDate(startDate) }} — {{ formatDate(endDate) }}</p>
                        </div>
                        <div class="text-right text-xs text-blue-100 space-y-1">
                            <p>Generado: {{ formatDate(new Date().toISOString()) }}</p>
                            <p>Total mostrado: <span class="font-bold text-white">{{ reportData?.users?.length }}</span> usuarios</p>
                        </div>
                    </div>

                    <!-- Tarjetas resumen -->
                    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
                        <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                            <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Total</p>
                            <p class="text-2xl font-bold text-emi-navy-500 mt-1">{{ reportData?.stats.total }}</p>
                            <p class="text-[11px] text-gray-400">usuarios</p>
                        </div>
                        <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                            <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Con CV</p>
                            <p class="text-2xl font-bold text-blue-600 mt-1">{{ reportData?.stats.with_cv }}</p>
                            <p class="text-[11px] text-gray-400">{{ reportData?.stats.with_cv_pct }}% del total</p>
                        </div>
                        <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                            <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Perfil Completo</p>
                            <p class="text-2xl font-bold text-green-600 mt-1">{{ reportData?.stats.profile_complete }}</p>
                            <p class="text-[11px] text-gray-400">{{ reportData?.stats.profile_complete_pct }}% del total</p>
                        </div>
                        <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                            <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Completitud Prom.</p>
                            <p class="text-2xl font-bold mt-1" :class="scoreTextColor(reportData?.stats.avg_completeness)">
                                {{ reportData?.stats.avg_completeness }}%
                            </p>
                            <p class="text-[11px] text-gray-400">promedio general</p>
                        </div>
                    </div>

                    <!-- Por Rol -->
                    <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-2">Distribución por Rol</p>
                        <div class="flex flex-wrap gap-3">
                            <div v-for="(count, rol) in reportData?.stats.by_role" :key="rol" class="flex items-center gap-2">
                                <span class="text-[11px] capitalize text-gray-600">{{ rol }}</span>
                                <span class="text-[11px] font-bold text-gray-800 bg-gray-100 px-2 py-0.5 rounded-full">{{ count }}</span>
                            </div>
                        </div>
                    </div>

                    <!-- Tabla -->
                    <div class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
                        <div class="px-5 py-3 border-b border-gray-100 flex items-center gap-2" :class="{ 'hidden': pdfMode }">
                            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
                            </svg>
                            <span class="text-sm font-semibold text-gray-700">Listado de usuarios</span>
                            <span class="text-xs text-gray-400">({{ reportData?.users?.length }} registros)</span>
                        </div>
                        <div class="overflow-x-auto">
                            <table class="min-w-full text-xs">
                                <thead>
                                    <tr class="bg-gray-50 border-b border-gray-100">
                                        <th class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">#</th>
                                        <th class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Usuario</th>
                                        <th v-if="colVisible('rol')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Rol</th>
                                        <th v-if="colVisible('carrera')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Carrera</th>
                                        <th v-if="colVisible('registro')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Registro</th>
                                        <th v-if="colVisible('cv')" class="px-4 py-2.5 text-center font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">CV</th>
                                        <th v-if="colVisible('cv_uploaded_at')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Últ. carga CV</th>
                                        <th v-if="colVisible('perfil_updated_at')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Últ. act. perfil</th>
                                        <th v-if="colVisible('completitud')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Completitud</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr
                                        v-for="(user, idx) in reportData?.users"
                                        :key="user.id"
                                        class="border-b border-gray-100 hover:bg-gray-50/60 transition-colors"
                                        :class="idx % 2 === 0 ? '' : 'bg-gray-50/30'"
                                    >
                                        <td class="px-4 py-2.5 text-gray-300 font-mono select-none">{{ idx + 1 }}</td>
                                        <td class="px-4 py-2.5 min-w-[180px]">
                                            <p class="font-medium text-gray-800 leading-tight">{{ user.nombre_completo || '—' }}</p>
                                            <p class="text-gray-400 mt-0.5 truncate max-w-[200px]">{{ user.email }}</p>
                                        </td>
                                        <td v-if="colVisible('rol')" class="px-4 py-2.5">
                                            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium capitalize" :class="rolBadge(user.rol)">
                                                {{ user.rol }}
                                            </span>
                                        </td>
                                        <td v-if="colVisible('carrera')" class="px-4 py-2.5 text-gray-600 whitespace-nowrap">
                                            <span v-if="user.carrera">{{ user.carrera }}<span v-if="user.semestre_actual" class="text-gray-400"> · Sem. {{ user.semestre_actual }}</span></span>
                                            <span v-else class="text-gray-300">—</span>
                                        </td>
                                        <td v-if="colVisible('registro')" class="px-4 py-2.5 text-gray-500 whitespace-nowrap">{{ formatDate(user.fecha_registro) }}</td>
                                        <td v-if="colVisible('cv')" class="px-4 py-2.5 text-center">
                                            <span v-if="user.tiene_cv" class="inline-flex items-center gap-1 text-green-600 font-medium">
                                                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
                                                Sí
                                            </span>
                                            <span v-else class="text-gray-300">No</span>
                                        </td>
                                        <td v-if="colVisible('cv_uploaded_at')" class="px-4 py-2.5 whitespace-nowrap">
                                            <span v-if="user.cv_uploaded_at" class="text-blue-600 font-medium">{{ formatDate(user.cv_uploaded_at) }}</span>
                                            <span v-else class="text-gray-300">—</span>
                                        </td>
                                        <td v-if="colVisible('perfil_updated_at')" class="px-4 py-2.5 text-gray-500 whitespace-nowrap">{{ formatDate(user.perfil_updated_at) }}</td>
                                        <td v-if="colVisible('completitud')" class="px-4 py-2.5 min-w-[120px]">
                                            <div class="flex items-center gap-2">
                                                <div class="flex-1 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                                                    <div class="h-1.5 rounded-full" :class="scoreColor(user.completeness_score)" :style="{ width: user.completeness_score + '%' }"></div>
                                                </div>
                                                <span class="text-[11px] font-semibold w-8 text-right shrink-0" :class="scoreTextColor(user.completeness_score)">
                                                    {{ user.completeness_score }}%
                                                </span>
                                            </div>
                                        </td>
                                    </tr>
                                    <tr v-if="!reportData?.users?.length">
                                        <td colspan="9" class="px-4 py-10 text-center text-gray-400 text-sm">
                                            No se encontraron usuarios con los filtros seleccionados.
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Pie PDF -->
                    <div v-if="pdfMode" class="text-center text-[10px] text-gray-400 pt-1">
                        Reporte generado automáticamente — Sistema de Bolsa Laboral EMI
                    </div>
                </div>
            </template>

            <!-- ══════════════════════════════════════════════════════════ -->
            <!-- TAB 2: Analítica General                                  -->
            <!-- ══════════════════════════════════════════════════════════ -->
            <template v-if="activeTab === 'analitica'">

                <!-- Filtros de período -->
                <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-200 mb-6">
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Período</label>
                            <select v-model="dateRange" @change="onRangeChange"
                                class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none bg-gray-50"
                            >
                                <option value="last_30_days">Últimos 30 días</option>
                                <option value="this_year">Este Año</option>
                                <option value="custom">Personalizado</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Desde</label>
                            <input type="date" v-model="customStartDate" @change="onCustomDateChange" :disabled="dateRange !== 'custom'"
                                class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none disabled:bg-gray-100 disabled:text-gray-400"
                            />
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Hasta</label>
                            <input type="date" v-model="customEndDate" @change="onCustomDateChange" :disabled="dateRange !== 'custom'"
                                class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none disabled:bg-gray-100 disabled:text-gray-400"
                            />
                        </div>
                    </div>
                </div>

                <!-- Loading -->
                <div v-if="analyticsLoading" class="bg-white rounded-xl shadow-sm p-12 text-center">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emi-navy-500 mx-auto"></div>
                    <p class="mt-4 text-gray-500">Generando analítica...</p>
                </div>

                <!-- Error -->
                <div v-else-if="analyticsError" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                    <p class="text-red-700">{{ analyticsError }}</p>
                </div>

                <!-- Contenido analítica -->
                <div v-else-if="analyticsLoaded" id="analytics-container" class="space-y-8">

                    <!-- Tarjetas resumen -->
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

                    <!-- Gráficas -->
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

                    <!-- Habilidades -->
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
                </div>
            </template>

        </div>
    </AppLayout>
</template>
