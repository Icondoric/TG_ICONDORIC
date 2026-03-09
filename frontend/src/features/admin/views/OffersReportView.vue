<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/features/auth/store/auth.store'
import axios from 'axios'
import html2pdf from 'html2pdf.js'
import AppLayout from '@/shared/components/AppLayout.vue'

const authStore = useAuthStore()
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// ── Tab ────────────────────────────────────────────────────────────────────
const activeTab = ref('listado')

// ── TAB 1: Listado ─────────────────────────────────────────────────────────
const loading = ref(true)
const error = ref(null)
const generatingPdf = ref(false)
const pdfMode = ref(false)
const showPdfConfig = ref(false)

// ── Filtros ────────────────────────────────────────────────────────────────
const startDate = ref('')
const endDate = ref('')
const tipoFilter = ref('')
const estadoFilter = ref('')
const modalidadFilter = ref('')
const sectorFilter = ref('')
const institucionFilter = ref('')
const areaFilter = ref('')
// Nuevos filtros por postulante
const conPostulacionesFilter = ref('')
const rolPostulanteFilter = ref('')
const carreraPostulanteFilter = ref('')
const minPostulacionesFilter = ref('')
const minScoreFilter = ref('')

const reportData = ref(null)

// ── Columnas PDF ───────────────────────────────────────────────────────────
const PDF_COLUMNS = [
    { key: 'oferta',             label: 'Convocatoria (Título + Institución)',   locked: true },
    { key: 'tipo',               label: 'Tipo' },
    { key: 'modalidad',          label: 'Modalidad' },
    { key: 'sector',             label: 'Sector' },
    { key: 'area',               label: 'Área' },
    { key: 'estado',             label: 'Estado' },
    { key: 'fechas',             label: 'Fechas (Inicio / Cierre)' },
    { key: 'dias_restantes',     label: 'Días restantes' },
    { key: 'cupos',              label: 'Cupos disponibles' },
    { key: 'postulaciones',      label: 'Postulaciones (Total / A-C-N)' },
    { key: 'postulantes_rol',    label: 'Postulantes Est. vs Tit.' },
    { key: 'carreras',           label: 'Top carreras postulantes' },
    { key: 'score',              label: 'Score promedio' },
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
            tipo: tipoFilter.value || undefined,
            estado: estadoFilter.value || undefined,
            modalidad: modalidadFilter.value || undefined,
            sector: sectorFilter.value || undefined,
            institucion: institucionFilter.value || undefined,
            area: areaFilter.value || undefined,
            con_postulaciones: conPostulacionesFilter.value === 'true' ? true : undefined,
            rol_postulante: rolPostulanteFilter.value || undefined,
            carrera_postulante: carreraPostulanteFilter.value || undefined,
            min_postulaciones: minPostulacionesFilter.value !== '' ? Number(minPostulacionesFilter.value) : undefined,
            min_score: minScoreFilter.value !== '' ? Number(minScoreFilter.value) : undefined,
        }
        const res = await axios.get(`${API_URL}/api/analytics/offers-report`, { headers, params })
        reportData.value = res.data
    } catch (err) {
        console.error('Error loading offers report:', err)
        error.value = 'Error al cargar el reporte de convocatorias.'
    } finally {
        loading.value = false
    }
}

