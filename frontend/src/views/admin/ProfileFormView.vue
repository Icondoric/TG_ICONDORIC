<script setup>
/**
 * ProfileFormView - Fase 7
 * Vista para crear/editar perfiles institucionales
 */

import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMLStore } from '../../stores/ml'
import { useAuthStore } from '../../stores/auth'
import AdminLayout from '../../components/admin/AdminLayout.vue'

const route = useRoute()
const router = useRouter()
const mlStore = useMLStore()
const authStore = useAuthStore()

// Estado local
const isLoading = ref(false)
const isSaving = ref(false)
const error = ref(null)

// Formulario
const form = ref({
    institution_name: '',
    sector: '',
    description: '',
    weights: {
        hard_skills: 0.30,
        soft_skills: 0.20,
        experience: 0.25,
        education: 0.15,
        languages: 0.10
    },
    requirements: {
        min_experience_years: 0,
        required_skills: [],
        preferred_skills: [],
        required_education_level: 'Licenciatura',
        required_languages: []
    },
    thresholds: {
        apto: 0.70,
        considerado: 0.50
    }
})

// Para edicion
const isEditMode = computed(() => !!route.params.id)
const profileId = computed(() => route.params.id)

// Skills temporales y custom inputs
const newRequiredSkill = ref('')
const newPreferredSkill = ref('')
const newLanguage = ref('')
const customSector = ref('')

// Opciones
const educationLevels = [
    'Bachillerato',
    'Tecnico',
    'Licenciatura',
    'Maestria',
    'Doctorado'
]

const sectorOptions = [
    'Tecnologia',
    'Finanzas',
    'Salud',
    'Educacion',
    'Construccion',
    'Comercio',
    'Servicios',
    'Industria',
    'Gobierno',
    'ONG',
    'Otro'
]

// Listas comunes para autocompletado
const commonSkills = [
    'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'SQL', 'NoSQL',
    'React', 'Vue.js', 'Angular', 'Node.js', 'Django', 'FastAPI', 'Spring Boot',
    'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP',
    'Machine Learning', 'Data Analysis', 'Project Management', 'Scrum', 'Agile',
    'Communication', 'Leadership', 'Teamwork', 'Problem Solving', 'Critical Thinking'
]

const commonLanguages = [
    'Español (Nativo)', 'Español (Avanzado)',
    'Inglés (A1)', 'Inglés (A2)', 'Inglés (B1)', 'Inglés (B2)', 'Inglés (C1)', 'Inglés (C2)',
    'Francés (B1)', 'Francés (B2)',
    'Portugués (B1)', 'Portugués (B2)',
    'Aymara (Básico)', 'Quechua (Básico)'
]

// Computed
const weightsSum = computed(() => {
    const weights = form.value.weights
    return Object.values(weights).reduce((a, b) => a + b, 0)
})

const isWeightsValid = computed(() => {
    return Math.abs(weightsSum.value - 1.0) < 0.01
})

const isThresholdsValid = computed(() => {
    return form.value.thresholds.apto > form.value.thresholds.considerado
})

const canSave = computed(() => {
    const isSectorValid = form.value.sector === 'Otro' ? customSector.value.trim().length > 0 : !!form.value.sector
    
    return form.value.institution_name.trim() &&
           isSectorValid &&
           isWeightsValid.value &&
           isThresholdsValid.value &&
           !isSaving.value
})

// Cargar datos si es edicion
onMounted(async () => {
    if (!authStore.isAdmin) {
        router.push('/dashboard')
        return
    }

    if (isEditMode.value) {
        isLoading.value = true
        try {
            await mlStore.loadProfile(profileId.value)
            if (mlStore.currentProfile) {
                // Poblar formulario
                form.value.institution_name = mlStore.currentProfile.institution_name
                
                // Manejo de Sector Personalizado
                const loadedSector = mlStore.currentProfile.sector
                if (sectorOptions.includes(loadedSector)) {
                    form.value.sector = loadedSector
                } else {
                    form.value.sector = 'Otro'
                    customSector.value = loadedSector
                }

                form.value.description = mlStore.currentProfile.description || ''
                form.value.weights = { ...mlStore.currentProfile.weights }
                form.value.requirements = { ...mlStore.currentProfile.requirements }
                form.value.thresholds = { ...mlStore.currentProfile.thresholds }

                // Asegurar que arrays existan
                if (!form.value.requirements.required_skills) form.value.requirements.required_skills = []
                if (!form.value.requirements.preferred_skills) form.value.requirements.preferred_skills = []
                if (!form.value.requirements.required_languages) form.value.requirements.required_languages = []
            }
        } catch (err) {
            error.value = 'Error cargando perfil'
        } finally {
            isLoading.value = false
        }
    }
})

