<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/features/auth/store/auth.store'
import axios from 'axios'
import html2pdf from 'html2pdf.js'
import AppLayout from '@/shared/components/AppLayout.vue'

const authStore = useAuthStore()
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

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
    { key: 'oferta',             label: 'Oferta (Título + Institución)',   locked: true },
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
        error.value = 'Error al cargar el reporte de ofertas.'
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
</script>

<template>
    <AppLayout>
        <div class="py-6 px-4 sm:px-6 lg:px-8 min-w-0">

            <!-- ── Header ──────────────────────────────────────────────── -->
            <header class="mb-6" :class="{ 'hidden': pdfMode }">
                <div class="flex flex-col xl:flex-row xl:items-center justify-between gap-4">
                    <div>
                        <h1 class="text-2xl font-bold text-emi-navy-500">Reporte de Ofertas</h1>
                        <p class="mt-0.5 text-sm text-gray-500">Detalle de ofertas laborales con segmentación por postulante.</p>
                    </div>
                    <button
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
                </div>
            </header>

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
                        <label class="block text-xs font-medium text-gray-500 mb-1">Área de la oferta</label>
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
                        <h1 class="text-xl font-bold">Reporte de Ofertas Laborales</h1>
                        <p class="text-xs text-blue-100 mt-0.5">Período: {{ formatDate(startDate) }} — {{ formatDate(endDate) }}</p>
                    </div>
                    <div class="text-right text-xs text-blue-100 space-y-1">
                        <p>Generado: {{ formatDate(new Date().toISOString()) }}</p>
                        <p>Total mostrado: <span class="font-bold text-white">{{ reportData?.ofertas?.length }}</span> ofertas</p>
                    </div>
                </div>

                <!-- ── Fila 1: métricas principales ──────────────────── -->
                <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
                    <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Total ofertas</p>
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
                        <span class="text-sm font-semibold text-gray-700">Listado de ofertas</span>
                        <span class="text-xs text-gray-400">({{ reportData?.ofertas?.length }} registros)</span>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="min-w-full text-xs">
                            <thead>
                                <tr class="bg-gray-50 border-b border-gray-100">
                                    <th class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide">#</th>
                                    <th class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Oferta</th>
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
                                        No se encontraron ofertas con los filtros seleccionados.
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
        </div>
    </AppLayout>
</template>
