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

// Filtros
const startDate = ref('')
const endDate = ref('')
const tipoFilter = ref('')
const tipoInstFilter = ref('')

const reportData = ref(null)

// Vista activa: 'resumen' | 'detalle'
const activeTab = ref('resumen')

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
        }
        const res = await axios.get(`${API_URL}/api/analytics/positions-by-sector`, { headers, params })
        reportData.value = res.data
    } catch (err) {
        console.error('Error loading positions report:', err)
        error.value = 'Error al cargar el reporte de cargos.'
    } finally {
        loading.value = false
    }
}

const resetFilters = () => {
    tipoFilter.value = ''
    tipoInstFilter.value = ''
    const end = new Date()
    const start = new Date()
    start.setDate(end.getDate() - 90)
    endDate.value = end.toISOString().split('T')[0]
    startDate.value = start.toISOString().split('T')[0]
    loadData()
}

const generatePDF = async () => {
    generatingPdf.value = true
    pdfMode.value = true
    await new Promise(r => setTimeout(r, 150))
    const element = document.getElementById('positions-report-container')
    const opt = {
        margin: [12, 8, 12, 8],
        filename: `reporte-cargos-${startDate.value}_${endDate.value}.pdf`,
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

const tipoBadge = (tipo) => {
    const map = {
        'Pública':       'bg-blue-100 text-blue-700 border border-blue-200',
        'Privada':       'bg-purple-100 text-purple-700 border border-purple-200',
        'Mixta':         'bg-teal-100 text-teal-700 border border-teal-200',
        'ONG':           'bg-orange-100 text-orange-700 border border-orange-200',
        'Sin clasificar':'bg-gray-100 text-gray-600 border border-gray-200',
    }
    return map[tipo] || 'bg-gray-100 text-gray-600 border border-gray-200'
}

const tipoInstColor = (tipo) => {
    const map = {
        'Pública': 'bg-blue-500',
        'Privada': 'bg-purple-500',
        'Mixta':   'bg-teal-500',
        'ONG':     'bg-orange-500',
    }
    return map[tipo] || 'bg-gray-400'
}

const activeFiltersCount = computed(() => {
    let n = 0
    if (tipoFilter.value) n++
    if (tipoInstFilter.value) n++
    return n
})

// Tipos de institución presentes en el summary, ordenados por total
const tiposOrdenados = computed(() => {
    const s = reportData.value?.summary_by_tipo || {}
    return Object.entries(s)
        .sort(([, a], [, b]) => b.total_ofertas - a.total_ofertas)
})

// Posiciones filtradas por tipo seleccionado en el detalle
const posicionesFiltradas = computed(() => {
    const pos = reportData.value?.posiciones || []
    if (!tipoInstFilter.value) return pos
    return pos.filter(p => p.tipo_institucion === tipoInstFilter.value)
})
</script>

<template>
    <AppLayout>
        <div class="py-6 px-4 sm:px-6 lg:px-8 min-w-0">

            <!-- ── Header ──────────────────────────────────────────────── -->
            <header class="mb-6" :class="{ 'hidden': pdfMode }">
                <div class="flex flex-col xl:flex-row xl:items-center justify-between gap-4">
                    <div>
                        <h1 class="text-2xl font-bold text-emi-navy-500">Cargos por Tipo de Institución</h1>
                        <p class="mt-0.5 text-sm text-gray-500">Qué cargos publicaron las instituciones públicas, privadas y otras.</p>
                    </div>
                    <button
                        @click="generatePDF"
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
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Publicado desde</label>
                        <input type="date" v-model="startDate" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Publicado hasta</label>
                        <input type="date" v-model="endDate" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                    </div>
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
                            <option value="">Todos</option>
                            <option value="pasantia">Pasantía</option>
                            <option value="empleo">Empleo</option>
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
            <div v-else id="positions-report-container" class="space-y-5">

                <!-- Encabezado PDF -->
                <div v-if="pdfMode" class="bg-emi-navy-700 text-white px-6 py-4 rounded-xl flex items-center justify-between">
                    <div>
                        <p class="text-[10px] text-blue-200 uppercase tracking-widest mb-1">Sistema de Bolsa Laboral — EMI</p>
                        <h1 class="text-xl font-bold">Cargos por Tipo de Institución</h1>
                        <p class="text-xs text-blue-100 mt-0.5">Período: {{ formatDate(startDate) }} — {{ formatDate(endDate) }}</p>
                    </div>
                    <div class="text-right text-xs text-blue-100 space-y-1">
                        <p>Generado: {{ formatDate(new Date().toISOString()) }}</p>
                        <p>Total: <span class="font-bold text-white">{{ reportData?.stats.total }}</span> cargos</p>
                    </div>
                </div>

                <!-- Tarjeta total -->
                <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
                    <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Total cargos</p>
                        <p class="text-2xl font-bold text-emi-navy-500 mt-1">{{ reportData?.stats.total }}</p>
                        <p class="text-[11px] text-gray-400">en el período</p>
                    </div>
                    <div v-for="(count, tipo) in reportData?.stats.by_tipo_institucion" :key="tipo"
                        class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm"
                    >
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">{{ tipo }}</p>
                        <p class="text-2xl font-bold mt-1 text-emi-navy-500">{{ count }}</p>
                        <p class="text-[11px] text-gray-400">cargos publicados</p>
                    </div>
                </div>

                <!-- Tabs de vista -->
                <div class="flex border-b border-gray-200" :class="{ 'hidden': pdfMode }">
                    <button @click="activeTab = 'resumen'"
                        class="px-4 py-2.5 text-sm font-medium border-b-2 transition-colors"
                        :class="activeTab === 'resumen' ? 'border-emi-navy-600 text-emi-navy-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                    >
                        Resumen por tipo
                    </button>
                    <button @click="activeTab = 'detalle'"
                        class="px-4 py-2.5 text-sm font-medium border-b-2 transition-colors"
                        :class="activeTab === 'detalle' ? 'border-emi-navy-600 text-emi-navy-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
                    >
                        Listado completo
                    </button>
                </div>

                <!-- ── VISTA: RESUMEN ─────────────────────────────────── -->
                <div v-if="activeTab === 'resumen' || pdfMode" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div
                        v-for="([tipo, data]) in tiposOrdenados" :key="tipo"
                        class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden"
                    >
                        <!-- Cabecera del tipo -->
                        <div class="px-4 py-3 flex items-center gap-3 border-b border-gray-100">
                            <div class="w-3 h-3 rounded-full shrink-0" :class="tipoInstColor(tipo)"></div>
                            <div class="flex-1">
                                <p class="text-sm font-semibold text-gray-800">{{ tipo }}</p>
                                <p class="text-[11px] text-gray-400">{{ data.total_ofertas }} cargo{{ data.total_ofertas !== 1 ? 's' : '' }} · {{ data.total_postulaciones }} postulacion{{ data.total_postulaciones !== 1 ? 'es' : '' }}</p>
                            </div>
                            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium" :class="tipoBadge(tipo)">
                                {{ tipo }}
                            </span>
                        </div>
                        <!-- Top cargos -->
                        <div class="px-4 py-3">
                            <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-2">Top cargos publicados</p>
                            <div v-if="data.top_cargos.length" class="space-y-1.5">
                                <div v-for="(cargo, i) in data.top_cargos" :key="i" class="flex items-center gap-2">
                                    <span class="text-[11px] text-gray-400 font-mono w-4 shrink-0">{{ i + 1 }}.</span>
                                    <span class="text-xs text-gray-700 flex-1 truncate">{{ cargo.titulo }}</span>
                                    <span class="text-[11px] font-semibold text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded-full shrink-0">
                                        {{ cargo.count }}x
                                    </span>
                                </div>
                            </div>
                            <p v-else class="text-[11px] text-gray-300">Sin datos</p>
                        </div>
                    </div>
                    <div v-if="!tiposOrdenados.length" class="sm:col-span-2 bg-white rounded-xl border border-gray-100 shadow-sm p-10 text-center">
                        <p class="text-sm text-gray-400">No se encontraron cargos con los filtros seleccionados.</p>
                    </div>
                </div>

                <!-- ── VISTA: DETALLE ─────────────────────────────────── -->
                <div v-if="activeTab === 'detalle'" class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
                    <div class="px-5 py-3 border-b border-gray-100 flex items-center gap-2">
                        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                        </svg>
                        <span class="text-sm font-semibold text-gray-700">Todos los cargos</span>
                        <span class="text-xs text-gray-400">({{ posicionesFiltradas.length }} registros)</span>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="min-w-full text-xs">
                            <thead>
                                <tr class="bg-gray-50 border-b border-gray-100">
                                    <th class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide">#</th>
                                    <th class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Cargo / Título</th>
                                    <th class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Institución</th>
                                    <th class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Tipo inst.</th>
                                    <th class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Tipo</th>
                                    <th class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Área</th>
                                    <th class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Publicado</th>
                                    <th class="px-4 py-2.5 text-center font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Postul.</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr
                                    v-for="(pos, idx) in posicionesFiltradas"
                                    :key="pos.id"
                                    class="border-b border-gray-100 hover:bg-gray-50/60 transition-colors"
                                    :class="idx % 2 === 0 ? '' : 'bg-gray-50/30'"
                                >
                                    <td class="px-4 py-2.5 text-gray-300 font-mono select-none">{{ idx + 1 }}</td>
                                    <td class="px-4 py-2.5 min-w-[180px]">
                                        <p class="font-medium text-gray-800 leading-tight">{{ pos.titulo }}</p>
                                    </td>
                                    <td class="px-4 py-2.5 min-w-[160px]">
                                        <p class="text-gray-600 leading-tight">{{ pos.institucion || '—' }}</p>
                                        <p class="text-gray-400 text-[11px] mt-0.5">{{ pos.sector || '' }}</p>
                                    </td>
                                    <td class="px-4 py-2.5">
                                        <span v-if="pos.tipo_institucion"
                                            class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium"
                                            :class="tipoBadge(pos.tipo_institucion)"
                                        >
                                            {{ pos.tipo_institucion }}
                                        </span>
                                        <span v-else class="text-gray-300">—</span>
                                    </td>
                                    <td class="px-4 py-2.5">
                                        <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium capitalize"
                                            :class="pos.tipo === 'pasantia' ? 'bg-blue-100 text-blue-700 border border-blue-200' : 'bg-purple-100 text-purple-700 border border-purple-200'"
                                        >
                                            {{ pos.tipo }}
                                        </span>
                                    </td>
                                    <td class="px-4 py-2.5 text-gray-600">{{ pos.area || '—' }}</td>
                                    <td class="px-4 py-2.5 text-gray-500 whitespace-nowrap">{{ formatDate(pos.fecha_publicacion) }}</td>
                                    <td class="px-4 py-2.5 text-center">
                                        <span v-if="pos.total_postulaciones > 0" class="font-semibold text-blue-600">{{ pos.total_postulaciones }}</span>
                                        <span v-else class="text-gray-300">0</span>
                                    </td>
                                </tr>
                                <tr v-if="!posicionesFiltradas.length">
                                    <td colspan="8" class="px-4 py-10 text-center text-gray-400 text-sm">
                                        No se encontraron cargos con los filtros seleccionados.
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
