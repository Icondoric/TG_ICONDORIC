<script setup>
/**
 * OfertaFormView
 * Vista para crear/editar ofertas laborales.
 * Formulario en 3 pasos: Información General / Publicación y Contacto / Criterios de Evaluación
 */

import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useOfertasStore } from '@/features/admin/store/ofertas.store'
import AppLayout from '@/shared/components/AppLayout.vue'
import { formatApiError } from '@/shared/utils/apiError'

const route = useRoute()
const router = useRouter()
const store = useOfertasStore()

const ofertaId = computed(() => route.params.id)
const isEditing = computed(() => !!ofertaId.value)

// ── Constantes de dominio ──────────────────────────────────
const educationLevels = ['Bachillerato', 'Tecnico', 'Licenciatura', 'Ingenieria', 'Maestria', 'Doctorado']

const emiCarreras = [
    'Ingenieria Civil',
    'Ingenieria de Sistemas',
    'Ingenieria Geografica',
    'Ingenieria Mecatronica',
    'Ingenieria en Sistemas Electronicos',
    'Ingenieria Financiera',
    'Ingenieria Industrial',
    'Derecho',
    'Ingenieria Comercial',
]

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

// ── Pesos y umbrales por defecto ───────────────────────────
const DEFAULT_WEIGHTS = { hard_skills: 0.30, soft_skills: 0.20, experience: 0.25, education: 0.15, languages: 0.10 }
const DEFAULT_THRESHOLDS = { apto: 0.70, considerado: 0.50 }

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
    weights: { ...DEFAULT_WEIGHTS },
    thresholds: { ...DEFAULT_THRESHOLDS },
    requirements: {
        min_experience_years: 0,
        required_skills: [],
        preferred_skills: [],
        required_soft_skills: [],
        required_education_level: 'Licenciatura',
        required_languages: [],
        carreras_aceptadas: [],
        semestre_minimo: null,
        semestre_maximo: null
    }
})

const newRequiredSkill = ref('')
const newSoftSkill = ref('')
const newLanguage = ref('')

const loading = ref(false)
const saving = ref(false)
const error = ref(null)

// ── Navegación por pasos ───────────────────────────────────
const currentStep = ref(1)
const stepError = ref(null)
const useCustomEvaluation = ref(false)

const steps = [
    { label: 'Información General' },
    { label: 'Publicación y Contacto' },
    { label: 'Criterios de Evaluación' },
]

const goNext = () => {
    stepError.value = null
    if (currentStep.value === 1) {
        if (form.titulo.trim().length < 5) {
            stepError.value = 'El título debe tener al menos 5 caracteres para continuar.'
            return
        }
    }
    if (currentStep.value === 2) {
        if (!form.tipo) {
            stepError.value = 'Selecciona el tipo de oferta antes de continuar.'
            return
        }
    }
    currentStep.value++
}

const goPrev = () => {
    stepError.value = null
    currentStep.value--
}

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

// ── Normalizacion de pesos ────────────────────────────────
const normalizeWeights = () => {
    const sum = weightsSum.value
    if (sum <= 0) return
    const keys = Object.keys(form.weights)
    let accumulated = 0
    for (let i = 0; i < keys.length; i++) {
        if (i === keys.length - 1) {
            form.weights[keys[i]] = Math.round((1 - accumulated) * 1000) / 1000
        } else {
            const v = Math.round((form.weights[keys[i]] / sum) * 1000) / 1000
            form.weights[keys[i]] = v
            accumulated += v
        }
    }
}

