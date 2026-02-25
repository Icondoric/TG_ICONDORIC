<script setup>
/**
 * OfertaFormView
 * Vista para crear/editar ofertas laborales.
 * Layout de 2 columnas: informacion principal a la izquierda,
 * configuracion de publicacion y acciones a la derecha (sticky).
 */

import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useOfertasStore } from '@/features/admin/store/ofertas.store'
import AppLayout from '@/shared/components/AppLayout.vue'

const route = useRoute()
const router = useRouter()
const store = useOfertasStore()

const ofertaId = computed(() => route.params.id)
const isEditing = computed(() => !!ofertaId.value)

// ── Constantes de dominio ──────────────────────────────────
const educationLevels = ['Bachillerato', 'Tecnico', 'Licenciatura', 'Ingenieria', 'Maestria', 'Doctorado']

const commonSkills = [
    'Python', 'Java', 'JavaScript', 'TypeScript', 'SQL', 'NoSQL',
    'React', 'Vue.js', 'Angular', 'Node.js', 'Django', 'FastAPI',
    'Docker', 'AWS', 'Machine Learning', 'Analisis de Datos', 'Scrum', 'Git'
]
const commonSoftSkills = [
    'Comunicacion', 'Trabajo en equipo', 'Liderazgo', 'Proactividad',
    'Responsabilidad', 'Adaptabilidad', 'Resolucion de problemas',
    'Pensamiento critico', 'Gestion del tiempo', 'Orientacion a resultados'
]
const commonLanguages = [
    'Espanol (Nativo)', 'Ingles (A1)', 'Ingles (A2)', 'Ingles (B1)',
    'Ingles (B2)', 'Ingles (C1)', 'Ingles (C2)', 'Frances (B1)', 'Portugues (B1)'
]

// ── Estado del formulario ──────────────────────────────────
const form = reactive({
    titulo: '',
    descripcion: '',
    tipo: '',
    modalidad: '',
    ubicacion: '',
    area: '',
    contact_phone: '',
    contact_email: '',
    institutional_profile_id: '',
    fecha_inicio: '',
    fecha_cierre: '',
    cupos_disponibles: 1,
    is_active: true,
    weights: {
        hard_skills: 0.30,
        soft_skills: 0.20,
        experience: 0.25,
        education: 0.15,
        languages: 0.10
    },
    thresholds: { apto: 0.70, considerado: 0.50 },
    requirements: {
        min_experience_years: 0,
        required_skills: [],
        preferred_skills: [],
        required_soft_skills: [],
        required_education_level: 'Licenciatura',
        required_languages: []
    }
})

const newRequiredSkill = ref('')
const newSoftSkill = ref('')
const newLanguage = ref('')

const loading = ref(false)
const saving = ref(false)
const error = ref(null)

// ── Validaciones ──────────────────────────────────────────
const weightsSum = computed(() =>
    Object.values(form.weights).reduce((a, b) => a + b, 0)
)
const isWeightsValid = computed(() => Math.abs(weightsSum.value - 1.0) < 0.01)
const isThresholdsValid = computed(() => form.thresholds.apto > form.thresholds.considerado)
const titleError = computed(() => {
    const len = form.titulo.trim().length
    if (len > 0 && len < 5) return 'El titulo debe tener al menos 5 caracteres.'
    return null
})

// ── Manejo de errores de API ──────────────────────────────
const FIELD_NAMES = {
    titulo: 'Titulo', tipo: 'Tipo', modalidad: 'Modalidad',
    ubicacion: 'Ubicacion', area: 'Area', contact_phone: 'Telefono',
    contact_email: 'Correo electronico', cupos_disponibles: 'Cupos disponibles',
    fecha_inicio: 'Fecha de inicio', fecha_cierre: 'Fecha de cierre',
}

const parseApiError = (err) => {
    const detail = err.response?.data?.detail
    if (!detail) return 'Ocurrio un error al guardar. Intenta de nuevo.'
    if (typeof detail === 'string') return detail
    if (Array.isArray(detail)) {
        return detail.map(e => {
            const field = e.loc?.length > 1
                ? (FIELD_NAMES[e.loc[e.loc.length - 1]] || e.loc[e.loc.length - 1])
                : ''
            const msg = e.msg || ''
            if (msg.includes('at least') && e.ctx?.min_length)
                return `${field}: debe tener al menos ${e.ctx.min_length} caracteres.`
            if (msg.includes('at most') && e.ctx?.max_length)
                return `${field}: no puede superar ${e.ctx.max_length} caracteres.`
            if (msg.toLowerCase().includes('missing') || msg.toLowerCase().includes('required'))
                return `${field}: campo obligatorio.`
            return field ? `${field}: valor invalido.` : 'Dato invalido.'
        }).join(' ')
    }
    return 'Ocurrio un error al guardar. Intenta de nuevo.'
}