const resetFilters = () => {
    tipoFilter.value = ''
    estadoFilter.value = ''
    modalidadFilter.value = ''
    sectorFilter.value = ''
    institucionFilter.value = ''
    areaFilter.value = ''
    conPostulacionesFilter.value = ''
    rolPostulanteFilter.value = ''
    carreraPostulanteFilter.value = ''
    minPostulacionesFilter.value = ''
    minScoreFilter.value = ''
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
    const element = document.getElementById('offers-report-container')
    const opt = {
        margin: [12, 8, 12, 8],
        filename: `reporte-ofertas-${startDate.value}_${endDate.value}.pdf`,
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

const formatDate = (dateStr) => {
    if (!dateStr) return '—'
    return new Date(dateStr).toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' })
}

const estadoBadge = (estado) => {
    const map = {
        activa:   'bg-green-100 text-green-700 border border-green-200',
        inactiva: 'bg-gray-100 text-gray-600 border border-gray-200',
        expirada: 'bg-red-100 text-red-700 border border-red-200',
    }
    return map[estado] || 'bg-gray-100 text-gray-600'
}

const tipoBadge = (tipo) => tipo === 'pasantia'
    ? 'bg-blue-100 text-blue-700 border border-blue-200'
    : 'bg-purple-100 text-purple-700 border border-purple-200'

const modalidadBadge = (modalidad) => {
    const map = {
        presencial: 'bg-orange-100 text-orange-700',
        remoto:     'bg-teal-100 text-teal-700',
        hibrido:    'bg-indigo-100 text-indigo-700',
    }
    return map[modalidad] || 'bg-gray-100 text-gray-600'
}

const diasColor = (dias) => {
    if (dias === null || dias === undefined) return 'text-gray-300'
    if (dias <= 7) return 'text-red-600 font-semibold'
    if (dias <= 30) return 'text-yellow-600 font-medium'
    return 'text-green-600'
}

const scoreBar = (score) => {
    if (score === null || score === undefined) return ''
    if (score >= 70) return 'bg-green-500'
    if (score >= 40) return 'bg-yellow-400'
    return 'bg-red-400'
}
const scoreText = (score) => {
    if (score === null || score === undefined) return 'text-gray-300'
    if (score >= 70) return 'text-green-700'
    if (score >= 40) return 'text-yellow-700'
    return 'text-red-600'
}

const activeFiltersCount = computed(() => {
    let n = 0
    if (tipoFilter.value) n++
    if (estadoFilter.value) n++
    if (modalidadFilter.value) n++
    if (sectorFilter.value) n++
    if (institucionFilter.value) n++
    if (areaFilter.value) n++
    if (conPostulacionesFilter.value) n++
    if (rolPostulanteFilter.value) n++
    if (carreraPostulanteFilter.value) n++
    if (minPostulacionesFilter.value !== '') n++
    if (minScoreFilter.value !== '') n++
    return n
})

const enabledPdfColCount = computed(() =>
    PDF_COLUMNS.filter(c => pdfColEnabled.value[c.key]).length
)

// Top carreras del reporte para mini-chart
const topCarrerasGlobal = computed(() => {
    const entries = Object.entries(reportData.value?.stats.top_carreras || {})
    const max = Math.max(...entries.map(([, v]) => v), 1)
    return entries
        .sort(([, a], [, b]) => b - a)
        .slice(0, 6)
        .map(([name, count]) => ({ name, count, pct: Math.round(count / max * 100) }))
})

// ── TAB 2: Cumplimiento por Convocatoria ───────────────────────────────────
const compLoaded = ref(false)
const compLoading = ref(false)
const compError = ref(null)
const compGeneratingPdf = ref(false)
const compPdfMode = ref(false)
const compShowPdfConfig = ref(false)

const compStartDate = ref('')
const compEndDate = ref('')
const compTipoFilter = ref('')
const compTipoInstFilter = ref('')
const compEstadoFilter = ref('')
const compInstitucionFilter = ref('')
const compData = ref(null)

const COMP_PDF_COLUMNS = [
    { key: 'convocatoria', label: 'Convocatoria (Título + Institución)', locked: true },
    { key: 'tipo_inst',    label: 'Tipo de institución' },
    { key: 'tipo',         label: 'Tipo (Pasantía / Empleo)' },
    { key: 'estado',       label: 'Estado' },
    { key: 'fechas',       label: 'Fechas (Inicio / Cierre)' },
    { key: 'cupos',        label: 'Cupos disponibles' },
    { key: 'postulaciones',label: 'Postulaciones (Total / A-C-N)' },
    { key: 'cumplimiento', label: '% Cumplimiento', locked: true },
]
const compPdfColEnabled = ref(Object.fromEntries(COMP_PDF_COLUMNS.map(c => [c.key, true])))
const compColVisible = (key) => !compPdfMode.value || compPdfColEnabled.value[key]

const compActiveFiltersCount = computed(() => {
    let n = 0
    if (compTipoFilter.value) n++
    if (compTipoInstFilter.value) n++
    if (compEstadoFilter.value) n++
    if (compInstitucionFilter.value) n++
    return n
})

const compEnabledPdfColCount = computed(() =>
    COMP_PDF_COLUMNS.filter(c => compPdfColEnabled.value[c.key]).length
)

const convocatoriasOrdenadas = computed(() =>
    [...(compData.value?.convocatorias || [])].sort((a, b) => a.pct_cumplimiento - b.pct_cumplimiento)
)

const loadCompliance = async () => {
    compLoading.value = true
    compError.value = null
    try {
        const headers = { Authorization: `Bearer ${authStore.token}` }
        const params = {
            start_date: compStartDate.value || undefined,
            end_date: compEndDate.value || undefined,
            tipo: compTipoFilter.value || undefined,
            tipo_institucion: compTipoInstFilter.value || undefined,
            estado: compEstadoFilter.value || undefined,
            institucion: compInstitucionFilter.value || undefined,
        }
        const res = await axios.get(`${API_URL}/api/analytics/compliance-report`, { headers, params })
        compData.value = res.data
        compLoaded.value = true
    } catch (err) {
        console.error('Error loading compliance report:', err)
        compError.value = 'Error al cargar el reporte de cumplimiento.'
    } finally {
        compLoading.value = false
    }
}

const resetCompFilters = () => {
    compTipoFilter.value = ''
    compTipoInstFilter.value = ''
    compEstadoFilter.value = ''
    compInstitucionFilter.value = ''
    const end = new Date()
    const start = new Date()
    start.setDate(end.getDate() - 90)
    compEndDate.value = end.toISOString().split('T')[0]
    compStartDate.value = start.toISOString().split('T')[0]
    loadCompliance()
}

const confirmAndGenerateCompPDF = async () => {
    compShowPdfConfig.value = false
    compGeneratingPdf.value = true
    compPdfMode.value = true
    await new Promise(r => setTimeout(r, 150))
    const element = document.getElementById('compliance-report-container')
    const opt = {
        margin: [12, 8, 12, 8],
        filename: `reporte-cumplimiento-${compStartDate.value}_${compEndDate.value}.pdf`,
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
        compPdfMode.value = false
        compGeneratingPdf.value = false
    }
}

const cumplimientoColor = (pct) => {
    if (pct >= 80) return 'bg-green-500'
    if (pct >= 40) return 'bg-yellow-400'
    return 'bg-red-400'
}
const cumplimientoText = (pct) => {
    if (pct >= 80) return 'text-green-700 font-semibold'
    if (pct >= 40) return 'text-yellow-700 font-medium'
    return 'text-red-600 font-medium'
}

const tipoBadgeInst = (tipo) => {
    const map = {
        'Pública':  'bg-blue-100 text-blue-700 border border-blue-200',
        'Privada':  'bg-purple-100 text-purple-700 border border-purple-200',
        'Mixta':    'bg-teal-100 text-teal-700 border border-teal-200',
        'ONG':      'bg-orange-100 text-orange-700 border border-orange-200',
    }
    return map[tipo] || 'bg-gray-100 text-gray-600 border border-gray-200'
}

const switchTab = (tab) => {
    activeTab.value = tab
    if (tab === 'cumplimiento' && !compLoaded.value) {
        const end = new Date()
        const start = new Date()
        start.setDate(end.getDate() - 90)
        compEndDate.value = end.toISOString().split('T')[0]
        compStartDate.value = start.toISOString().split('T')[0]
        loadCompliance()
    }
}
</script>

<template>
    <AppLayout>
        <div class="py-6 px-4 sm:px-6 lg:px-8 min-w-0">

            <!-- ── Header ──────────────────────────────────────────────── -->
            <header class="mb-4" :class="{ 'hidden': pdfMode && activeTab === 'listado' || compPdfMode && activeTab === 'cumplimiento' }">
                <div class="flex flex-col xl:flex-row xl:items-center justify-between gap-4">
                    <div>
                        <h1 class="text-2xl font-bold text-emi-navy-500">Reporte de Convocatorias</h1>
                        <p class="mt-0.5 text-sm text-gray-500">Listado de convocatorias laborales y análisis de cumplimiento.</p>
                    </div>
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
                    <button v-if="activeTab === 'cumplimiento'"
                        @click="compShowPdfConfig = true"
                        :disabled="compLoading || compGeneratingPdf || !compLoaded"
                        class="h-10 px-5 bg-emi-navy-600 text-white rounded-lg hover:bg-emi-navy-700 transition-colors text-sm font-medium inline-flex items-center gap-2 disabled:opacity-50 whitespace-nowrap self-start xl:self-auto"
                    >
                        <svg v-if="!compGeneratingPdf" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <div v-else class="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                        {{ compGeneratingPdf ? 'Generando PDF...' : 'Exportar PDF' }}
                    </button>
                </div>
            </header>

            <!-- ── Tab bar ─────────────────────────────────────────────── -->
            <div v-if="!pdfMode && !compPdfMode" class="flex border-b border-gray-200 mb-6">
                <button @click="switchTab('listado')"
                    class="px-5 py-2.5 text-sm font-medium border-b-2 transition-colors"
                    :class="activeTab === 'listado' ? 'border-emi-navy-600 text-emi-navy-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                >
                    Listado de Convocatorias
                </button>
                <button @click="switchTab('cumplimiento')"
                    class="px-5 py-2.5 text-sm font-medium border-b-2 transition-colors"
                    :class="activeTab === 'cumplimiento' ? 'border-emi-navy-600 text-emi-navy-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                >
                    Cumplimiento por Convocatoria
                </button>
            </div>

            <!-- ══════════════════════════════════════════════════════════ -->
            <!-- TAB 1: Listado de Convocatorias                           -->
            <!-- ══════════════════════════════════════════════════════════ -->
            <template v-if="activeTab === 'listado' || pdfMode">

            <!-- ── Modal: configuración de columnas PDF ────────────────── -->
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
                        <div class="px-6 py-4 space-y-1 max-h-[70vh] overflow-y-auto">
                            <label
                                v-for="col in PDF_COLUMNS"
                                :key="col.key"
                                class="flex items-center gap-3 p-2.5 rounded-lg cursor-pointer transition-colors"
                                :class="col.locked ? 'bg-gray-50 cursor-not-allowed opacity-60' : 'hover:bg-gray-50'"
                            >
                                <input
                                    type="checkbox"
                                    v-model="pdfColEnabled[col.key]"
                                    :disabled="col.locked"
                                    class="w-4 h-4 rounded accent-blue-600"
                                />
                                <span class="text-sm text-gray-700">{{ col.label }}</span>
                                <span v-if="col.locked" class="ml-auto text-xs text-gray-400 italic">obligatorio</span>
                            </label>
                        </div>
                        <div class="px-6 pb-5 pt-3 flex items-center justify-between border-t border-gray-100">
                            <span class="text-xs text-gray-400">{{ enabledPdfColCount }} columnas seleccionadas</span>
                            <div class="flex gap-2">
                                <button @click="showPdfConfig = false" class="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-200 rounded-lg">
                                    Cancelar
                                </button>
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

            <!-- ── Panel de filtros ────────────────────────────────────── -->
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

                <!-- Fila 1: Fechas + Oferta -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-3">
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Publicado desde</label>
                        <input type="date" v-model="startDate" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Publicado hasta</label>
                        <input type="date" v-model="endDate" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Tipo</label>
                        <select v-model="tipoFilter" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none">
                            <option value="">Todos los tipos</option>
                            <option value="pasantia">Pasantía</option>
                            <option value="empleo">Empleo</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Estado</label>
                        <select v-model="estadoFilter" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none">
                            <option value="">Todos los estados</option>
                            <option value="activa">Activa</option>
                            <option value="inactiva">Inactiva</option>
                            <option value="expirada">Expirada</option>
                        </select>
                    </div>
                </div>

                <!-- Fila 2: Modalidad + Institución -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-3">
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Modalidad</label>
                        <select v-model="modalidadFilter" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none">
                            <option value="">Todas las modalidades</option>
                            <option value="presencial">Presencial</option>
                            <option value="remoto">Remoto</option>
                            <option value="hibrido">Híbrido</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Sector institucional</label>
                        <input type="text" v-model="sectorFilter" placeholder="Ej: Tecnología, Salud..." class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Institución</label>
                        <input type="text" v-model="institucionFilter" placeholder="Ej: AGETIC, YPFB..." class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Área de la convocatoria</label>
                        <input type="text" v-model="areaFilter" placeholder="Ej: Desarrollo, RRHH..." class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                    </div>
                </div>

                <!-- Fila 3: Filtros por postulantes ── NUEVOS -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 pb-1">
                    <div class="sm:col-span-2 lg:col-span-1">
                        <label class="block text-xs font-medium text-gray-500 mb-1">
                            <span class="text-emi-navy-500">★</span> Con postulaciones
                        </label>
                        <select v-model="conPostulacionesFilter" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none">
                            <option value="">Todas las ofertas</option>
                            <option value="true">Solo con postulaciones</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">
                            <span class="text-emi-navy-500">★</span> Rol postulante
                        </label>
                        <select v-model="rolPostulanteFilter" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none">
                            <option value="">Todos los roles</option>
                            <option value="estudiante">Con estudiantes</option>
                            <option value="titulado">Con titulados</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">
                            <span class="text-emi-navy-500">★</span> Carrera postulante
                        </label>
                        <input type="text" v-model="carreraPostulanteFilter" placeholder="Ej: Sistemas, Civil..." class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">
                            <span class="text-emi-navy-500">★</span> Mín. postulaciones
                        </label>
                        <select v-model="minPostulacionesFilter" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none">
                            <option value="">Sin mínimo</option>
                            <option value="1">≥ 1</option>
                            <option value="5">≥ 5</option>
                            <option value="10">≥ 10</option>
                            <option value="20">≥ 20</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">
                            <span class="text-emi-navy-500">★</span> Score prom. mín.
                        </label>
                        <select v-model="minScoreFilter" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none">
                            <option value="">Sin mínimo</option>
                            <option value="30">≥ 30%</option>
                            <option value="50">≥ 50%</option>
                            <option value="65">≥ 65%</option>
                            <option value="80">≥ 80%</option>
                        </select>
                    </div>
                </div>
                <p class="text-[10px] text-emi-navy-500 mt-2 mb-3">★ Filtros por perfil de postulante</p>

                <div class="flex justify-end border-t border-gray-100 pt-3">
                    <button @click="loadData" :disabled="loading" class="px-5 py-2 bg-emi-navy-600 text-white rounded-lg text-sm hover:bg-emi-navy-700 disabled:opacity-50 font-medium">
                        Aplicar filtros
                    </button>
                </div>
            </div>

            <!-- ── Loading ─────────────────────────────────────────────── -->
            <div v-if="loading" class="bg-white rounded-xl p-12 text-center">
                <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-emi-navy-500 mx-auto"></div>
                <p class="mt-4 text-sm text-gray-400">Cargando reporte...</p>
            </div>

            <!-- ── Error ───────────────────────────────────────────────── -->
            <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
                <p class="text-sm text-red-700">{{ error }}</p>
            </div>

            <!-- ── Contenido del reporte ───────────────────────────────── -->
            <div v-else id="offers-report-container" class="space-y-5">

                <!-- Encabezado PDF -->
                <div v-if="pdfMode" class="bg-emi-navy-700 text-white px-6 py-4 rounded-xl flex items-center justify-between">
                    <div>
                        <p class="text-[10px] text-blue-200 uppercase tracking-widest mb-1">Sistema de Bolsa Laboral — EMI</p>
                        <h1 class="text-xl font-bold">Reporte de Convocatorias Laborales</h1>
                        <p class="text-xs text-blue-100 mt-0.5">Período: {{ formatDate(startDate) }} — {{ formatDate(endDate) }}</p>
                    </div>
                    <div class="text-right text-xs text-blue-100 space-y-1">
                        <p>Generado: {{ formatDate(new Date().toISOString()) }}</p>
                        <p>Total mostrado: <span class="font-bold text-white">{{ reportData?.ofertas?.length }}</span> convocatorias</p>
                    </div>
                </div>

                <!-- ── Fila 1: métricas principales ──────────────────── -->
                <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
                    <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Total convocatorias</p>
                        <p class="text-2xl font-bold text-emi-navy-500 mt-1">{{ reportData?.stats.total }}</p>
                        <div class="flex gap-3 mt-1">
                            <span class="text-[11px] text-green-600">{{ reportData?.stats.activas }} activas</span>
                            <span class="text-[11px] text-red-500">{{ reportData?.stats.expiradas }} exp.</span>
                        </div>
                    </div>
                    <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Postulaciones</p>
                        <p class="text-2xl font-bold text-blue-600 mt-1">{{ reportData?.stats.total_postulaciones }}</p>
                        <p class="text-[11px] text-gray-400">en total</p>
                    </div>
                    <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Estudiantes postulan</p>
                        <p class="text-2xl font-bold text-indigo-600 mt-1">{{ reportData?.stats.postulantes_estudiantes }}</p>
                        <p class="text-[11px] text-gray-400">postulaciones de estudiantes</p>
                    </div>
                    <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Titulados postulan</p>
                        <p class="text-2xl font-bold text-purple-600 mt-1">{{ reportData?.stats.postulantes_titulados }}</p>
                        <p class="text-[11px] text-gray-400">postulaciones de titulados</p>
                    </div>
                </div>

                <!-- ── Fila 2: distribuciones ─────────────────────────── -->
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-2">Por Tipo</p>
                        <div class="flex flex-wrap gap-x-4 gap-y-1">
                            <div v-for="(count, tipo) in reportData?.stats.by_tipo" :key="tipo" class="flex items-center gap-1.5">
                                <span class="text-[11px] capitalize text-gray-600">{{ tipo }}</span>
                                <span class="text-[11px] font-bold bg-gray-100 px-1.5 py-0.5 rounded-full text-gray-700">{{ count }}</span>
                            </div>
                        </div>
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-1 mt-3">Por Modalidad</p>
                        <div class="flex flex-wrap gap-x-4 gap-y-1">
                            <div v-for="(count, mod) in reportData?.stats.by_modalidad" :key="mod" class="flex items-center gap-1.5">
                                <span class="text-[11px] capitalize text-gray-600">{{ mod }}</span>
                                <span class="text-[11px] font-bold bg-gray-100 px-1.5 py-0.5 rounded-full text-gray-700">{{ count }}</span>
                            </div>
                            <p v-if="!Object.keys(reportData?.stats.by_modalidad || {}).length" class="text-[11px] text-gray-300">Sin datos</p>
                        </div>
                    </div>

                    <!-- Score + Rol postulantes -->
                    <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Score Prom. Global</p>
                        <p class="text-2xl font-bold mt-1" :class="scoreText(reportData?.stats.avg_match_score)">
                            {{ reportData?.stats.avg_match_score ? reportData.stats.avg_match_score + '%' : '—' }}
                        </p>
                        <p class="text-[11px] text-gray-400 mb-3">match promedio</p>
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-1">Ratio Estudiantes/Titulados</p>
                        <div v-if="(reportData?.stats.postulantes_estudiantes + reportData?.stats.postulantes_titulados) > 0">
                            <div class="flex gap-1 h-2 rounded-full overflow-hidden mb-1">
                                <div
                                    class="bg-indigo-400 rounded-l-full transition-all"
                                    :style="{ width: (reportData.stats.postulantes_estudiantes / (reportData.stats.postulantes_estudiantes + reportData.stats.postulantes_titulados) * 100) + '%' }"
                                ></div>
                                <div class="flex-1 bg-purple-400 rounded-r-full"></div>
                            </div>
                            <div class="flex justify-between text-[10px]">
                                <span class="text-indigo-600">Est. {{ Math.round(reportData.stats.postulantes_estudiantes / (reportData.stats.postulantes_estudiantes + reportData.stats.postulantes_titulados) * 100) }}%</span>
                                <span class="text-purple-600">Tit. {{ Math.round(reportData.stats.postulantes_titulados / (reportData.stats.postulantes_estudiantes + reportData.stats.postulantes_titulados) * 100) }}%</span>
                            </div>
                        </div>
                        <p v-else class="text-[11px] text-gray-300">Sin postulaciones</p>
                    </div>

                    <!-- Top carreras -->
                    <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-2">Top Carreras Postulantes</p>
                        <div v-if="topCarrerasGlobal.length" class="space-y-1.5">
                            <div v-for="c in topCarrerasGlobal" :key="c.name" class="flex items-center gap-2">
                                <span class="text-[11px] text-gray-600 truncate w-28 shrink-0 capitalize">{{ c.name }}</span>
                                <div class="flex-1 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                                    <div class="h-1.5 bg-emi-navy-400 rounded-full" :style="{ width: c.pct + '%' }"></div>
                                </div>
                                <span class="text-[10px] font-semibold text-gray-600 w-4 text-right shrink-0">{{ c.count }}</span>
                            </div>
                        </div>
                        <p v-else class="text-[11px] text-gray-300">Sin datos de carreras</p>
                    </div>
                </div>

                <!-- ── Tabla ──────────────────────────────────────────── -->
                <div class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
                    <div class="px-5 py-3 border-b border-gray-100 flex items-center gap-2" :class="{ 'hidden': pdfMode }">
                        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                        </svg>
                        <span class="text-sm font-semibold text-gray-700">Listado de convocatorias</span>
                        <span class="text-xs text-gray-400">({{ reportData?.ofertas?.length }} registros)</span>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="min-w-full text-xs">
                            <thead>
                                <tr class="bg-gray-50 border-b border-gray-100">
                                    <th class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide">#</th>
                                    <th class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Convocatoria</th>
                                    <th v-if="colVisible('tipo')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Tipo</th>
                                    <th v-if="colVisible('modalidad')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Modalidad</th>
                                    <th v-if="colVisible('sector')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Sector</th>
                                    <th v-if="colVisible('area')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Área</th>
                                    <th v-if="colVisible('estado')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Estado</th>
                                    <th v-if="colVisible('fechas')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Inicio / Cierre</th>
                                    <th v-if="colVisible('dias_restantes')" class="px-4 py-2.5 text-center font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Días rest.</th>
                                    <th v-if="colVisible('cupos')" class="px-4 py-2.5 text-center font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Cupos</th>
                                    <th v-if="colVisible('postulaciones')" class="px-4 py-2.5 text-center font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Postul.</th>
                                    <th v-if="colVisible('postulantes_rol')" class="px-4 py-2.5 text-center font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Est. / Tit.</th>
                                    <th v-if="colVisible('carreras')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Top carreras</th>
                                    <th v-if="colVisible('score')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Score prom.</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr
                                    v-for="(oferta, idx) in reportData?.ofertas"
                                    :key="oferta.id"
                                    class="border-b border-gray-100 hover:bg-gray-50/60 transition-colors"
                                    :class="idx % 2 === 0 ? '' : 'bg-gray-50/30'"
                                >
                                    <td class="px-4 py-2.5 text-gray-300 font-mono select-none">{{ idx + 1 }}</td>

                                    <td class="px-4 py-2.5 min-w-[180px]">
                                        <p class="font-medium text-gray-800 leading-tight">{{ oferta.titulo }}</p>
                                        <p class="text-gray-400 mt-0.5">{{ oferta.institucion || '—' }}</p>
                                    </td>

                                    <td v-if="colVisible('tipo')" class="px-4 py-2.5">
                                        <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium capitalize" :class="tipoBadge(oferta.tipo)">
                                            {{ oferta.tipo }}
                                        </span>
                                    </td>

                                    <td v-if="colVisible('modalidad')" class="px-4 py-2.5">
                                        <span v-if="oferta.modalidad" class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium capitalize" :class="modalidadBadge(oferta.modalidad)">
                                            {{ oferta.modalidad }}
                                        </span>
                                        <span v-else class="text-gray-300">—</span>
                                    </td>

                                    <td v-if="colVisible('sector')" class="px-4 py-2.5 text-gray-600 whitespace-nowrap">{{ oferta.sector || '—' }}</td>
                                    <td v-if="colVisible('area')" class="px-4 py-2.5 text-gray-600 whitespace-nowrap">{{ oferta.area || '—' }}</td>

                                    <td v-if="colVisible('estado')" class="px-4 py-2.5">
                                        <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium capitalize" :class="estadoBadge(oferta.estado)">
                                            {{ oferta.estado }}
                                        </span>
                                    </td>

                                    <td v-if="colVisible('fechas')" class="px-4 py-2.5 whitespace-nowrap">
                                        <p class="text-gray-500">{{ formatDate(oferta.fecha_inicio) }}</p>
                                        <p class="text-gray-400 mt-0.5">→ {{ formatDate(oferta.fecha_cierre) }}</p>
                                    </td>

                                    <td v-if="colVisible('dias_restantes')" class="px-4 py-2.5 text-center whitespace-nowrap">
                                        <span v-if="oferta.dias_restantes !== null && oferta.dias_restantes !== undefined" :class="diasColor(oferta.dias_restantes)">
                                            {{ oferta.dias_restantes }}d
                                        </span>
                                        <span v-else class="text-gray-300">—</span>
                                    </td>

                                    <td v-if="colVisible('cupos')" class="px-4 py-2.5 text-center font-medium text-gray-700">
                                        {{ oferta.cupos_disponibles }}
                                    </td>

                                    <td v-if="colVisible('postulaciones')" class="px-4 py-2.5 text-center">
                                        <span v-if="oferta.total_postulaciones > 0" class="font-semibold text-blue-600">
                                            {{ oferta.total_postulaciones }}
                                        </span>
                                        <span v-else class="text-gray-300">0</span>
                                        <div v-if="oferta.total_postulaciones > 0" class="text-[10px] text-gray-400 mt-0.5 leading-none">
                                            {{ oferta.aptos }}A · {{ oferta.considerados }}C · {{ oferta.no_aptos }}N
                                        </div>
                                    </td>

                                    <!-- Nueva col: Est. vs Tit. -->
                                    <td v-if="colVisible('postulantes_rol')" class="px-4 py-2.5 text-center whitespace-nowrap">
                                        <div v-if="oferta.total_postulaciones > 0" class="space-y-0.5">
                                            <p class="text-indigo-600 font-medium">{{ oferta.postulantes_estudiantes }}<span class="text-[10px] font-normal text-gray-400"> est.</span></p>
                                            <p class="text-purple-600 font-medium">{{ oferta.postulantes_titulados }}<span class="text-[10px] font-normal text-gray-400"> tit.</span></p>
                                        </div>
                                        <span v-else class="text-gray-300">—</span>
                                    </td>

                                    <!-- Nueva col: Top carreras -->
                                    <td v-if="colVisible('carreras')" class="px-4 py-2.5 min-w-[130px]">
                                        <div v-if="oferta.top_carreras?.length" class="space-y-0.5">
                                            <p v-for="c in oferta.top_carreras" :key="c" class="text-[11px] text-gray-600 capitalize leading-tight truncate max-w-[120px]">· {{ c }}</p>
                                        </div>
                                        <span v-else class="text-gray-300">—</span>
                                    </td>

                                    <td v-if="colVisible('score')" class="px-4 py-2.5 min-w-[110px]">
                                        <div v-if="oferta.avg_match_score !== null" class="flex items-center gap-2">
                                            <div class="flex-1 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                                                <div class="h-1.5 rounded-full" :class="scoreBar(oferta.avg_match_score)" :style="{ width: oferta.avg_match_score + '%' }"></div>
                                            </div>
                                            <span class="text-[11px] font-semibold w-8 text-right shrink-0" :class="scoreText(oferta.avg_match_score)">
                                                {{ oferta.avg_match_score }}%
                                            </span>
                                        </div>
                                        <span v-else class="text-gray-300">—</span>
                                    </td>
                                </tr>

                                <tr v-if="!reportData?.ofertas?.length">
                                    <td colspan="15" class="px-4 py-10 text-center text-gray-400 text-sm">
                                        No se encontraron convocatorias con los filtros seleccionados.
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
            <!-- TAB 2: Cumplimiento por Convocatoria                      -->
            <!-- ══════════════════════════════════════════════════════════ -->
            <template v-if="activeTab === 'cumplimiento' || compPdfMode">

                <!-- Modal PDF compliance -->
                <Teleport to="body">
                    <div v-if="compShowPdfConfig" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
                        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4">
                            <div class="px-6 pt-5 pb-4 border-b border-gray-100 flex items-center justify-between">
                                <div>
                                    <h2 class="text-base font-semibold text-gray-800">Configurar exportación PDF</h2>
                                    <p class="text-xs text-gray-400 mt-0.5">Selecciona las columnas que aparecerán en el PDF</p>
                                </div>
                                <button @click="compShowPdfConfig = false" class="text-gray-400 hover:text-gray-600 p-1">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                                    </svg>
                                </button>
                            </div>
                            <div class="px-6 py-4 space-y-1">
                                <label v-for="col in COMP_PDF_COLUMNS" :key="col.key"
                                    class="flex items-center gap-3 p-2.5 rounded-lg cursor-pointer"
                                    :class="col.locked ? 'bg-gray-50 cursor-not-allowed opacity-60' : 'hover:bg-gray-50'"
                                >
                                    <input type="checkbox" v-model="compPdfColEnabled[col.key]" :disabled="col.locked" class="w-4 h-4 rounded accent-blue-600" />
                                    <span class="text-sm text-gray-700">{{ col.label }}</span>
                                    <span v-if="col.locked" class="ml-auto text-xs text-gray-400 italic">obligatorio</span>
                                </label>
                            </div>
                            <div class="px-6 pb-5 pt-3 flex items-center justify-between border-t border-gray-100">
                                <span class="text-xs text-gray-400">{{ compEnabledPdfColCount }} columnas seleccionadas</span>
                                <div class="flex gap-2">
                                    <button @click="compShowPdfConfig = false" class="px-4 py-2 text-sm text-gray-600 border border-gray-200 rounded-lg hover:text-gray-800">Cancelar</button>
                                    <button @click="confirmAndGenerateCompPDF" class="px-5 py-2 text-sm bg-emi-navy-600 text-white rounded-lg hover:bg-emi-navy-700 font-medium">Generar PDF</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </Teleport>

                <!-- Filtros compliance -->
                <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-200 mb-6" :class="{ 'hidden': compPdfMode }">
                    <div class="flex items-center justify-between mb-4">
                        <h2 class="text-sm font-semibold text-gray-700 inline-flex items-center gap-2">
                            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2a1 1 0 01-.293.707L13 13.414V19a1 1 0 01-.553.894l-4 2A1 1 0 017 21v-7.586L3.293 6.707A1 1 0 013 6V4z"/>
                            </svg>
                            Filtros
                            <span v-if="compActiveFiltersCount > 0" class="bg-emi-navy-100 text-emi-navy-700 text-xs font-bold px-2 py-0.5 rounded-full">
                                {{ compActiveFiltersCount }} activos
                            </span>
                        </h2>
                        <button @click="resetCompFilters" class="text-xs text-gray-400 hover:text-gray-600 underline">Limpiar todo</button>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 mb-3">
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Publicado desde</label>
                            <input type="date" v-model="compStartDate" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Publicado hasta</label>
                            <input type="date" v-model="compEndDate" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Institución</label>
                            <input type="text" v-model="compInstitucionFilter" placeholder="Ej: AGETIC, YPFB..." class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Tipo de institución</label>
                            <select v-model="compTipoInstFilter" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none">
                                <option value="">Todos los tipos</option>
                                <option value="Pública">Pública</option>
                                <option value="Privada">Privada</option>
                                <option value="Mixta">Mixta</option>
                                <option value="ONG">ONG</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Tipo de oferta</label>
                            <select v-model="compTipoFilter" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none">
                                <option value="">Todos los tipos</option>
                                <option value="pasantia">Pasantía</option>
                                <option value="empleo">Empleo</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-gray-500 mb-1">Estado</label>
                            <select v-model="compEstadoFilter" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none">
                                <option value="">Todos los estados</option>
                                <option value="activa">Activa</option>
                                <option value="inactiva">Inactiva</option>
                                <option value="expirada">Expirada</option>
                            </select>
                        </div>
                    </div>
                    <div class="mt-4 flex justify-end">
                        <button @click="loadCompliance" :disabled="compLoading" class="px-5 py-2 bg-emi-navy-600 text-white rounded-lg text-sm hover:bg-emi-navy-700 disabled:opacity-50 font-medium">
                            Aplicar filtros
                        </button>
                    </div>
                </div>

                <!-- Loading compliance -->
                <div v-if="compLoading" class="bg-white rounded-xl p-12 text-center">
                    <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-emi-navy-500 mx-auto"></div>
                    <p class="mt-4 text-sm text-gray-400">Cargando reporte de cumplimiento...</p>
                </div>

                <!-- Error compliance -->
                <div v-else-if="compError" class="bg-red-50 border border-red-200 rounded-lg p-4">
                    <p class="text-sm text-red-700">{{ compError }}</p>
                </div>

                <!-- Contenido compliance -->
                <div v-else-if="compLoaded" id="compliance-report-container" class="space-y-5">

                    <!-- Encabezado PDF -->
                    <div v-if="compPdfMode" class="bg-emi-navy-700 text-white px-6 py-4 rounded-xl flex items-center justify-between">
                        <div>
                            <p class="text-[10px] text-blue-200 uppercase tracking-widest mb-1">Sistema de Bolsa Laboral — EMI</p>
                            <h1 class="text-xl font-bold">Reporte de Cumplimiento por Convocatoria</h1>
                            <p class="text-xs text-blue-100 mt-0.5">Período: {{ formatDate(compStartDate) }} — {{ formatDate(compEndDate) }}</p>
                        </div>
                        <div class="text-right text-xs text-blue-100 space-y-1">
                            <p>Generado: {{ formatDate(new Date().toISOString()) }}</p>
                            <p>Total: <span class="font-bold text-white">{{ compData?.convocatorias?.length }}</span> convocatorias</p>
                        </div>
                    </div>

                    <!-- Tarjetas resumen -->
                    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
                        <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                            <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Convocatorias</p>
                            <p class="text-2xl font-bold text-emi-navy-500 mt-1">{{ compData?.stats.total }}</p>
                            <p class="text-[11px] text-gray-400">en el período</p>
                        </div>
                        <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                            <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Cupos totales</p>
                            <p class="text-2xl font-bold text-blue-600 mt-1">{{ compData?.stats.total_cupos }}</p>
                            <p class="text-[11px] text-gray-400">disponibles</p>
                        </div>
                        <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                            <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Aptos totales</p>
                            <p class="text-2xl font-bold text-green-600 mt-1">{{ compData?.stats.total_aptos }}</p>
                            <p class="text-[11px] text-gray-400">postulantes APTOS</p>
                        </div>
                        <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                            <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Cumplimiento global</p>
                            <p class="text-2xl font-bold mt-1" :class="cumplimientoText(compData?.stats.pct_cumplimiento_global)">
                                {{ compData?.stats.pct_cumplimiento_global }}%
                            </p>
                            <p class="text-[11px] text-gray-400">aptos / cupos total</p>
                        </div>
                    </div>

                    <!-- Por tipo institución -->
                    <div v-if="Object.keys(compData?.stats.by_tipo_institucion || {}).length" class="bg-white px-5 py-4 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-3">Convocatorias por Tipo de Institución</p>
                        <div class="flex flex-wrap gap-2">
                            <div v-for="(count, tipo) in compData?.stats.by_tipo_institucion" :key="tipo"
                                class="flex items-center gap-2 px-3 py-1.5 rounded-lg"
                                :class="tipoBadgeInst(tipo)"
                            >
                                <span class="text-xs font-semibold">{{ tipo }}</span>
                                <span class="text-xs font-bold bg-white/50 px-1.5 py-0.5 rounded-full">{{ count }}</span>
                            </div>
                        </div>
                    </div>

                    <!-- Tabla cumplimiento -->
                    <div class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
                        <div class="px-5 py-3 border-b border-gray-100 flex items-center gap-2" :class="{ 'hidden': compPdfMode }">
                            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                            </svg>
                            <span class="text-sm font-semibold text-gray-700">Detalle por convocatoria</span>
                            <span class="text-xs text-gray-400">(ordenado por menor cumplimiento)</span>
                        </div>
                        <div class="overflow-x-auto">
                            <table class="min-w-full text-xs">
                                <thead>
                                    <tr class="bg-gray-50 border-b border-gray-100">
                                        <th class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide">#</th>
                                        <th class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Convocatoria</th>
                                        <th v-if="compColVisible('tipo_inst')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Tipo inst.</th>
                                        <th v-if="compColVisible('tipo')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Tipo</th>
                                        <th v-if="compColVisible('estado')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Estado</th>
                                        <th v-if="compColVisible('fechas')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Inicio / Cierre</th>
                                        <th v-if="compColVisible('cupos')" class="px-4 py-2.5 text-center font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Cupos</th>
                                        <th v-if="compColVisible('postulaciones')" class="px-4 py-2.5 text-center font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Postul.</th>
                                        <th v-if="compColVisible('cumplimiento')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">% Cumplimiento</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr
                                        v-for="(conv, idx) in convocatoriasOrdenadas"
                                        :key="conv.id"
                                        class="border-b border-gray-100 hover:bg-gray-50/60 transition-colors"
                                        :class="idx % 2 === 0 ? '' : 'bg-gray-50/30'"
                                    >
                                        <td class="px-4 py-2.5 text-gray-300 font-mono select-none">{{ idx + 1 }}</td>
                                        <td class="px-4 py-2.5 min-w-[200px]">
                                            <p class="font-medium text-gray-800 leading-tight">{{ conv.titulo }}</p>
                                            <p class="text-gray-400 mt-0.5">{{ conv.institucion || '—' }}</p>
                                        </td>
                                        <td v-if="compColVisible('tipo_inst')" class="px-4 py-2.5">
                                            <span v-if="conv.tipo_institucion" class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium" :class="tipoBadgeInst(conv.tipo_institucion)">
                                                {{ conv.tipo_institucion }}
                                            </span>
                                            <span v-else class="text-gray-300">—</span>
                                        </td>
                                        <td v-if="compColVisible('tipo')" class="px-4 py-2.5">
                                            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium capitalize"
                                                :class="conv.tipo === 'pasantia' ? 'bg-blue-100 text-blue-700 border border-blue-200' : 'bg-purple-100 text-purple-700 border border-purple-200'"
                                            >{{ conv.tipo }}</span>
                                        </td>
                                        <td v-if="compColVisible('estado')" class="px-4 py-2.5">
                                            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium capitalize" :class="estadoBadge(conv.estado)">
                                                {{ conv.estado }}
                                            </span>
                                        </td>
                                        <td v-if="compColVisible('fechas')" class="px-4 py-2.5 whitespace-nowrap">
                                            <p class="text-gray-500">{{ formatDate(conv.fecha_inicio) }}</p>
                                            <p class="text-gray-400 mt-0.5">→ {{ formatDate(conv.fecha_cierre) }}</p>
                                        </td>
                                        <td v-if="compColVisible('cupos')" class="px-4 py-2.5 text-center font-semibold text-gray-700">{{ conv.cupos_disponibles }}</td>
                                        <td v-if="compColVisible('postulaciones')" class="px-4 py-2.5 text-center">
                                            <span class="font-semibold text-blue-600">{{ conv.total_postulaciones }}</span>
                                            <div v-if="conv.total_postulaciones > 0" class="text-[10px] text-gray-400 mt-0.5">
                                                {{ conv.aptos }}A · {{ conv.considerados }}C · {{ conv.no_aptos }}N
                                            </div>
                                        </td>
                                        <td v-if="compColVisible('cumplimiento')" class="px-4 py-2.5 min-w-[130px]">
                                            <div class="flex items-center gap-2">
                                                <div class="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                                                    <div class="h-2 rounded-full transition-all" :class="cumplimientoColor(conv.pct_cumplimiento)" :style="{ width: conv.pct_cumplimiento + '%' }"></div>
                                                </div>
                                                <span class="text-xs w-10 text-right shrink-0" :class="cumplimientoText(conv.pct_cumplimiento)">{{ conv.pct_cumplimiento }}%</span>
                                            </div>
                                            <p class="text-[10px] text-gray-400 mt-0.5">{{ conv.aptos }} apto{{ conv.aptos !== 1 ? 's' : '' }} / {{ conv.cupos_disponibles }} cupo{{ conv.cupos_disponibles !== 1 ? 's' : '' }}</p>
                                        </td>
                                    </tr>
                                    <tr v-if="!compData?.convocatorias?.length">
                                        <td colspan="9" class="px-4 py-10 text-center text-gray-400 text-sm">
                                            No se encontraron convocatorias con los filtros seleccionados.
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Pie PDF -->
                    <div v-if="compPdfMode" class="text-center text-[10px] text-gray-400 pt-1">
                        Reporte generado automáticamente — Sistema de Bolsa Laboral EMI
                    </div>
                </div>
            </template>

        </div>
    </AppLayout>
</template>