const resetToDefaultEvaluation = () => {
    Object.assign(form.weights, DEFAULT_WEIGHTS)
    Object.assign(form.thresholds, DEFAULT_THRESHOLDS)
    useCustomEvaluation.value = false
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

const toggleCarrera = (carrera) => {
    const idx = form.requirements.carreras_aceptadas.indexOf(carrera)
    if (idx === -1) {
        form.requirements.carreras_aceptadas.push(carrera)
    } else {
        form.requirements.carreras_aceptadas.splice(idx, 1)
    }
}

// ── Busqueda de perfil institucional ─────────────────────
const profileSearch = ref('')
const profileDropdownOpen = ref(false)
const selectedProfileName = ref('')

const filteredProfiles = computed(() => {
    const q = profileSearch.value.trim().toLowerCase()
    if (!q) return store.profiles
    return store.profiles.filter(p =>
        p.institution_name.toLowerCase().includes(q) ||
        (p.sector || '').toLowerCase().includes(q)
    )
})

const selectProfile = async (profile) => {
    form.institutional_profile_id = profile.id
    selectedProfileName.value = profile.institution_name
    profileSearch.value = ''
    profileDropdownOpen.value = false
    await onInstitutionChange()
}

const clearProfile = () => {
    form.institutional_profile_id = ''
    selectedProfileName.value = ''
    profileSearch.value = ''
    profileDropdownOpen.value = false
    store.clearSuggestions()
}

// ── Institucion y sugerencias ─────────────────────────────
const onInstitutionChange = async () => {
    store.clearSuggestions()
    if (!form.institutional_profile_id) return

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

        if (oferta.weights) {
            for (const key of Object.keys(form.weights)) {
                if (oferta.weights[key] !== undefined) form.weights[key] = oferta.weights[key]
            }
            // Si los pesos difieren de los defaults, abrir el panel de personalización
            const differsFromDefault = Object.keys(DEFAULT_WEIGHTS).some(
                k => Math.abs(form.weights[k] - DEFAULT_WEIGHTS[k]) > 0.001
            )
            if (differsFromDefault) useCustomEvaluation.value = true
        }
        if (oferta.thresholds) {
            Object.assign(form.thresholds, oferta.thresholds)
            const thresholdsDiffer =
                Math.abs(form.thresholds.apto - DEFAULT_THRESHOLDS.apto) > 0.001 ||
                Math.abs(form.thresholds.considerado - DEFAULT_THRESHOLDS.considerado) > 0.001
            if (thresholdsDiffer) useCustomEvaluation.value = true
        }
        if (oferta.requirements) {
            Object.assign(form.requirements, oferta.requirements)
            if (!form.requirements.required_skills) form.requirements.required_skills = []
            if (!form.requirements.preferred_skills) form.requirements.preferred_skills = []
            if (!form.requirements.required_soft_skills) form.requirements.required_soft_skills = []
            if (!form.requirements.required_languages) form.requirements.required_languages = []
            if (!form.requirements.carreras_aceptadas) form.requirements.carreras_aceptadas = []
            if (form.requirements.semestre_minimo === undefined) form.requirements.semestre_minimo = null
            if (form.requirements.semestre_maximo === undefined) form.requirements.semestre_maximo = null
        }

        if (form.institutional_profile_id) {
            const p = store.profiles.find(x => x.id === form.institutional_profile_id)
            if (p) selectedProfileName.value = p.institution_name
            await onInstitutionChange()
        }
    } catch (e) {
        error.value = formatApiError(e, 'Error cargando la oferta')
    } finally {
        loading.value = false
    }
}