// ── Normalizacion de pesos ────────────────────────────────
const normalizeWeights = () => {
    const sum = weightsSum.value
    if (sum <= 0) return
    const keys = Object.keys(form.weights)
    for (const key of keys) {
        form.weights[key] = Math.round((form.weights[key] / sum) * 100) / 100
    }
    const newSum = Object.values(form.weights).reduce((a, b) => a + b, 0)
    const diff = Math.round((1 - newSum) * 100) / 100
    for (const key of [...keys].reverse()) {
        if (form.weights[key] > 0) {
            form.weights[key] = Math.round((form.weights[key] + diff) * 100) / 100
            break
        }
    }
}

// ── Skills ────────────────────────────────────────────────
const addRequiredSkill = () => {
    const s = newRequiredSkill.value.trim()
    if (s && !form.requirements.required_skills.includes(s)) {
        form.requirements.required_skills.push(s)
        newRequiredSkill.value = ''
    }
}
const addSoftSkill = () => {
    const s = newSoftSkill.value.trim()
    if (s && !form.requirements.required_soft_skills.includes(s)) {
        form.requirements.required_soft_skills.push(s)
        newSoftSkill.value = ''
    }
}
const addLanguage = () => {
    const l = newLanguage.value.trim()
    if (l && !form.requirements.required_languages.includes(l)) {
        form.requirements.required_languages.push(l)
        newLanguage.value = ''
    }
}
const removeSkill = (field, value) => {
    form.requirements[field] = form.requirements[field].filter(v => v !== value)
}

// ── Institucion y sugerencias ─────────────────────────────
const onInstitutionChange = async () => {
    store.clearSuggestions()
    if (!form.institutional_profile_id) return

    // Autocompletar ubicacion desde el perfil (sincrono, ya tenemos la lista)
    const profile = store.profiles.find(p => p.id === form.institutional_profile_id)
    if (profile?.ubicacion) {
        if (!form.ubicacion) {
            form.ubicacion = profile.ubicacion
        } else if (form.ubicacion !== profile.ubicacion) {
            store.suggestions.ubicacion = profile.ubicacion
        }
    }

    await store.fetchContactSuggestions(form.institutional_profile_id)
}

// ── Carga inicial ─────────────────────────────────────────
const loadOferta = async () => {
    if (!isEditing.value) return
    loading.value = true
    error.value = null
    try {
        const oferta = await store.fetchOferta(ofertaId.value)
        form.titulo = oferta.titulo
        form.descripcion = oferta.descripcion || ''
        form.tipo = oferta.tipo
        form.modalidad = oferta.modalidad || ''
        form.ubicacion = oferta.ubicacion || ''
        form.area = oferta.area || ''
        form.contact_phone = oferta.contact_phone || ''
        form.contact_email = oferta.contact_email || ''
        form.institutional_profile_id = oferta.institutional_profile_id || ''
        form.fecha_inicio = oferta.fecha_inicio || ''
        form.fecha_cierre = oferta.fecha_cierre || ''
        form.cupos_disponibles = oferta.cupos_disponibles || 1
        form.is_active = oferta.is_active

        if (oferta.weights) Object.assign(form.weights, oferta.weights)
        if (oferta.thresholds) Object.assign(form.thresholds, oferta.thresholds)
        if (oferta.requirements) {
            Object.assign(form.requirements, oferta.requirements)
            if (!form.requirements.required_skills) form.requirements.required_skills = []
            if (!form.requirements.preferred_skills) form.requirements.preferred_skills = []
            if (!form.requirements.required_soft_skills) form.requirements.required_soft_skills = []
            if (!form.requirements.required_languages) form.requirements.required_languages = []
        }

        if (form.institutional_profile_id) await onInstitutionChange()
    } catch (e) {
        error.value = e.response?.data?.detail || 'Error cargando la oferta'
    } finally {
        loading.value = false
    }
}

