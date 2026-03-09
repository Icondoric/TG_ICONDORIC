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

// Filtros
const startDate = ref('')
const endDate = ref('')
const tipoFilter = ref('')
const tipoInstFilter = ref('')
const estadoFilter = ref('')
const institucionFilter = ref('')

const reportData = ref(null)

const PDF_COLUMNS = [
    { key: 'convocatoria', label: 'Convocatoria (Título + Institución)', locked: true },
    { key: 'tipo_inst',    label: 'Tipo de institución' },
    { key: 'tipo',         label: 'Tipo (Pasantía / Empleo)' },
    { key: 'estado',       label: 'Estado' },
    { key: 'fechas',       label: 'Fechas (Inicio / Cierre)' },
    { key: 'cupos',        label: 'Cupos disponibles' },
    { key: 'postulaciones',label: 'Postulaciones (Total / A-C-N)' },
    { key: 'cumplimiento', label: '% Cumplimiento', locked: true },
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
            tipo_institucion: tipoInstFilter.value || undefined,
            estado: estadoFilter.value || undefined,
            institucion: institucionFilter.value || undefined,
        }
        const res = await axios.get(`${API_URL}/api/analytics/compliance-report`, { headers, params })
        reportData.value = res.data
    } catch (err) {
        console.error('Error loading compliance report:', err)
        error.value = 'Error al cargar el reporte de cumplimiento.'
    } finally {
        loading.value = false
    }
}

const resetFilters = () => {
    tipoFilter.value = ''
    tipoInstFilter.value = ''
    estadoFilter.value = ''
    institucionFilter.value = ''
    const end = new Date()
    const start = new Date()
    start.setDate(end.getDate() - 90)
    endDate.value = end.toISOString().split('T')[0]
    startDate.value = start.toISOString().split('T')[0]
    loadData()
}