// ── Guardar ───────────────────────────────────────────────
const saveOferta = async () => {
    if (!isWeightsValid.value) {
        error.value = `Los pesos de evaluación suman ${(weightsSum.value * 100).toFixed(0)}%. Deben sumar exactamente 100%. Usa el botón "Normalizar a 100%".`
        return
    }

    saving.value = true
    error.value = null
    try {
        const rawWeights = { ...form.weights }
        const wSum = Object.values(rawWeights).reduce((a, b) => a + b, 0)
        const normalizedWeights = Object.fromEntries(
            Object.entries(rawWeights).map(([k, v]) => [k, Math.round((v / wSum) * 1000) / 1000])
        )

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
            weights: normalizedWeights,
            thresholds: { ...form.thresholds },
            requirements: { ...form.requirements }
        }
        if (isEditing.value) data.is_active = form.is_active
        await store.saveOferta(isEditing.value ? ofertaId.value : null, data)
        router.push('/admin/ofertas')
    } catch (e) {
        error.value = formatApiError(e, 'Ocurrio un error al guardar.')
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
                <h1 class="text-3xl font-bold text-emi-navy-500">
                    {{ isEditing ? 'Editar Oferta' : 'Nueva Oferta Laboral' }}
                </h1>
                <p class="mt-1 text-slate-500">
                    {{ isEditing
                        ? 'Modifica los datos de la oferta y guarda los cambios.'
                        : 'Completa la informacion para publicar la oferta y comenzar a recibir candidatos.' }}
                </p>
            </header>

            <!-- Cargando -->
            <div v-if="loading" class="card-emi p-12 text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emi-gold mx-auto"></div>
                <p class="mt-4 text-slate-500">Cargando oferta...</p>
            </div>

            <form v-else novalidate @submit.prevent="saveOferta" class="space-y-6">

                <!-- Error global -->
                <div v-if="error" class="p-4 bg-red-50 border border-red-200 rounded-xl flex items-start gap-3">
                    <svg class="w-5 h-5 text-red-500 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <p class="text-red-700 text-sm whitespace-pre-line">{{ error }}</p>
                </div>

                <!-- ── Indicador de pasos ── -->
                <nav class="flex items-center">
                    <template v-for="(step, idx) in steps" :key="idx">
                        <div class="flex items-center gap-2 shrink-0">
                            <div :class="[
                                'w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold shrink-0 transition-colors',
                                currentStep === idx + 1 ? 'bg-emi-navy-500 text-white' :
                                currentStep > idx + 1  ? 'bg-success-500 text-white' :
                                                         'bg-slate-200 text-slate-500'
                            ]">
                                <svg v-if="currentStep > idx + 1" class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                                </svg>
                                <span v-else>{{ idx + 1 }}</span>
                            </div>
                            <span :class="[
                                'text-sm font-medium hidden sm:block',
                                currentStep === idx + 1 ? 'text-emi-navy-700' :
                                currentStep > idx + 1  ? 'text-success-600' :
                                                         'text-slate-400'
                            ]">{{ step.label }}</span>
                        </div>
                        <div v-if="idx < steps.length - 1" class="flex-1 h-px mx-3 min-w-4 transition-colors"
                            :class="currentStep > idx + 1 ? 'bg-success-400' : 'bg-slate-200'">
                        </div>
                    </template>
                </nav>

                <!-- Error de paso -->
                <div v-if="stepError" class="p-3 bg-amber-50 border border-amber-200 rounded-lg flex items-center gap-2">
                    <svg class="w-4 h-4 text-amber-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
                    </svg>
                    <p class="text-amber-700 text-sm">{{ stepError }}</p>
                </div>

                <!-- ═══════════════════════════════════════════════ -->
                <!-- PASO 1 — Información General                   -->
                <!-- ═══════════════════════════════════════════════ -->
                <template v-if="currentStep === 1">

                    <!-- ─── Detalle de la Oferta ─── -->
                    <div class="card-emi p-6">
                        <div class="flex items-center gap-3 mb-5">
                            <div class="w-9 h-9 bg-info-100 rounded-lg flex items-center justify-center shrink-0">
                                <svg class="w-5 h-5 text-info-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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
                                    :class="[
                                        'w-full px-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors',
                                        titleError ? 'border-danger-400 bg-danger-50' : 'border-slate-200'
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
                                    class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 resize-none transition-colors"
                                    placeholder="Describe las responsabilidades, el equipo de trabajo, los beneficios y el ambiente laboral..."
                                ></textarea>
                                <p class="text-xs text-slate-400 mt-1">
                                    Una descripcion completa atrae candidatos mas adecuados al perfil buscado.
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- ─── Empresa y Lugar de Trabajo ─── -->
                    <div class="card-emi p-6">
                        <div class="flex items-center gap-3 mb-5">
                            <div class="w-9 h-9 bg-success-100 rounded-lg flex items-center justify-center shrink-0">
                                <svg class="w-5 h-5 text-success-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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

                                <!-- Perfil seleccionado -->
                                <div v-if="selectedProfileName" class="flex items-center gap-2 px-3 py-2.5 border border-emi-navy-300 bg-emi-navy-50 rounded-lg">
                                    <svg class="w-4 h-4 text-emi-navy-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-2 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                                    </svg>
                                    <span class="flex-1 text-sm font-medium text-emi-navy-700">{{ selectedProfileName }}</span>
                                    <button type="button" @click="clearProfile" class="text-slate-400 hover:text-red-500 transition-colors" title="Quitar perfil">
                                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                        </svg>
                                    </button>
                                </div>

                                <!-- Buscador -->
                                <div v-else class="relative">
                                    <div class="relative">
                                        <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z" />
                                        </svg>
                                        <input
                                            v-model="profileSearch"
                                            type="text"
                                            placeholder="Buscar institución por nombre o sector..."
                                            class="w-full pl-9 pr-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors text-sm"
                                            @focus="profileDropdownOpen = true"
                                            @blur="setTimeout(() => { profileDropdownOpen = false }, 150)"
                                        />
                                    </div>

                                    <!-- Dropdown de resultados -->
                                    <div
                                        v-if="profileDropdownOpen"
                                        class="absolute z-20 mt-1 w-full bg-white border border-slate-200 rounded-lg shadow-lg max-h-52 overflow-y-auto"
                                    >
                                        <button
                                            v-for="profile in filteredProfiles"
                                            :key="profile.id"
                                            type="button"
                                            @mousedown.prevent="selectProfile(profile)"
                                            class="w-full text-left px-4 py-2.5 hover:bg-slate-50 flex items-center gap-3 border-b border-slate-100 last:border-0 transition-colors"
                                        >
                                            <div class="w-7 h-7 rounded-md bg-emi-navy-100 flex items-center justify-center shrink-0">
                                                <svg class="w-4 h-4 text-emi-navy-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-2 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                                                </svg>
                                            </div>
                                            <div class="min-w-0">
                                                <p class="text-sm font-medium text-slate-800 truncate">{{ profile.institution_name }}</p>
                                                <p class="text-xs text-slate-400 capitalize">{{ profile.sector }}</p>
                                            </div>
                                        </button>

                                        <div v-if="filteredProfiles.length === 0" class="px-4 py-4 text-center">
                                            <p class="text-sm text-slate-500 mb-3">
                                                No se encontró "{{ profileSearch }}"
                                            </p>
                                            <button
                                                type="button"
                                                @mousedown.prevent="router.push({ name: 'admin-profiles-new' })"
                                                class="inline-flex items-center gap-2 px-3 py-1.5 bg-emi-navy-600 hover:bg-emi-navy-700 text-white text-xs font-medium rounded-lg transition-colors"
                                            >
                                                <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                                                </svg>
                                                Crear perfil institucional
                                            </button>
                                        </div>
                                    </div>
                                </div>

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
                                        class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
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
                                        class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                                        placeholder="Ej: Desarrollo de Software, RRHH"
                                    />
                                    <button
                                        v-if="store.suggestions.area && form.area !== store.suggestions.area"
                                        type="button"
                                        @click="form.area = store.suggestions.area"
                                        class="mt-1 text-xs text-emi-navy-600 hover:text-emi-navy-800 flex items-center gap-1 transition-colors"
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

                </template>
                <!-- fin paso 1 -->

                <!-- ═══════════════════════════════════════════════ -->
                <!-- PASO 2 — Publicación y Contacto               -->
                <!-- ═══════════════════════════════════════════════ -->
                <template v-if="currentStep === 2">
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

                        <!-- ─── Publicación ─── -->
                        <div class="card-emi p-6">
                            <div class="flex items-center gap-3 mb-5">
                                <div class="w-9 h-9 bg-info-100 rounded-lg flex items-center justify-center shrink-0">
                                    <svg class="w-5 h-5 text-info-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                    </svg>
                                </div>
                                <div>
                                    <h2 class="text-base font-semibold text-slate-800">Publicación</h2>
                                    <p class="text-xs text-slate-400">Tipo, fechas y cupos disponibles</p>
                                </div>
                            </div>

                            <div class="space-y-4">
                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">Tipo de Oferta *</label>
                                    <select
                                        v-model="form.tipo"
                                        class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                                    >
                                        <option value="">Seleccionar...</option>
                                        <option value="pasantia">Pasantia</option>
                                        <option value="empleo">Empleo</option>
                                    </select>
                                </div>

                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">Modalidad</label>
                                    <select
                                        v-model="form.modalidad"
                                        class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                                    >
                                        <option value="">Seleccionar...</option>
                                        <option value="presencial">Presencial</option>
                                        <option value="remoto">Remoto</option>
                                        <option value="hibrido">Hibrido</option>
                                    </select>
                                </div>

                                <div class="grid grid-cols-2 gap-3">
                                    <div>
                                        <label class="block text-sm font-medium text-slate-700 mb-1">Desde</label>
                                        <input
                                            v-model="form.fecha_inicio"
                                            type="date"
                                            class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                                        />
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium text-slate-700 mb-1">Cierre</label>
                                        <input
                                            v-model="form.fecha_cierre"
                                            type="date"
                                            class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                                        />
                                    </div>
                                </div>

                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">Cupos Disponibles</label>
                                    <input
                                        v-model.number="form.cupos_disponibles"
                                        type="number"
                                        min="1"
                                        class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                                    />
                                </div>

                                <div v-if="isEditing" class="flex items-center gap-2 pt-1 border-t border-slate-100">
                                    <input
                                        v-model="form.is_active"
                                        type="checkbox"
                                        id="is_active"
                                        class="h-4 w-4 text-emi-navy-600 focus:ring-emi-navy-500 border-slate-300 rounded"
                                    />
                                    <label for="is_active" class="text-sm font-medium text-slate-700 cursor-pointer">
                                        Oferta activa y visible para candidatos
                                    </label>
                                </div>
                            </div>
                        </div>

                        <!-- ─── Contacto ─── -->
                        <div class="card-emi p-6">
                            <div class="flex items-center gap-3 mb-5">
                                <div class="w-9 h-9 bg-info-100 rounded-lg flex items-center justify-center shrink-0">
                                    <svg class="w-5 h-5 text-info-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                    </svg>
                                </div>
                                <div>
                                    <h2 class="text-base font-semibold text-slate-800">Contacto</h2>
                                    <p class="text-xs text-slate-400">Para consultas de candidatos</p>
                                </div>
                            </div>

                            <div v-if="store.loadingSuggestions" class="flex items-center gap-2 mb-3 text-xs text-slate-400">
                                <div class="animate-spin rounded-full h-3 w-3 border-b-2 border-emi-gold"></div>
                                Buscando datos previos de la empresa...
                            </div>

                            <div class="space-y-4">
                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">Telefono</label>
                                    <input
                                        v-model="form.contact_phone"
                                        type="tel"
                                        class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                                        placeholder="+591 2 1234567"
                                    />
                                    <button
                                        v-if="store.suggestions.contact_phone && form.contact_phone !== store.suggestions.contact_phone"
                                        type="button"
                                        @click="form.contact_phone = store.suggestions.contact_phone"
                                        class="mt-1 text-xs text-emi-navy-600 hover:text-emi-navy-800 flex items-center gap-1 transition-colors"
                                    >
                                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                                        </svg>
                                        Usar ultimo: {{ store.suggestions.contact_phone }}
                                    </button>
                                </div>

                                <div>
                                    <label class="block text-sm font-medium text-slate-700 mb-1">Correo Electronico</label>
                                    <input
                                        v-model="form.contact_email"
                                        type="email"
                                        class="w-full px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                                        placeholder="rrhh@empresa.com"
                                    />
                                    <button
                                        v-if="store.suggestions.contact_email && form.contact_email !== store.suggestions.contact_email"
                                        type="button"
                                        @click="form.contact_email = store.suggestions.contact_email"
                                        class="mt-1 text-xs text-emi-navy-600 hover:text-emi-navy-800 flex items-center gap-1 transition-colors"
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
                </template>
                <!-- fin paso 2 -->

                <!-- ═══════════════════════════════════════════════ -->
                <!-- PASO 3 — Criterios de Evaluación              -->
                <!-- ═══════════════════════════════════════════════ -->
                <template v-if="currentStep === 3">
                    <div class="card-emi p-6">
                        <div class="flex items-center gap-3 mb-6">
                            <div class="w-9 h-9 bg-warning-100 rounded-lg flex items-center justify-center shrink-0">
                                <svg class="w-5 h-5 text-warning-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                                </svg>
                            </div>
                            <div>
                                <h2 class="text-base font-semibold text-slate-800">Configuracion de Evaluacion</h2>
                                <p class="text-xs text-slate-400">Criterios para evaluar y clasificar a los candidatos que postulen</p>
                            </div>
                        </div>

                        <div class="space-y-8">

                            <!-- ── 1. Requisitos Mínimos ── -->
                            <div>
                                <div class="flex items-center gap-2 mb-4">
                                    <span class="w-6 h-6 rounded-full bg-emi-navy-500 text-white text-xs flex items-center justify-center font-bold shrink-0">1</span>
                                    <div>
                                        <h3 class="text-sm font-semibold text-slate-700">Requisitos Minimos</h3>
                                        <p class="text-xs text-slate-400">Condiciones que el candidato debe cumplir para ser evaluado</p>
                                    </div>
                                </div>

                                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
                                    <div>
                                        <label class="block text-xs font-medium text-slate-600 mb-1">Experiencia minima (años)</label>
                                        <input
                                            v-model.number="form.requirements.min_experience_years"
                                            type="number" min="0" step="0.5"
                                            placeholder="0"
                                            class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                                        />
                                    </div>
                                    <div>
                                        <label class="block text-xs font-medium text-slate-600 mb-1">Nivel educativo minimo</label>
                                        <select
                                            v-model="form.requirements.required_education_level"
                                            class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                                        >
                                            <option v-for="lvl in educationLevels" :key="lvl" :value="lvl">{{ lvl }}</option>
                                        </select>
                                    </div>
                                </div>

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
                                                class="flex-1 px-2.5 py-1.5 border border-slate-200 rounded-md text-xs bg-white focus:ring-1 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                                            />
                                            <button type="button" @click="addRequiredSkill"
                                                class="px-2.5 py-1.5 bg-emi-navy-500 text-white text-xs rounded-md hover:bg-emi-navy-600 font-medium transition-colors">+</button>
                                        </div>
                                        <div class="flex flex-wrap gap-1.5 min-h-6">
                                            <span
                                                v-for="skill in form.requirements.required_skills" :key="skill"
                                                class="inline-flex items-center px-2 py-0.5 bg-emi-navy-100 text-emi-navy-700 rounded-full text-xs"
                                            >
                                                {{ skill }}
                                                <button type="button" @click="removeSkill('required_skills', skill)"
                                                    class="ml-1 hover:text-emi-navy-900 leading-none">&times;</button>
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
                                                class="flex-1 px-2.5 py-1.5 border border-slate-200 rounded-md text-xs bg-white focus:ring-1 focus:ring-info-500 focus:border-info-500 transition-colors"
                                            />
                                            <button type="button" @click="addSoftSkill"
                                                class="px-2.5 py-1.5 bg-info-500 text-white text-xs rounded-md hover:bg-info-600 font-medium transition-colors">+</button>
                                        </div>
                                        <div class="flex flex-wrap gap-1.5 min-h-6">
                                            <span
                                                v-for="skill in form.requirements.required_soft_skills" :key="skill"
                                                class="inline-flex items-center px-2 py-0.5 bg-info-100 text-info-700 rounded-full text-xs"
                                            >
                                                {{ skill }}
                                                <button type="button" @click="removeSkill('required_soft_skills', skill)"
                                                    class="ml-1 hover:text-info-900 leading-none">&times;</button>
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
                                                class="flex-1 px-2.5 py-1.5 border border-slate-200 rounded-md text-xs bg-white focus:ring-1 focus:ring-success-500 focus:border-success-500 transition-colors"
                                            />
                                            <button type="button" @click="addLanguage"
                                                class="px-2.5 py-1.5 bg-slate-300 text-slate-700 text-xs rounded-md hover:bg-slate-400 font-medium">+</button>
                                        </div>
                                        <div class="flex flex-wrap gap-1.5 min-h-6">
                                            <span
                                                v-for="lang in form.requirements.required_languages" :key="lang"
                                                class="inline-flex items-center px-2 py-0.5 bg-success-100 text-success-700 rounded-full text-xs"
                                            >
                                                {{ lang }}
                                                <button type="button" @click="removeSkill('required_languages', lang)"
                                                    class="ml-1 hover:text-success-900 leading-none">&times;</button>
                                            </span>
                                            <span v-if="form.requirements.required_languages.length === 0"
                                                class="text-xs text-slate-400 italic">Ninguno aun</span>
                                        </div>
                                    </div>
                                </div>

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

                            <!-- ── 2. Elegibilidad ── -->
                            <div class="border-t border-slate-100 pt-6">
                                <div class="flex items-center gap-2 mb-4">
                                    <span class="w-6 h-6 rounded-full bg-emi-navy-500 text-white text-xs flex items-center justify-center font-bold shrink-0">2</span>
                                    <div>
                                        <h3 class="text-sm font-semibold text-slate-700">Filtro de Elegibilidad</h3>
                                        <p class="text-xs text-slate-400">Pre-filtro binario: candidatos que no cumplan estos criterios quedan como NO_APTO sin pasar por el modelo ML</p>
                                    </div>
                                </div>

                                <div class="space-y-4">
                                    <div>
                                        <label class="block text-xs font-semibold text-slate-600 mb-2">
                                            Carreras Aceptadas
                                            <span class="font-normal text-slate-400 ml-1">(dejar vacío = todas las carreras)</span>
                                        </label>
                                        <div class="flex flex-wrap gap-2">
                                            <button
                                                v-for="carrera in emiCarreras"
                                                :key="carrera"
                                                type="button"
                                                @click="toggleCarrera(carrera)"
                                                :class="[
                                                    'px-3 py-1.5 rounded-full text-xs font-medium border transition-colors',
                                                    form.requirements.carreras_aceptadas.includes(carrera)
                                                        ? 'bg-emi-navy-500 text-white border-emi-navy-500'
                                                        : 'bg-white text-slate-600 border-slate-300 hover:border-emi-navy-400'
                                                ]"
                                            >
                                                {{ carrera }}
                                            </button>
                                        </div>
                                        <p v-if="form.requirements.carreras_aceptadas.length === 0" class="mt-1.5 text-xs text-slate-400 italic">
                                            Ninguna seleccionada — se aceptan candidatos de cualquier carrera
                                        </p>
                                    </div>

                                    <div v-if="form.tipo === 'pasantia'">
                                        <label class="block text-xs font-semibold text-slate-600 mb-2">
                                            Rango de Semestre
                                            <span class="font-normal text-slate-400 ml-1">(solo aplica a estudiantes activos)</span>
                                        </label>
                                        <div class="flex items-center gap-3">
                                            <div class="flex items-center gap-2">
                                                <label class="text-xs text-slate-500 whitespace-nowrap">Desde semestre</label>
                                                <input
                                                    v-model.number="form.requirements.semestre_minimo"
                                                    type="number" min="1" max="10"
                                                    placeholder="—"
                                                    class="w-20 px-3 py-2 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                                                />
                                            </div>
                                            <span class="text-slate-400 text-xs">hasta</span>
                                            <div class="flex items-center gap-2">
                                                <input
                                                    v-model.number="form.requirements.semestre_maximo"
                                                    type="number" min="1" max="10"
                                                    placeholder="—"
                                                    class="w-20 px-3 py-2 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                                                />
                                                <label class="text-xs text-slate-500 whitespace-nowrap">semestre</label>
                                            </div>
                                            <button
                                                v-if="form.requirements.semestre_minimo || form.requirements.semestre_maximo"
                                                type="button"
                                                @click="form.requirements.semestre_minimo = null; form.requirements.semestre_maximo = null"
                                                class="text-xs text-red-500 hover:text-red-700 transition-colors"
                                            >
                                                Limpiar
                                            </button>
                                        </div>
                                        <p class="mt-1 text-xs text-slate-400">
                                            Ejemplo: "7 hasta —" para desde 7mo semestre sin límite superior. Titulados ignoran este filtro.
                                        </p>
                                    </div>
                                    <p v-else class="text-xs text-slate-400 italic">
                                        El filtro de semestre solo aplica a ofertas de tipo Pasantia.
                                    </p>
                                </div>
                            </div>

                            <!-- ── 3 + 4. Pesos y Umbrales ── -->
                            <div class="border-t border-slate-100 pt-6">
                                <div class="flex items-center gap-2 mb-4">
                                    <span class="w-6 h-6 rounded-full bg-emi-navy-500 text-white text-xs flex items-center justify-center font-bold shrink-0">3</span>
                                    <div>
                                        <h3 class="text-sm font-semibold text-slate-700">Pesos y Umbrales de Evaluacion</h3>
                                        <p class="text-xs text-slate-400">Importancia de cada dimension y puntuacion minima por categoria</p>
                                    </div>
                                </div>

                                <!-- ── Panel estándar (colapsado) ── -->
                                <div v-if="!useCustomEvaluation" class="border border-slate-200 rounded-xl p-5 bg-slate-50">
                                    <div class="flex items-start justify-between gap-4 mb-4">
                                        <div class="flex items-center gap-2">
                                            <div class="w-6 h-6 rounded-full bg-success-100 flex items-center justify-center shrink-0">
                                                <svg class="w-3.5 h-3.5 text-success-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                                                </svg>
                                            </div>
                                            <span class="text-sm font-semibold text-slate-700">Configuracion estandar recomendada</span>
                                        </div>
                                        <button
                                            type="button"
                                            @click="useCustomEvaluation = true"
                                            class="text-xs text-emi-navy-600 hover:text-emi-navy-800 underline whitespace-nowrap transition-colors shrink-0"
                                        >
                                            Personalizar
                                        </button>
                                    </div>

                                    <!-- Chips de pesos -->
                                    <div class="grid grid-cols-2 sm:grid-cols-5 gap-2 mb-4">
                                        <div
                                            v-for="[key, label] in [
                                                ['hard_skills', 'Técnicas'],
                                                ['soft_skills', 'Blandas'],
                                                ['experience', 'Experiencia'],
                                                ['education', 'Educación'],
                                                ['languages', 'Idiomas']
                                            ]"
                                            :key="key"
                                            class="text-center bg-white rounded-lg border border-slate-200 py-2.5 px-2"
                                        >
                                            <p class="text-xs text-slate-400 mb-0.5">{{ label }}</p>
                                            <p class="text-sm font-bold text-emi-navy-700">{{ (form.weights[key] * 100).toFixed(0) }}%</p>
                                        </div>
                                    </div>

                                    <!-- Chips de umbrales -->
                                    <div class="flex flex-wrap items-center gap-2 mb-4">
                                        <span class="text-xs px-2.5 py-1 bg-success-100 text-success-700 rounded-full font-medium">
                                            APTO ≥ {{ (form.thresholds.apto * 100).toFixed(0) }}%
                                        </span>
                                        <span class="text-xs px-2.5 py-1 bg-warning-100 text-warning-700 rounded-full font-medium">
                                            CONSIDERADO ≥ {{ (form.thresholds.considerado * 100).toFixed(0) }}%
                                        </span>
                                        <span class="text-xs px-2.5 py-1 bg-slate-100 text-slate-500 rounded-full font-medium">
                                            NO APTO &lt; {{ (form.thresholds.considerado * 100).toFixed(0) }}%
                                        </span>
                                    </div>

                                    <!-- Justificación -->
                                    <div class="flex items-start gap-2 text-xs text-slate-400">
                                        <svg class="w-3.5 h-3.5 mt-0.5 shrink-0 text-info-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                        </svg>
                                        Valores calibrados para el sistema ICONDORIC. Representan el balance recomendado para la mayoria de ofertas. Personaliza solo si el perfil de evaluacion de esta oferta es muy especifico.
                                    </div>
                                </div>

                                <!-- ── Panel personalizado (expandido) ── -->
                                <div v-else class="border border-emi-navy-200 rounded-xl p-5 bg-white">
                                    <div class="flex items-center justify-between mb-5">
                                        <span class="text-sm font-semibold text-slate-700">Configuracion personalizada</span>
                                        <button
                                            type="button"
                                            @click="resetToDefaultEvaluation"
                                            class="text-xs text-slate-500 hover:text-slate-700 underline transition-colors"
                                        >
                                            Volver a estandar
                                        </button>
                                    </div>

                                    <div class="grid grid-cols-1 lg:grid-cols-5 gap-8">

                                        <!-- Pesos (3/5) -->
                                        <div class="lg:col-span-3">
                                            <div class="flex items-center justify-between mb-1">
                                                <h4 class="text-xs font-semibold text-slate-600">Pesos de Evaluacion</h4>
                                                <div class="flex items-center gap-3">
                                                    <span :class="[
                                                        'text-xs font-semibold px-2 py-0.5 rounded-full',
                                                        isWeightsValid ? 'bg-success-100 text-success-700' : 'bg-danger-100 text-danger-700'
                                                    ]">
                                                        {{ (weightsSum * 100).toFixed(0) }}%
                                                    </span>
                                                    <button type="button" @click="normalizeWeights"
                                                        class="text-xs text-emi-navy-600 hover:text-emi-navy-800 underline transition-colors">
                                                        Normalizar a 100%
                                                    </button>
                                                </div>
                                            </div>
                                            <p class="text-xs text-slate-400 mb-4">
                                                Cuanto vale cada dimension al calcular la puntuacion final. Debe sumar exactamente 100%.
                                            </p>

                                            <div class="space-y-3">
                                                <div
                                                    v-for="[key, label] in [
                                                        ['hard_skills', 'Habilidades Tecnicas'],
                                                        ['soft_skills', 'Habilidades Blandas'],
                                                        ['experience', 'Experiencia Laboral'],
                                                        ['education', 'Nivel Educativo'],
                                                        ['languages', 'Idiomas']
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
                                                        class="w-full h-1.5 bg-slate-200 rounded-full appearance-none cursor-pointer accent-emi-navy-500"
                                                    />
                                                </div>
                                            </div>
                                        </div>

                                        <!-- Umbrales (2/5) -->
                                        <div class="lg:col-span-2">
                                            <h4 class="text-xs font-semibold text-slate-600 mb-1">Umbrales de Clasificacion</h4>
                                            <p class="text-xs text-slate-400 mb-4">
                                                Puntuacion minima para asignar cada categoria al candidato.
                                            </p>

                                            <div v-if="!isThresholdsValid" class="mb-3 p-2.5 rounded-lg text-xs bg-danger-50 border border-danger-200 text-danger-700">
                                                El umbral APTO debe ser mayor que CONSIDERADO.
                                            </div>

                                            <div class="space-y-3">
                                                <div class="bg-success-50 border border-success-200 rounded-lg p-4">
                                                    <div class="flex items-center justify-between mb-2">
                                                        <span class="text-xs font-bold text-success-700 uppercase tracking-wide">APTO</span>
                                                        <span class="text-xs text-success-600">Score &ge; {{ (form.thresholds.apto * 100).toFixed(0) }}%</span>
                                                    </div>
                                                    <input
                                                        v-model.number="form.thresholds.apto"
                                                        type="number" min="0" max="1" step="0.05"
                                                        class="w-full px-3 py-1.5 border border-success-300 rounded-lg text-sm bg-white focus:ring-2 focus:ring-success-500 transition-colors"
                                                    />
                                                </div>

                                                <div class="bg-warning-50 border border-warning-200 rounded-lg p-4">
                                                    <div class="flex items-center justify-between mb-2">
                                                        <span class="text-xs font-bold text-warning-700 uppercase tracking-wide">CONSIDERADO</span>
                                                        <span class="text-xs text-warning-600">Score &ge; {{ (form.thresholds.considerado * 100).toFixed(0) }}%</span>
                                                    </div>
                                                    <input
                                                        v-model.number="form.thresholds.considerado"
                                                        type="number" min="0" max="1" step="0.05"
                                                        class="w-full px-3 py-1.5 border border-warning-300 rounded-lg text-sm bg-white focus:ring-2 focus:ring-warning-500 transition-colors"
                                                    />
                                                </div>

                                                <div class="bg-slate-100 border border-slate-200 rounded-lg p-3 text-center">
                                                    <span class="text-xs font-bold text-slate-500 uppercase tracking-wide">NO APTO</span>
                                                    <p class="text-xs text-slate-400 mt-0.5">Menos de {{ (form.thresholds.considerado * 100).toFixed(0) }}%</p>
                                                </div>
                                            </div>
                                        </div>

                                    </div>
                                </div>
                                <!-- fin pesos y umbrales -->

                            </div>
                            <!-- fin sección 3 -->

                        </div>
                    </div>
                </template>
                <!-- fin paso 3 -->

                <!-- ─── Navegación de pasos ─── -->
                <div class="flex justify-between gap-3 pt-2">
                    <!-- Izquierda -->
                    <div>
                        <router-link
                            v-if="currentStep === 1"
                            to="/admin/ofertas"
                            class="px-6 py-2.5 text-sm text-slate-600 hover:text-slate-800 font-medium rounded-lg border border-slate-200 hover:bg-slate-50 transition-colors"
                        >
                            Cancelar
                        </router-link>
                        <button
                            v-else
                            type="button"
                            @click="goPrev"
                            class="px-6 py-2.5 text-sm text-slate-600 hover:text-slate-800 font-medium rounded-lg border border-slate-200 hover:bg-slate-50 transition-colors inline-flex items-center gap-2"
                        >
                            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                            </svg>
                            Anterior
                        </button>
                    </div>

                    <!-- Derecha -->
                    <div>
                        <button
                            v-if="currentStep < 3"
                            type="button"
                            @click="goNext"
                            class="px-8 py-2.5 rounded-lg font-semibold text-white text-sm bg-emi-navy-600 hover:bg-emi-navy-700 hover:shadow-md transition-all inline-flex items-center gap-2"
                        >
                            Siguiente
                            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                            </svg>
                        </button>
                        <button
                            v-else
                            type="submit"
                            :disabled="saving || !isWeightsValid"
                            :class="[
                                'px-8 py-2.5 rounded-lg font-semibold text-white text-sm transition-all',
                                (saving || !isWeightsValid)
                                    ? 'bg-slate-300 cursor-not-allowed'
                                    : 'bg-emi-navy-600 hover:bg-emi-navy-700 hover:shadow-md'
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
                </div>

            </form>
        </div>
    </AppLayout>
</template>

<style scoped>
input[type="range"] { -webkit-appearance: none; appearance: none; }
input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none; appearance: none;
    height: 14px; width: 14px;
    border-radius: 50%;
    background: #193f77; /* emi-navy-500 */
    cursor: pointer;
    margin-top: -5px;
}
input[type="range"]::-moz-range-thumb {
    height: 14px; width: 14px;
    border-radius: 50%;
    background: #193f77; /* emi-navy-500 */
    cursor: pointer;
    border: none;
}
</style>