// ── Guardar ───────────────────────────────────────────────
const saveOferta = async () => {
    saving.value = true
    error.value = null
    try {
        const data = {
            titulo: form.titulo,
            descripcion: form.descripcion || null,
            tipo: form.tipo,
            modalidad: form.modalidad || null,
            ubicacion: form.ubicacion || null,
            area: form.area || null,
            contact_phone: form.contact_phone || null,
            contact_email: form.contact_email || null,
            institutional_profile_id: form.institutional_profile_id || null,
            fecha_inicio: form.fecha_inicio || null,
            fecha_cierre: form.fecha_cierre || null,
            cupos_disponibles: form.cupos_disponibles,
            weights: { ...form.weights },
            thresholds: { ...form.thresholds },
            requirements: { ...form.requirements }
        }
        if (isEditing.value) data.is_active = form.is_active
        await store.saveOferta(isEditing.value ? ofertaId.value : null, data)
        router.push('/admin/ofertas')
    } catch (e) {
        error.value = parseApiError(e)
    } finally {
        saving.value = false
    }
}

onMounted(async () => {
    await store.loadProfiles()
    await loadOferta()
})
</script>

<template>
    <AppLayout>
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

            <!-- Encabezado -->
            <header class="mb-8">
                <router-link to="/admin/ofertas"
                    class="inline-flex items-center text-slate-500 hover:text-slate-700 mb-4 text-sm">
                    <svg class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                    Volver a Ofertas
                </router-link>
                <h1 class="text-3xl font-bold text-slate-800">
                    {{ isEditing ? 'Editar Oferta' : 'Nueva Oferta Laboral' }}
                </h1>
                <p class="mt-1 text-slate-500">
                    {{ isEditing
                        ? 'Modifica los datos de la oferta y guarda los cambios.'
                        : 'Completa la informacion para publicar la oferta y comenzar a recibir candidatos.' }}
                </p>
            </header>

            <!-- Cargando -->
            <div v-if="loading" class="bg-white rounded-xl shadow-md p-12 text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p class="mt-4 text-slate-500">Cargando oferta...</p>
            </div>

            <form v-else @submit.prevent="saveOferta" class="space-y-6">

                <!-- Error global -->
                <div v-if="error" class="p-4 bg-red-50 border border-red-200 rounded-xl flex items-start gap-3">
                    <svg class="w-5 h-5 text-red-500 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <p class="text-red-700 text-sm">{{ error }}</p>
                </div>

                <!-- ── Layout principal: 2 columnas ── -->
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

                    <!-- ═══ COLUMNA IZQUIERDA (2/3) ═══ -->
                    <div class="lg:col-span-2 space-y-6">

                        <!-- ─── Detalle de la Oferta ─── -->
                        <div class="bg-white rounded-xl shadow-md p-6">
                            <div class="flex items-center gap-3 mb-5">
                                <div class="w-9 h-9 bg-blue-100 rounded-lg flex items-center justify-center shrink-0">
                                    <svg class="w-5 h-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                    </svg>
                                </div>
                                <div>
                                    <h2 class="text-base font-semibold text-slate-800">Detalle de la Oferta</h2>
                                    <p class="text-xs text-slate-400">Informacion principal que veran los candidatos</p>
                                </div>
                            </div>

                            <div class="space-y-4">
                                <!-- Titulo -->
                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">
                                        Titulo del Puesto *
                                    </label>
                                    <input
                                        v-model="form.titulo"
                                        type="text"
                                        required
                                        :class="[
                                            'w-full px-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                                            titleError ? 'border-red-400 bg-red-50' : 'border-slate-200'
                                        ]"
                                        placeholder="Ej: Pasantia en Desarrollo Web, Analista de Datos Jr."
                                    />
                                    <p v-if="titleError" class="mt-1 text-xs text-red-600">{{ titleError }}</p>
                                </div>

                                <!-- Descripcion -->
                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">
                                        Descripcion del Puesto
                                    </label>
                                    <textarea
                                        v-model="form.descripcion"
                                        rows="5"
                                        class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
                                        placeholder="Describe las responsabilidades, el equipo de trabajo, los beneficios y el ambiente laboral..."
                                    ></textarea>
                                    <p class="text-xs text-slate-400 mt-1">
                                        Una descripcion completa atrae candidatos mas adecuados al perfil buscado.
                                    </p>
                                </div>
                            </div>
                        </div>

                        <!-- ─── Empresa y Lugar de Trabajo ─── -->
                        <div class="bg-white rounded-xl shadow-md p-6">
                            <div class="flex items-center gap-3 mb-5">
                                <div class="w-9 h-9 bg-emerald-100 rounded-lg flex items-center justify-center shrink-0">
                                    <svg class="w-5 h-5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-2 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                                    </svg>
                                </div>
                                <div>
                                    <h2 class="text-base font-semibold text-slate-800">Empresa y Lugar de Trabajo</h2>
                                    <p class="text-xs text-slate-400">Donde se publicara la oferta y donde se trabajara</p>
                                </div>
                            </div>

                            <div class="space-y-4">
                                <!-- Perfil institucional -->
                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">
                                        Perfil Institucional
                                    </label>
                                    <select
                                        v-model="form.institutional_profile_id"
                                        @change="onInstitutionChange"
                                        class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                    >
                                        <option value="">Sin perfil asociado</option>
                                        <option v-for="profile in store.profiles" :key="profile.id" :value="profile.id">
                                            {{ profile.institution_name }} — {{ profile.sector }}
                                        </option>
                                    </select>
                                    <p class="text-xs text-slate-400 mt-1">
                                        Al vincular un perfil se autocompletaran la ubicacion y el contacto, y se usara su configuracion de evaluacion.
                                    </p>
                                </div>

                                <!-- Ubicacion y Area -->
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <label class="block text-sm font-medium text-slate-700 mb-1">Ubicacion</label>
                                        <input
                                            v-model="form.ubicacion"
                                            type="text"
                                            class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                            placeholder="Ej: La Paz, Bolivia"
                                        />
                                        <button
                                            v-if="store.suggestions.ubicacion && form.ubicacion !== store.suggestions.ubicacion"
                                            type="button"
                                            @click="form.ubicacion = store.suggestions.ubicacion"
                                            class="mt-1 text-xs text-blue-600 hover:text-blue-800 flex items-center gap-1"
                                        >
                                            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                                            </svg>
                                            Usar del perfil: {{ store.suggestions.ubicacion }}
                                        </button>
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium text-slate-700 mb-1">
                                            Area o Departamento
                                        </label>
                                        <input
                                            v-model="form.area"
                                            type="text"
                                            class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                            placeholder="Ej: Desarrollo de Software, RRHH"
                                        />
                                        <button
                                            v-if="store.suggestions.area && form.area !== store.suggestions.area"
                                            type="button"
                                            @click="form.area = store.suggestions.area"
                                            class="mt-1 text-xs text-blue-600 hover:text-blue-800 flex items-center gap-1"
                                        >
                                            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                                            </svg>
                                            Usar ultimo: {{ store.suggestions.area }}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                    <!-- fin columna izquierda -->

                    <!-- ═══ COLUMNA DERECHA — Sidebar sticky (1/3) ═══ -->
                    <div class="space-y-4 lg:sticky lg:top-6 lg:self-start">

                        <!-- ─── Configuracion de Publicacion ─── -->
                        <div class="bg-white rounded-xl shadow-md p-5">
                            <div class="flex items-center gap-2 mb-4">
                                <div class="w-7 h-7 bg-violet-100 rounded-lg flex items-center justify-center shrink-0">
                                    <svg class="w-4 h-4 text-violet-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                    </svg>
                                </div>
                                <div>
                                    <h2 class="text-sm font-semibold text-slate-800">Publicación</h2>
                                    <p class="text-xs text-slate-400">Tipo, fechas y cupos</p>
                                </div>
                            </div>

                            <div class="space-y-3">
                                <div>
                                    <label class="block text-xs font-medium text-slate-600 mb-1">Tipo de Oferta *</label>
                                    <select
                                        v-model="form.tipo"
                                        required
                                        class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                    >
                                        <option value="">Seleccionar...</option>
                                        <option value="pasantia">Pasantia</option>
                                        <option value="empleo">Empleo</option>
                                    </select>
                                </div>

                                <div>
                                    <label class="block text-xs font-medium text-slate-600 mb-1">Modalidad</label>
                                    <select
                                        v-model="form.modalidad"
                                        class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                    >
                                        <option value="">Seleccionar...</option>
                                        <option value="presencial">Presencial</option>
                                        <option value="remoto">Remoto</option>
                                        <option value="hibrido">Hibrido</option>
                                    </select>
                                </div>

                                <div class="grid grid-cols-2 gap-2">
                                    <div>
                                        <label class="block text-xs font-medium text-slate-600 mb-1">Desde</label>
                                        <input
                                            v-model="form.fecha_inicio"
                                            type="date"
                                            class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                        />
                                    </div>
                                    <div>
                                        <label class="block text-xs font-medium text-slate-600 mb-1">Cierre</label>
                                        <input
                                            v-model="form.fecha_cierre"
                                            type="date"
                                            class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                        />
                                    </div>
                                </div>

                                <div>
                                    <label class="block text-xs font-medium text-slate-600 mb-1">Cupos Disponibles</label>
                                    <input
                                        v-model.number="form.cupos_disponibles"
                                        type="number"
                                        min="1"
                                        class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                    />
                                </div>

                                <div v-if="isEditing" class="flex items-center gap-2 pt-1 border-t border-slate-100">
                                    <input
                                        v-model="form.is_active"
                                        type="checkbox"
                                        id="is_active"
                                        class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-slate-300 rounded"
                                    />
                                    <label for="is_active" class="text-xs font-medium text-slate-600 cursor-pointer">
                                        Oferta activa y visible para candidatos
                                    </label>
                                </div>
                            </div>
                        </div>

                        <!-- ─── Contacto ─── -->
                        <div class="bg-white rounded-xl shadow-md p-5">
                            <div class="flex items-center gap-2 mb-4">
                                <div class="w-7 h-7 bg-sky-100 rounded-lg flex items-center justify-center shrink-0">
                                    <svg class="w-4 h-4 text-sky-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                    </svg>
                                </div>
                                <div>
                                    <h2 class="text-sm font-semibold text-slate-800">Contacto</h2>
                                    <p class="text-xs text-slate-400">Para consultas de candidatos</p>
                                </div>
                            </div>

                            <div v-if="store.loadingSuggestions" class="flex items-center gap-2 mb-3 text-xs text-slate-400">
                                <div class="animate-spin rounded-full h-3 w-3 border-b-2 border-blue-400"></div>
                                Buscando datos previos de la empresa...
                            </div>

                            <div class="space-y-3">
                                <div>
                                    <label class="block text-xs font-medium text-slate-600 mb-1">Telefono</label>
                                    <input
                                        v-model="form.contact_phone"
                                        type="tel"
                                        class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                        placeholder="+591 2 1234567"
                                    />
                                    <button
                                        v-if="store.suggestions.contact_phone && form.contact_phone !== store.suggestions.contact_phone"
                                        type="button"
                                        @click="form.contact_phone = store.suggestions.contact_phone"
                                        class="mt-1 text-xs text-blue-600 hover:text-blue-800 flex items-center gap-1"
                                    >
                                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                                        </svg>
                                        Usar ultimo: {{ store.suggestions.contact_phone }}
                                    </button>
                                </div>

                                <div>
                                    <label class="block text-xs font-medium text-slate-600 mb-1">Correo Electronico</label>
                                    <input
                                        v-model="form.contact_email"
                                        type="email"
                                        class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                        placeholder="rrhh@empresa.com"
                                    />
                                    <button
                                        v-if="store.suggestions.contact_email && form.contact_email !== store.suggestions.contact_email"
                                        type="button"
                                        @click="form.contact_email = store.suggestions.contact_email"
                                        class="mt-1 text-xs text-blue-600 hover:text-blue-800 flex items-center gap-1"
                                    >
                                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                                        </svg>
                                        Usar ultimo: {{ store.suggestions.contact_email }}
                                    </button>
                                </div>
                            </div>
                        </div>

                    </div>
                    <!-- fin columna derecha -->

                </div>
                <!-- fin grid principal -->

                <!-- ─── Configuracion de Evaluacion (ancho completo) ─── -->
                <div class="bg-white rounded-xl shadow-md p-6">
                    <!-- Encabezado -->
                    <div class="flex items-center gap-3 mb-6">
                        <div class="w-9 h-9 bg-amber-100 rounded-lg flex items-center justify-center shrink-0">
                            <svg class="w-5 h-5 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                            </svg>
                        </div>
                        <div>
                            <h2 class="text-base font-semibold text-slate-800">Configuracion de Evaluacion</h2>
                            <p class="text-xs text-slate-400">Criterios para evaluar y clasificar a los candidatos que postulen</p>
                        </div>
                    </div>

                    <div class="space-y-8">

                        <!-- ── 1. Requisitos Minimos ── -->
                        <div>
                            <div class="flex items-center gap-2 mb-4">
                                <span class="w-6 h-6 rounded-full bg-blue-600 text-white text-xs flex items-center justify-center font-bold shrink-0">1</span>
                                <div>
                                    <h3 class="text-sm font-semibold text-slate-700">Requisitos Minimos</h3>
                                    <p class="text-xs text-slate-400">Condiciones que el candidato debe cumplir para ser evaluado</p>
                                </div>
                            </div>

                            <!-- Experiencia y Educacion -->
                            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
                                <div>
                                    <label class="block text-xs font-medium text-slate-600 mb-1">Experiencia minima (años)</label>
                                    <input
                                        v-model.number="form.requirements.min_experience_years"
                                        type="number" min="0" step="0.5"
                                        placeholder="0"
                                        class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                    />
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-600 mb-1">Nivel educativo minimo</label>
                                    <select
                                        v-model="form.requirements.required_education_level"
                                        class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                    >
                                        <option v-for="lvl in educationLevels" :key="lvl" :value="lvl">{{ lvl }}</option>
                                    </select>
                                </div>
                            </div>

                            <!-- Habilidades en 3 columnas -->
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <!-- Tecnicas -->
                                <div class="bg-slate-50 rounded-lg p-3">
                                    <label class="block text-xs font-semibold text-slate-600 mb-2">Habilidades Tecnicas</label>
                                    <div class="flex gap-1.5 mb-2">
                                        <input
                                            v-model="newRequiredSkill"
                                            @keyup.enter.prevent="addRequiredSkill"
                                            type="text"
                                            list="oferta-skillsList"
                                            placeholder="Agregar..."
                                            class="flex-1 px-2.5 py-1.5 border border-slate-200 rounded-md text-xs bg-white focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                                        />
                                        <button type="button" @click="addRequiredSkill"
                                            class="px-2.5 py-1.5 bg-blue-600 text-white text-xs rounded-md hover:bg-blue-700 font-medium">
                                            +
                                        </button>
                                    </div>
                                    <div class="flex flex-wrap gap-1.5 min-h-6">
                                        <span
                                            v-for="skill in form.requirements.required_skills" :key="skill"
                                            class="inline-flex items-center px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-xs"
                                        >
                                            {{ skill }}
                                            <button type="button" @click="removeSkill('required_skills', skill)"
                                                class="ml-1 hover:text-blue-900 leading-none">&times;</button>
                                        </span>
                                        <span v-if="form.requirements.required_skills.length === 0"
                                            class="text-xs text-slate-400 italic">Ninguna aun</span>
                                    </div>
                                </div>

                                <!-- Blandas -->
                                <div class="bg-slate-50 rounded-lg p-3">
                                    <label class="block text-xs font-semibold text-slate-600 mb-2">Habilidades Blandas</label>
                                    <div class="flex gap-1.5 mb-2">
                                        <input
                                            v-model="newSoftSkill"
                                            @keyup.enter.prevent="addSoftSkill"
                                            type="text"
                                            list="oferta-softSkillsList"
                                            placeholder="Agregar..."
                                            class="flex-1 px-2.5 py-1.5 border border-slate-200 rounded-md text-xs bg-white focus:ring-1 focus:ring-purple-500 focus:border-purple-500"
                                        />
                                        <button type="button" @click="addSoftSkill"
                                            class="px-2.5 py-1.5 bg-purple-600 text-white text-xs rounded-md hover:bg-purple-700 font-medium">
                                            +
                                        </button>
                                    </div>
                                    <div class="flex flex-wrap gap-1.5 min-h-6">
                                        <span
                                            v-for="skill in form.requirements.required_soft_skills" :key="skill"
                                            class="inline-flex items-center px-2 py-0.5 bg-purple-100 text-purple-700 rounded-full text-xs"
                                        >
                                            {{ skill }}
                                            <button type="button" @click="removeSkill('required_soft_skills', skill)"
                                                class="ml-1 hover:text-purple-900 leading-none">&times;</button>
                                        </span>
                                        <span v-if="form.requirements.required_soft_skills.length === 0"
                                            class="text-xs text-slate-400 italic">Ninguna aun</span>
                                    </div>
                                </div>

                                <!-- Idiomas -->
                                <div class="bg-slate-50 rounded-lg p-3">
                                    <label class="block text-xs font-semibold text-slate-600 mb-2">Idiomas Requeridos</label>
                                    <div class="flex gap-1.5 mb-2">
                                        <input
                                            v-model="newLanguage"
                                            @keyup.enter.prevent="addLanguage"
                                            type="text"
                                            list="oferta-languagesList"
                                            placeholder="Agregar..."
                                            class="flex-1 px-2.5 py-1.5 border border-slate-200 rounded-md text-xs bg-white focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                                        />
                                        <button type="button" @click="addLanguage"
                                            class="px-2.5 py-1.5 bg-slate-300 text-slate-700 text-xs rounded-md hover:bg-slate-400 font-medium">
                                            +
                                        </button>
                                    </div>
                                    <div class="flex flex-wrap gap-1.5 min-h-6">
                                        <span
                                            v-for="lang in form.requirements.required_languages" :key="lang"
                                            class="inline-flex items-center px-2 py-0.5 bg-green-100 text-green-700 rounded-full text-xs"
                                        >
                                            {{ lang }}
                                            <button type="button" @click="removeSkill('required_languages', lang)"
                                                class="ml-1 hover:text-green-900 leading-none">&times;</button>
                                        </span>
                                        <span v-if="form.requirements.required_languages.length === 0"
                                            class="text-xs text-slate-400 italic">Ninguno aun</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Datalists -->
                            <datalist id="oferta-skillsList">
                                <option v-for="s in commonSkills" :key="s" :value="s" />
                            </datalist>
                            <datalist id="oferta-softSkillsList">
                                <option v-for="s in commonSoftSkills" :key="s" :value="s" />
                            </datalist>
                            <datalist id="oferta-languagesList">
                                <option v-for="l in commonLanguages" :key="l" :value="l" />
                            </datalist>
                        </div>

                        <!-- ── 2. Pesos + 3. Umbrales en grid 2 columnas ── -->
                        <div class="grid grid-cols-1 lg:grid-cols-5 gap-8 border-t border-slate-100 pt-6">

                            <!-- 2. Pesos (3/5) -->
                            <div class="lg:col-span-3">
                                <div class="flex items-center justify-between mb-1">
                                    <div class="flex items-center gap-2">
                                        <span class="w-6 h-6 rounded-full bg-blue-600 text-white text-xs flex items-center justify-center font-bold shrink-0">2</span>
                                        <h3 class="text-sm font-semibold text-slate-700">Pesos de Evaluacion</h3>
                                    </div>
                                    <div class="flex items-center gap-3">
                                        <span :class="[
                                            'text-xs font-semibold px-2 py-0.5 rounded-full',
                                            isWeightsValid ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                                        ]">
                                            {{ (weightsSum * 100).toFixed(0) }}%
                                        </span>
                                        <button type="button" @click="normalizeWeights"
                                            class="text-xs text-blue-600 hover:text-blue-800 underline">
                                            Normalizar a 100%
                                        </button>
                                    </div>
                                </div>
                                <p class="text-xs text-slate-400 mb-4 ml-8">
                                    Cuanto vale cada dimension al calcular la puntuacion final del candidato. Debe sumar exactamente 100%.
                                </p>

                                <div class="space-y-3">
                                    <div
                                        v-for="[key, label, color] in [
                                            ['hard_skills', 'Habilidades Tecnicas', 'blue'],
                                            ['soft_skills', 'Habilidades Blandas', 'purple'],
                                            ['experience', 'Experiencia Laboral', 'emerald'],
                                            ['education', 'Nivel Educativo', 'amber'],
                                            ['languages', 'Idiomas', 'teal']
                                        ]"
                                        :key="key"
                                    >
                                        <div class="flex justify-between text-xs mb-1">
                                            <span class="font-medium text-slate-600">{{ label }}</span>
                                            <span class="font-semibold text-slate-700">{{ (form.weights[key] * 100).toFixed(0) }}%</span>
                                        </div>
                                        <input
                                            v-model.number="form.weights[key]"
                                            type="range" min="0" max="1" step="0.05"
                                            class="w-full h-1.5 bg-slate-200 rounded-full appearance-none cursor-pointer accent-blue-600"
                                        />
                                    </div>
                                </div>
                            </div>

                            <!-- 3. Umbrales (2/5) -->
                            <div class="lg:col-span-2">
                                <div class="flex items-center gap-2 mb-1">
                                    <span class="w-6 h-6 rounded-full bg-blue-600 text-white text-xs flex items-center justify-center font-bold shrink-0">3</span>
                                    <h3 class="text-sm font-semibold text-slate-700">Umbrales de Clasificacion</h3>
                                </div>
                                <p class="text-xs text-slate-400 mb-4 ml-8">
                                    Puntuacion minima para asignar cada categoria al candidato.
                                </p>

                                <div v-if="!isThresholdsValid" class="mb-3 p-2.5 rounded-lg text-xs bg-red-50 border border-red-200 text-red-700">
                                    El umbral APTO debe ser mayor que CONSIDERADO.
                                </div>

                                <div class="space-y-3">
                                    <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                                        <div class="flex items-center justify-between mb-2">
                                            <span class="text-xs font-bold text-green-700 uppercase tracking-wide">APTO</span>
                                            <span class="text-xs text-green-600">Score &ge; {{ (form.thresholds.apto * 100).toFixed(0) }}%</span>
                                        </div>
                                        <input
                                            v-model.number="form.thresholds.apto"
                                            type="number" min="0" max="1" step="0.05"
                                            class="w-full px-3 py-1.5 border border-green-300 rounded-lg text-sm bg-white focus:ring-2 focus:ring-green-500"
                                        />
                                    </div>

                                    <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                                        <div class="flex items-center justify-between mb-2">
                                            <span class="text-xs font-bold text-yellow-700 uppercase tracking-wide">CONSIDERADO</span>
                                            <span class="text-xs text-yellow-600">Score &ge; {{ (form.thresholds.considerado * 100).toFixed(0) }}%</span>
                                        </div>
                                        <input
                                            v-model.number="form.thresholds.considerado"
                                            type="number" min="0" max="1" step="0.05"
                                            class="w-full px-3 py-1.5 border border-yellow-300 rounded-lg text-sm bg-white focus:ring-2 focus:ring-yellow-500"
                                        />
                                    </div>

                                    <div class="bg-slate-100 border border-slate-200 rounded-lg p-3 text-center">
                                        <span class="text-xs font-bold text-slate-500 uppercase tracking-wide">NO APTO</span>
                                        <p class="text-xs text-slate-400 mt-0.5">Menos de {{ (form.thresholds.considerado * 100).toFixed(0) }}%</p>
                                    </div>
                                </div>
                            </div>

                        </div>
                        <!-- fin grid pesos + umbrales -->

                    </div>
                    <!-- fin config propia -->

                </div>
                <!-- fin Configuracion de Evaluacion -->

                <!-- ─── Botones de accion ─── -->
                <div class="flex justify-end gap-3 pt-2">
                    <router-link
                        to="/admin/ofertas"
                        class="px-6 py-2.5 text-sm text-slate-600 hover:text-slate-800 font-medium rounded-lg border border-slate-200 hover:bg-slate-50 transition-colors"
                    >
                        Cancelar
                    </router-link>
                    <button
                        type="submit"
                        :disabled="saving || !isWeightsValid"
                        :class="[
                            'px-8 py-2.5 rounded-lg font-semibold text-white text-sm transition-all',
                            (saving || !isWeightsValid)
                                ? 'bg-slate-300 cursor-not-allowed'
                                : 'bg-blue-600 hover:bg-blue-700 hover:shadow-md'
                        ]"
                    >
                        <span v-if="saving" class="flex items-center gap-2">
                            <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Guardando...
                        </span>
                        <span v-else>{{ isEditing ? 'Guardar Cambios' : 'Publicar Oferta' }}</span>
                    </button>
                </div>

            </form>
        </div>
    </AppLayout>
</template>

<style scoped>
input[type="range"] { -webkit-appearance: none; }
input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    height: 14px; width: 14px;
    border-radius: 50%;
    background: #3b82f6;
    cursor: pointer;
    margin-top: -5px;
}
input[type="range"]::-moz-range-thumb {
    height: 14px; width: 14px;
    border-radius: 50%;
    background: #3b82f6;
    cursor: pointer;
    border: none;
}
</style>