// Methods
const addRequiredSkill = () => {
    const skill = newRequiredSkill.value.trim()
    if (skill && !form.value.requirements.required_skills.includes(skill)) {
        form.value.requirements.required_skills.push(skill)
        newRequiredSkill.value = ''
    }
}

const removeRequiredSkill = (skill) => {
    form.value.requirements.required_skills = form.value.requirements.required_skills.filter(s => s !== skill)
}

const addPreferredSkill = () => {
    const skill = newPreferredSkill.value.trim()
    if (skill && !form.value.requirements.preferred_skills.includes(skill)) {
        form.value.requirements.preferred_skills.push(skill)
        newPreferredSkill.value = ''
    }
}

const removePreferredSkill = (skill) => {
    form.value.requirements.preferred_skills = form.value.requirements.preferred_skills.filter(s => s !== skill)
}

const addLanguage = () => {
    const lang = newLanguage.value.trim()
    if (lang && !form.value.requirements.required_languages.includes(lang)) {
        form.value.requirements.required_languages.push(lang)
        newLanguage.value = ''
    }
}

const removeLanguage = (lang) => {
    form.value.requirements.required_languages = form.value.requirements.required_languages.filter(l => l !== lang)
}

const normalizeWeights = () => {
    const sum = weightsSum.value
    if (sum > 0) {
        const weights = form.value.weights
        for (const key in weights) {
            weights[key] = Math.round((weights[key] / sum) * 100) / 100
        }
        // Ajustar ultimo para que sume exactamente 1
        const newSum = Object.values(weights).reduce((a, b) => a + b, 0)
        weights.languages = Math.round((weights.languages + (1 - newSum)) * 100) / 100
    }
}

const save = async () => {
    if (!canSave.value) return

    isSaving.value = true
    error.value = null

    try {
        // Determinar sector final
        const finalSector = form.value.sector === 'Otro' ? customSector.value.trim() : form.value.sector

        const data = {
            institution_name: form.value.institution_name.trim(),
            sector: finalSector,
            description: form.value.description.trim() || null,
            weights: form.value.weights,
            requirements: form.value.requirements,
            thresholds: form.value.thresholds
        }

        if (isEditMode.value) {
            await mlStore.updateProfileAction(profileId.value, data)
        } else {
            await mlStore.createProfileAction(data)
        }

        router.push('/admin/profiles')
    } catch (err) {
        error.value = err.response?.data?.detail || 'Error guardando perfil'
    } finally {
        isSaving.value = false
    }
}

const cancel = () => {
    router.push('/admin/profiles')
}
</script>