const confirmAndGeneratePDF = async () => {
    showPdfConfig.value = false
    generatingPdf.value = true
    pdfMode.value = true
    await new Promise(r => setTimeout(r, 150))
    const element = document.getElementById('compliance-report-container')
    const opt = {
        margin: [12, 8, 12, 8],
        filename: `reporte-cumplimiento-${startDate.value}_${endDate.value}.pdf`,
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

const tipoBadge = (tipo) => {
    const map = {
        'Pública':  'bg-blue-100 text-blue-700 border border-blue-200',
        'Privada':  'bg-purple-100 text-purple-700 border border-purple-200',
        'Mixta':    'bg-teal-100 text-teal-700 border border-teal-200',
        'ONG':      'bg-orange-100 text-orange-700 border border-orange-200',
    }
    return map[tipo] || 'bg-gray-100 text-gray-600 border border-gray-200'
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

const activeFiltersCount = computed(() => {
    let n = 0
    if (tipoFilter.value) n++
    if (tipoInstFilter.value) n++
    if (estadoFilter.value) n++
    if (institucionFilter.value) n++
    return n
})

const enabledPdfColCount = computed(() =>
    PDF_COLUMNS.filter(c => pdfColEnabled.value[c.key]).length
)

// Sorted by % cumplimiento asc (menor primero para ver los que más necesitan atención)
const convocatoriasOrdenadas = computed(() => {
    return [...(reportData.value?.convocatorias || [])].sort((a, b) => a.pct_cumplimiento - b.pct_cumplimiento)
})
</script>

<template>
    <AppLayout>
        <div class="py-6 px-4 sm:px-6 lg:px-8 min-w-0">

            <!-- ── Header ──────────────────────────────────────────────── -->
            <header class="mb-6" :class="{ 'hidden': pdfMode }">
                <div class="flex flex-col xl:flex-row xl:items-center justify-between gap-4">
                    <div>
                        <h1 class="text-2xl font-bold text-emi-navy-500">Cumplimiento por Convocatoria</h1>
                        <p class="mt-0.5 text-sm text-gray-500">% de cupos cubiertos con postulantes APTOS por oferta.</p>
                    </div>
                    <button
                        @click="showPdfConfig = true"
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

            <!-- ── Modal PDF ───────────────────────────────────────────── -->
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
                        <div class="px-6 py-4 space-y-1">
                            <label v-for="col in PDF_COLUMNS" :key="col.key"
                                class="flex items-center gap-3 p-2.5 rounded-lg cursor-pointer"
                                :class="col.locked ? 'bg-gray-50 cursor-not-allowed opacity-60' : 'hover:bg-gray-50'"
                            >
                                <input type="checkbox" v-model="pdfColEnabled[col.key]" :disabled="col.locked" class="w-4 h-4 rounded accent-blue-600" />
                                <span class="text-sm text-gray-700">{{ col.label }}</span>
                                <span v-if="col.locked" class="ml-auto text-xs text-gray-400 italic">obligatorio</span>
                            </label>
                        </div>
                        <div class="px-6 pb-5 pt-3 flex items-center justify-between border-t border-gray-100">
                            <span class="text-xs text-gray-400">{{ enabledPdfColCount }} columnas seleccionadas</span>
                            <div class="flex gap-2">
                                <button @click="showPdfConfig = false" class="px-4 py-2 text-sm text-gray-600 border border-gray-200 rounded-lg hover:text-gray-800">Cancelar</button>
                                <button @click="confirmAndGeneratePDF" class="px-5 py-2 text-sm bg-emi-navy-600 text-white rounded-lg hover:bg-emi-navy-700 font-medium">
                                    Generar PDF
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </Teleport>

            <!-- ── Filtros ─────────────────────────────────────────────── -->
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
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 mb-3">
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Publicado desde</label>
                        <input type="date" v-model="startDate" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Publicado hasta</label>
                        <input type="date" v-model="endDate" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Institución</label>
                        <input type="text" v-model="institucionFilter" placeholder="Ej: AGETIC, YPFB..." class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                    </div>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Tipo de institución</label>
                        <select v-model="tipoInstFilter" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none">
                            <option value="">Todos los tipos</option>
                            <option value="Pública">Pública</option>
                            <option value="Privada">Privada</option>
                            <option value="Mixta">Mixta</option>
                            <option value="ONG">ONG</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Tipo de oferta</label>
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
                <div class="mt-4 flex justify-end">
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

            <!-- ── Contenido ───────────────────────────────────────────── -->
            <div v-else id="compliance-report-container" class="space-y-5">

                <!-- Encabezado PDF -->
                <div v-if="pdfMode" class="bg-emi-navy-700 text-white px-6 py-4 rounded-xl flex items-center justify-between">
                    <div>
                        <p class="text-[10px] text-blue-200 uppercase tracking-widest mb-1">Sistema de Bolsa Laboral — EMI</p>
                        <h1 class="text-xl font-bold">Reporte de Cumplimiento por Convocatoria</h1>
                        <p class="text-xs text-blue-100 mt-0.5">Período: {{ formatDate(startDate) }} — {{ formatDate(endDate) }}</p>
                    </div>
                    <div class="text-right text-xs text-blue-100 space-y-1">
                        <p>Generado: {{ formatDate(new Date().toISOString()) }}</p>
                        <p>Total: <span class="font-bold text-white">{{ reportData?.convocatorias?.length }}</span> convocatorias</p>
                    </div>
                </div>

                <!-- Tarjetas resumen -->
                <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
                    <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Convocatorias</p>
                        <p class="text-2xl font-bold text-emi-navy-500 mt-1">{{ reportData?.stats.total }}</p>
                        <p class="text-[11px] text-gray-400">en el período</p>
                    </div>
                    <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Cupos totales</p>
                        <p class="text-2xl font-bold text-blue-600 mt-1">{{ reportData?.stats.total_cupos }}</p>
                        <p class="text-[11px] text-gray-400">disponibles</p>
                    </div>
                    <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Aptos totales</p>
                        <p class="text-2xl font-bold text-green-600 mt-1">{{ reportData?.stats.total_aptos }}</p>
                        <p class="text-[11px] text-gray-400">postulantes APTOS</p>
                    </div>
                    <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Cumplimiento global</p>
                        <p class="text-2xl font-bold mt-1" :class="cumplimientoText(reportData?.stats.pct_cumplimiento_global)">
                            {{ reportData?.stats.pct_cumplimiento_global }}%
                        </p>
                        <p class="text-[11px] text-gray-400">aptos / cupos total</p>
                    </div>
                </div>

                <!-- Distribución por tipo institución -->
                <div v-if="Object.keys(reportData?.stats.by_tipo_institucion || {}).length" class="bg-white px-5 py-4 rounded-xl border border-gray-100 shadow-sm">
                    <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-3">Convocatorias por Tipo de Institución</p>
                    <div class="flex flex-wrap gap-2">
                        <div v-for="(count, tipo) in reportData?.stats.by_tipo_institucion" :key="tipo"
                            class="flex items-center gap-2 px-3 py-1.5 rounded-lg"
                            :class="tipoBadge(tipo)"
                        >
                            <span class="text-xs font-semibold">{{ tipo }}</span>
                            <span class="text-xs font-bold bg-white/50 px-1.5 py-0.5 rounded-full">{{ count }}</span>
                        </div>
                    </div>
                </div>

                <!-- Tabla -->
                <div class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
                    <div class="px-5 py-3 border-b border-gray-100 flex items-center gap-2" :class="{ 'hidden': pdfMode }">
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
                                    <th v-if="colVisible('tipo_inst')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Tipo inst.</th>
                                    <th v-if="colVisible('tipo')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Tipo</th>
                                    <th v-if="colVisible('estado')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Estado</th>
                                    <th v-if="colVisible('fechas')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Inicio / Cierre</th>
                                    <th v-if="colVisible('cupos')" class="px-4 py-2.5 text-center font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Cupos</th>
                                    <th v-if="colVisible('postulaciones')" class="px-4 py-2.5 text-center font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Postul.</th>
                                    <th v-if="colVisible('cumplimiento')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">% Cumplimiento</th>
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

                                    <td v-if="colVisible('tipo_inst')" class="px-4 py-2.5">
                                        <span v-if="conv.tipo_institucion"
                                            class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium"
                                            :class="tipoBadge(conv.tipo_institucion)"
                                        >
                                            {{ conv.tipo_institucion }}
                                        </span>
                                        <span v-else class="text-gray-300">—</span>
                                    </td>

                                    <td v-if="colVisible('tipo')" class="px-4 py-2.5">
                                        <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium capitalize"
                                            :class="conv.tipo === 'pasantia' ? 'bg-blue-100 text-blue-700 border border-blue-200' : 'bg-purple-100 text-purple-700 border border-purple-200'"
                                        >
                                            {{ conv.tipo }}
                                        </span>
                                    </td>

                                    <td v-if="colVisible('estado')" class="px-4 py-2.5">
                                        <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium capitalize" :class="estadoBadge(conv.estado)">
                                            {{ conv.estado }}
                                        </span>
                                    </td>

                                    <td v-if="colVisible('fechas')" class="px-4 py-2.5 whitespace-nowrap">
                                        <p class="text-gray-500">{{ formatDate(conv.fecha_inicio) }}</p>
                                        <p class="text-gray-400 mt-0.5">→ {{ formatDate(conv.fecha_cierre) }}</p>
                                    </td>

                                    <td v-if="colVisible('cupos')" class="px-4 py-2.5 text-center font-semibold text-gray-700">
                                        {{ conv.cupos_disponibles }}
                                    </td>

                                    <td v-if="colVisible('postulaciones')" class="px-4 py-2.5 text-center">
                                        <span class="font-semibold text-blue-600">{{ conv.total_postulaciones }}</span>
                                        <div v-if="conv.total_postulaciones > 0" class="text-[10px] text-gray-400 mt-0.5">
                                            {{ conv.aptos }}A · {{ conv.considerados }}C · {{ conv.no_aptos }}N
                                        </div>
                                    </td>

                                    <td v-if="colVisible('cumplimiento')" class="px-4 py-2.5 min-w-[130px]">
                                        <div class="flex items-center gap-2">
                                            <div class="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                                                <div class="h-2 rounded-full transition-all" :class="cumplimientoColor(conv.pct_cumplimiento)" :style="{ width: conv.pct_cumplimiento + '%' }"></div>
                                            </div>
                                            <span class="text-xs w-10 text-right shrink-0" :class="cumplimientoText(conv.pct_cumplimiento)">
                                                {{ conv.pct_cumplimiento }}%
                                            </span>
                                        </div>
                                        <p class="text-[10px] text-gray-400 mt-0.5">{{ conv.aptos }} apto{{ conv.aptos !== 1 ? 's' : '' }} / {{ conv.cupos_disponibles }} cupo{{ conv.cupos_disponibles !== 1 ? 's' : '' }}</p>
                                    </td>
                                </tr>
                                <tr v-if="!reportData?.convocatorias?.length">
                                    <td colspan="9" class="px-4 py-10 text-center text-gray-400 text-sm">
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
        </div>
    </AppLayout>
</template>
