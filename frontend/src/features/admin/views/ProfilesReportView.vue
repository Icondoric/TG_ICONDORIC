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

// Filters
const startDate = ref('')
const endDate = ref('')
const sectorFilter = ref('')
const estadoFilter = ref('')
const nombreFilter = ref('')

// Data
const reportData = ref(null)

// PDF column config
const PDF_COLUMNS = [
    { key: 'institucion',   label: 'Institución (Nombre + Sector)', locked: true },
    { key: 'estado',        label: 'Estado' },
    { key: 'ubicacion',     label: 'Ubicación' },
    { key: 'contacto',      label: 'Contacto (Email / Teléfono)' },
    { key: 'ofertas',       label: 'Ofertas (Total / Activas)' },
    { key: 'postulaciones', label: 'Postulaciones' },
    { key: 'fechas',        label: 'Fecha de registro / Actualización' },
]
const pdfColEnabled = ref(
    Object.fromEntries(PDF_COLUMNS.map(c => [c.key, true]))
)
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
            sector: sectorFilter.value || undefined,
            estado: estadoFilter.value || undefined,
            nombre: nombreFilter.value || undefined,
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

const resetFilters = () => {
    sectorFilter.value = ''
    estadoFilter.value = ''
    nombreFilter.value = ''
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
    const element = document.getElementById('profiles-report-container')
    const opt = {
        margin: [12, 8, 12, 8],
        filename: `reporte-perfiles-${startDate.value}_${endDate.value}.pdf`,
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

const estadoBadge = (isActive) => isActive
    ? 'bg-green-100 text-green-700 border border-green-200'
    : 'bg-gray-100 text-gray-600 border border-gray-200'

const activeFiltersCount = computed(() => {
    let n = 0
    if (sectorFilter.value) n++
    if (estadoFilter.value) n++
    if (nombreFilter.value) n++
    return n
})

const enabledPdfColCount = computed(() =>
    PDF_COLUMNS.filter(c => pdfColEnabled.value[c.key]).length
)

// Top sectors sorted by count for mini bar chart
const topSectors = computed(() => {
    const entries = Object.entries(reportData.value?.stats.by_sector || {})
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
                        <h1 class="text-2xl font-bold text-emi-navy-500">Reporte de Perfiles Institucionales</h1>
                        <p class="mt-0.5 text-sm text-gray-500">Detalle de instituciones registradas en la plataforma.</p>
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
                            <label
                                v-for="col in PDF_COLUMNS" :key="col.key"
                                class="flex items-center gap-3 p-2.5 rounded-lg cursor-pointer transition-colors"
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

                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 items-end">
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Registrado desde</label>
                        <input type="date" v-model="startDate" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Registrado hasta</label>
                        <input type="date" v-model="endDate" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Institución</label>
                        <input type="text" v-model="nombreFilter" placeholder="Ej: AGETIC, YPFB..." class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Sector</label>
                        <input type="text" v-model="sectorFilter" placeholder="Ej: Tecnología, Salud..." class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-gray-500 mb-1">Estado</label>
                        <select v-model="estadoFilter" class="w-full px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-emi-navy-200 focus:outline-none">
                            <option value="">Todos</option>
                            <option value="activo">Activos</option>
                            <option value="inactivo">Inactivos</option>
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

            <!-- ── Contenido del reporte ───────────────────────────────── -->
            <div v-else id="profiles-report-container" class="space-y-5">

                <!-- Encabezado PDF -->
                <div v-if="pdfMode" class="bg-emi-navy-700 text-white px-6 py-4 rounded-xl flex items-center justify-between">
                    <div>
                        <p class="text-[10px] text-blue-200 uppercase tracking-widest mb-1">Sistema de Bolsa Laboral — EMI</p>
                        <h1 class="text-xl font-bold">Reporte de Perfiles Institucionales</h1>
                        <p class="text-xs text-blue-100 mt-0.5">Período: {{ formatDate(startDate) }} — {{ formatDate(endDate) }}</p>
                    </div>
                    <div class="text-right text-xs text-blue-100 space-y-1">
                        <p>Generado: {{ formatDate(new Date().toISOString()) }}</p>
                        <p>Total mostrado: <span class="font-bold text-white">{{ reportData?.profiles?.length }}</span> perfiles</p>
                    </div>
                </div>

                <!-- ── Tarjetas resumen ─────────────────────────────── -->
                <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
                    <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Total</p>
                        <p class="text-2xl font-bold text-emi-navy-500 mt-1">{{ reportData?.stats.total }}</p>
                        <p class="text-[11px] text-gray-400">instituciones</p>
                    </div>
                    <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Activas</p>
                        <p class="text-2xl font-bold text-green-600 mt-1">{{ reportData?.stats.activos }}</p>
                        <p class="text-[11px] text-gray-400">{{ reportData?.stats.inactivos }} inactivas</p>
                    </div>
                    <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Ofertas activas</p>
                        <p class="text-2xl font-bold text-blue-600 mt-1">{{ reportData?.stats.total_ofertas_activas }}</p>
                        <p class="text-[11px] text-gray-400">publicadas actualmente</p>
                    </div>
                    <div class="bg-white px-4 py-3 rounded-xl border border-gray-100 shadow-sm">
                        <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Postulaciones</p>
                        <p class="text-2xl font-bold text-purple-600 mt-1">{{ reportData?.stats.total_postulaciones }}</p>
                        <p class="text-[11px] text-gray-400">en total</p>
                    </div>
                </div>

                <!-- Distribución por sector -->
                <div v-if="topSectors.length" class="bg-white px-5 py-4 rounded-xl border border-gray-100 shadow-sm">
                    <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-3">Distribución por Sector</p>
                    <div class="space-y-2">
                        <div v-for="s in topSectors" :key="s.name" class="flex items-center gap-3">
                            <span class="text-xs text-gray-600 capitalize w-32 shrink-0 truncate">{{ s.name }}</span>
                            <div class="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                                <div class="h-2 bg-emi-navy-500 rounded-full" :style="{ width: s.pct + '%' }"></div>
                            </div>
                            <span class="text-xs font-semibold text-gray-700 w-6 text-right shrink-0">{{ s.count }}</span>
                        </div>
                    </div>
                </div>

                <!-- ── Tabla ──────────────────────────────────────────── -->
                <div class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
                    <div class="px-5 py-3 border-b border-gray-100 flex items-center gap-2" :class="{ 'hidden': pdfMode }">
                        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                        </svg>
                        <span class="text-sm font-semibold text-gray-700">Listado de perfiles</span>
                        <span class="text-xs text-gray-400">({{ reportData?.profiles?.length }} registros)</span>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="min-w-full text-xs">
                            <thead>
                                <tr class="bg-gray-50 border-b border-gray-100">
                                    <th class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide">#</th>
                                    <th class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Institución</th>
                                    <th v-if="colVisible('estado')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Estado</th>
                                    <th v-if="colVisible('ubicacion')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Ubicación</th>
                                    <th v-if="colVisible('contacto')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Contacto</th>
                                    <th v-if="colVisible('ofertas')" class="px-4 py-2.5 text-center font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Ofertas</th>
                                    <th v-if="colVisible('postulaciones')" class="px-4 py-2.5 text-center font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Postul.</th>
                                    <th v-if="colVisible('fechas')" class="px-4 py-2.5 text-left font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap">Registro / Act.</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr
                                    v-for="(profile, idx) in reportData?.profiles"
                                    :key="profile.id"
                                    class="border-b border-gray-100 hover:bg-gray-50/60 transition-colors"
                                    :class="idx % 2 === 0 ? '' : 'bg-gray-50/30'"
                                >
                                    <td class="px-4 py-2.5 text-gray-300 font-mono select-none">{{ idx + 1 }}</td>

                                    <td class="px-4 py-2.5 min-w-[180px]">
                                        <p class="font-medium text-gray-800 leading-tight">{{ profile.institution_name || '—' }}</p>
                                        <p class="text-gray-400 mt-0.5 capitalize">{{ profile.sector || '—' }}</p>
                                    </td>

                                    <td v-if="colVisible('estado')" class="px-4 py-2.5">
                                        <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium" :class="estadoBadge(profile.is_active)">
                                            {{ profile.is_active ? 'Activo' : 'Inactivo' }}
                                        </span>
                                    </td>

                                    <td v-if="colVisible('ubicacion')" class="px-4 py-2.5 text-gray-600 whitespace-nowrap">
                                        {{ profile.ubicacion || '—' }}
                                    </td>

                                    <td v-if="colVisible('contacto')" class="px-4 py-2.5 min-w-[160px]">
                                        <p v-if="profile.contact_email" class="text-gray-600 truncate max-w-[180px]">{{ profile.contact_email }}</p>
                                        <p v-if="profile.contact_phone" class="text-gray-400 mt-0.5">{{ profile.contact_phone }}</p>
                                        <span v-if="!profile.contact_email && !profile.contact_phone" class="text-gray-300">—</span>
                                    </td>

                                    <td v-if="colVisible('ofertas')" class="px-4 py-2.5 text-center">
                                        <span class="font-semibold text-gray-700">{{ profile.total_ofertas }}</span>
                                        <span v-if="profile.ofertas_activas > 0" class="block text-[10px] text-green-600 font-medium mt-0.5">
                                            {{ profile.ofertas_activas }} activa{{ profile.ofertas_activas !== 1 ? 's' : '' }}
                                        </span>
                                        <span v-else class="block text-[10px] text-gray-300 mt-0.5">sin activas</span>
                                    </td>

                                    <td v-if="colVisible('postulaciones')" class="px-4 py-2.5 text-center">
                                        <span v-if="profile.total_postulaciones > 0" class="font-semibold text-blue-600">{{ profile.total_postulaciones }}</span>
                                        <span v-else class="text-gray-300">0</span>
                                    </td>

                                    <td v-if="colVisible('fechas')" class="px-4 py-2.5 whitespace-nowrap">
                                        <p class="text-gray-500">{{ formatDate(profile.created_at) }}</p>
                                        <p class="text-gray-400 mt-0.5">{{ formatDate(profile.updated_at) }}</p>
                                    </td>
                                </tr>

                                <tr v-if="!reportData?.profiles?.length">
                                    <td colspan="8" class="px-4 py-10 text-center text-gray-400 text-sm">
                                        No se encontraron perfiles con los filtros seleccionados.
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