<template>
    <AdminLayout>
        <div class="max-w-4xl mx-auto py-8 px-4">
            <!-- Header -->
            <header class="mb-8">
                <button
                    @click="cancel"
                    class="flex items-center text-slate-600 hover:text-slate-800 mb-4"
                >
                    <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                    Volver
                </button>
                <h1 class="text-3xl font-bold text-slate-800">
                    {{ isEditMode ? 'Editar Perfil' : 'Nuevo Perfil' }}
                </h1>
                <p class="mt-2 text-slate-600">
                    {{ isEditMode ? 'Modifica los datos del perfil institucional' : 'Crea un nuevo perfil institucional para el sistema de matching' }}
                </p>
            </header>

            <!-- Loading -->
            <div v-if="isLoading" class="bg-white rounded-xl shadow-md p-8 text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p class="mt-4 text-slate-500">Cargando perfil...</p>
            </div>

            <!-- Formulario -->
            <form v-else @submit.prevent="save" class="space-y-6">
                <!-- Error -->
                <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
                    <p class="text-red-700">{{ error }}</p>
                </div>

                <!-- Informacion Basica -->
                <div class="bg-white rounded-xl shadow-md p-6">
                    <h2 class="text-lg font-semibold text-slate-800 mb-4">
                        Informacion Basica
                    </h2>

                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">
                                Nombre de la Institucion *
                            </label>
                            <input
                                v-model="form.institution_name"
                                type="text"
                                required
                                class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                placeholder="Ej: TechBolivia Startup"
                            />
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">
                                Sector *
                            </label>
                            <select
                                v-model="form.sector"
                                required
                                class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            >
                                <option value="">Selecciona un sector</option>
                                <option v-for="sector in sectorOptions" :key="sector" :value="sector">
                                    {{ sector }}
                                </option>
                            </select>
                            
                            <!-- Input para sector personalizado -->
                            <div v-if="form.sector === 'Otro'" class="mt-3">
                                <label class="block text-sm font-medium text-slate-700 mb-1">
                                    Especificar Sector *
                                </label>
                                <input
                                    v-model="customSector"
                                    type="text"
                                    required
                                    placeholder="Ej: Biotecnología"
                                    class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-slate-50"
                                />
                            </div>
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">
                                Descripcion
                            </label>
                            <textarea
                                v-model="form.description"
                                rows="3"
                                class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                placeholder="Descripcion breve de la institucion..."
                            ></textarea>
                        </div>
                    </div>
                </div>

                <!-- Pesos -->
                <div class="bg-white rounded-xl shadow-md p-6">
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-lg font-semibold text-slate-800">
                            Pesos de Evaluacion
                        </h2>
                        <button
                            type="button"
                            @click="normalizeWeights"
                            class="text-sm text-blue-600 hover:text-blue-800"
                        >
                            Normalizar a 100%
                        </button>
                    </div>

                    <p class="text-sm text-slate-500 mb-4">
                        Define la importancia de cada dimension en la evaluacion (deben sumar 100%)
                    </p>

                    <!-- Validacion -->
                    <div
                        :class="[
                            'mb-4 p-3 rounded-lg text-sm',
                            isWeightsValid ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
                        ]"
                    >
                        Total: {{ (weightsSum * 100).toFixed(0) }}%
                        {{ isWeightsValid ? '(Valido)' : '(Debe sumar 100%)' }}
                    </div>

                    <div class="space-y-4">
                        <div v-for="(value, key) in form.weights" :key="key">
                            <div class="flex justify-between items-center mb-1">
                                <label class="text-sm font-medium text-slate-700 capitalize">
                                    {{ key.replace('_', ' ') }}
                                </label>
                                <span class="text-sm text-slate-500">{{ (value * 100).toFixed(0) }}%</span>
                            </div>
                            <input
                                v-model.number="form.weights[key]"
                                type="range"
                                min="0"
                                max="1"
                                step="0.05"
                                class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
                            />
                        </div>
                    </div>
                </div>

                <!-- Umbrales -->
                <div class="bg-white rounded-xl shadow-md p-6">
                    <h2 class="text-lg font-semibold text-slate-800 mb-4">
                        Umbrales de Clasificacion
                    </h2>

                    <!-- Validacion -->
                    <div
                        v-if="!isThresholdsValid"
                        class="mb-4 p-3 rounded-lg text-sm bg-red-50 text-red-700"
                    >
                        El umbral de APTO debe ser mayor que el de CONSIDERADO
                    </div>

                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">
                                Umbral APTO (%)
                            </label>
                            <input
                                v-model.number="form.thresholds.apto"
                                type="number"
                                min="0"
                                max="1"
                                step="0.05"
                                class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            />
                            <p class="text-xs text-slate-400 mt-1">
                                Score minimo para ser APTO: {{ (form.thresholds.apto * 100).toFixed(0) }}%
                            </p>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">
                                Umbral CONSIDERADO (%)
                            </label>
                            <input
                                v-model.number="form.thresholds.considerado"
                                type="number"
                                min="0"
                                max="1"
                                step="0.05"
                                class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            />
                            <p class="text-xs text-slate-400 mt-1">
                                Score minimo para ser CONSIDERADO: {{ (form.thresholds.considerado * 100).toFixed(0) }}%
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Requisitos -->
                <div class="bg-white rounded-xl shadow-md p-6">
                    <h2 class="text-lg font-semibold text-slate-800 mb-4">
                        Requisitos
                    </h2>

                    <div class="space-y-6">
                        <!-- Experiencia Minima -->
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">
                                Experiencia Minima (anos)
                            </label>
                            <input
                                v-model.number="form.requirements.min_experience_years"
                                type="number"
                                min="0"
                                step="0.5"
                                class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            />
                        </div>

                        <!-- Nivel Educativo -->
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">
                                Nivel Educativo Minimo
                            </label>
                            <select
                                v-model="form.requirements.required_education_level"
                                class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            >
                                <option v-for="level in educationLevels" :key="level" :value="level">
                                    {{ level }}
                                </option>
                            </select>
                        </div>

                        <!-- Skills Requeridas -->
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">
                                Habilidades Requeridas
                            </label>
                            <div class="flex gap-2 mb-2">
                                <input
                                    v-model="newRequiredSkill"
                                    @keyup.enter.prevent="addRequiredSkill"
                                    type="text"
                                    list="skillsList"
                                    placeholder="Agregar habilidad..."
                                    class="flex-1 px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                />
                                <button
                                    type="button"
                                    @click="addRequiredSkill"
                                    class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                                >
                                    Agregar
                                </button>
                            </div>
                            <div class="flex flex-wrap gap-2">
                                <span
                                    v-for="skill in form.requirements.required_skills"
                                    :key="skill"
                                    class="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm"
                                >
                                    {{ skill }}
                                    <button type="button" @click="removeRequiredSkill(skill)" class="ml-2 hover:text-blue-900">
                                        &times;
                                    </button>
                                </span>
                            </div>
                        </div>

                        <!-- Skills Preferidas -->
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">
                                Habilidades Preferidas
                            </label>
                            <div class="flex gap-2 mb-2">
                                <input
                                    v-model="newPreferredSkill"
                                    @keyup.enter.prevent="addPreferredSkill"
                                    type="text"
                                    list="skillsList"
                                    placeholder="Agregar habilidad..."
                                    class="flex-1 px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                />
                                <button
                                    type="button"
                                    @click="addPreferredSkill"
                                    class="px-4 py-2 bg-slate-200 text-slate-700 rounded-lg hover:bg-slate-300"
                                >
                                    Agregar
                                </button>
                            </div>
                            <div class="flex flex-wrap gap-2">
                                <span
                                    v-for="skill in form.requirements.preferred_skills"
                                    :key="skill"
                                    class="inline-flex items-center px-3 py-1 bg-slate-100 text-slate-700 rounded-full text-sm"
                                >
                                    {{ skill }}
                                    <button type="button" @click="removePreferredSkill(skill)" class="ml-2 hover:text-slate-900">
                                        &times;
                                    </button>
                                </span>
                            </div>
                        </div>

                        <!-- Idiomas -->
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">
                                Idiomas Requeridos
                            </label>
                            <div class="flex gap-2 mb-2">
                                <input
                                    v-model="newLanguage"
                                    @keyup.enter.prevent="addLanguage"
                                    type="text"
                                    list="languagesList"
                                    placeholder="Ej: Ingles (B2)..."
                                    class="flex-1 px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                />
                                <button
                                    type="button"
                                    @click="addLanguage"
                                    class="px-4 py-2 bg-slate-200 text-slate-700 rounded-lg hover:bg-slate-300"
                                >
                                    Agregar
                                </button>
                            </div>
                            <div class="flex flex-wrap gap-2">
                                <span
                                    v-for="lang in form.requirements.required_languages"
                                    :key="lang"
                                    class="inline-flex items-center px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm"
                                >
                                    {{ lang }}
                                    <button type="button" @click="removeLanguage(lang)" class="ml-2 hover:text-green-900">
                                        &times;
                                    </button>
                                </span>
                            </div>
                        </div>

                        <!-- Datalists -->
                        <datalist id="skillsList">
                            <option v-for="skill in commonSkills" :key="skill" :value="skill" />
                        </datalist>
                        <datalist id="languagesList">
                            <option v-for="lang in commonLanguages" :key="lang" :value="lang" />
                        </datalist>
                    </div>
                </div>

                <!-- Botones de Accion -->
                <div class="flex justify-end gap-4">
                    <button
                        type="button"
                        @click="cancel"
                        class="px-6 py-3 text-slate-600 hover:text-slate-800 font-medium"
                    >
                        Cancelar
                    </button>
                    <button
                        type="submit"
                        :disabled="!canSave"
                        :class="[
                            'px-8 py-3 rounded-lg font-semibold text-white transition-all',
                            canSave
                                ? 'bg-blue-600 hover:bg-blue-700 hover:shadow-lg'
                                : 'bg-slate-300 cursor-not-allowed'
                        ]"
                    >
                        <span v-if="isSaving" class="flex items-center">
                            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Guardando...
                        </span>
                        <span v-else>
                            {{ isEditMode ? 'Actualizar Perfil' : 'Crear Perfil' }}
                        </span>
                    </button>
                </div>
            </form>
        </div>
    </AdminLayout>
</template>

<style scoped>
/* Custom range slider styling */
input[type="range"] {
    -webkit-appearance: none;
}

input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    height: 16px;
    width: 16px;
    border-radius: 50%;
    background: #3b82f6;
    cursor: pointer;
    margin-top: -6px;
}

input[type="range"]::-moz-range-thumb {
    height: 16px;
    width: 16px;
    border-radius: 50%;
    background: #3b82f6;
    cursor: pointer;
    border: none;
}
</style>
