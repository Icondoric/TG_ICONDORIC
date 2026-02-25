<script setup>
/**
 * ProfileFormView
 * Vista para crear/editar perfiles institucionales
 */

import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAdminProfilesStore } from '@/features/admin/store/adminProfiles.store'
import { useAuthStore } from '@/features/auth/store/auth.store'
import AppLayout from '@/shared/components/AppLayout.vue'

const route = useRoute()
const router = useRouter()
const adminProfilesStore = useAdminProfilesStore()
const authStore = useAuthStore()

const isLoading = ref(false)
const isSaving = ref(false)
const error = ref(null)

const form = ref({
    institution_name: '',
    sector: '',
    description: '',
    ubicacion: '',
    contact_phone: '',
    contact_email: '',
    // Pesos con valores por defecto — no se muestran en el formulario,
    // cada oferta define los suyos propios
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
        required_soft_skills: [],
        required_education_level: 'Licenciatura',
        required_languages: []
    },
    thresholds: {
        apto: 0.70,
        considerado: 0.50
    }
})

const isEditMode = computed(() => !!route.params.id)
const profileId = computed(() => route.params.id)

const customSector = ref('')

const sectorOptions = [
    'Tecnologia', 'Finanzas', 'Salud', 'Educacion',
    'Construccion', 'Comercio', 'Servicios', 'Industria',
    'Gobierno', 'ONG', 'Otro'
]

const canSave = computed(() => {
    const isSectorValid = form.value.sector === 'Otro'
        ? customSector.value.trim().length > 0
        : !!form.value.sector

    return form.value.institution_name.trim() &&
           isSectorValid &&
           !isSaving.value
})

onMounted(async () => {
    if (!authStore.isAdminOrOperator) {
        router.push('/dashboard')
        return
    }

    if (isEditMode.value) {
        isLoading.value = true
        try {
            await adminProfilesStore.loadProfile(profileId.value)
            if (adminProfilesStore.currentProfile) {
                const p = adminProfilesStore.currentProfile

                form.value.institution_name = p.institution_name

                const loadedSector = p.sector
                if (sectorOptions.includes(loadedSector)) {
                    form.value.sector = loadedSector
                } else {
                    form.value.sector = 'Otro'
                    customSector.value = loadedSector
                }

                form.value.description = p.description || ''
                form.value.ubicacion = p.ubicacion || ''
                form.value.contact_phone = p.contact_phone || ''
                form.value.contact_email = p.contact_email || ''
                form.value.weights = { ...p.weights }
                form.value.requirements = { ...p.requirements }
                form.value.thresholds = { ...p.thresholds }

                if (!form.value.requirements.required_skills) form.value.requirements.required_skills = []
                if (!form.value.requirements.preferred_skills) form.value.requirements.preferred_skills = []
                if (!form.value.requirements.required_soft_skills) form.value.requirements.required_soft_skills = []
                if (!form.value.requirements.required_languages) form.value.requirements.required_languages = []
            }
        } catch (err) {
            error.value = 'Error cargando el perfil'
        } finally {
            isLoading.value = false
        }
    }
})

const save = async () => {
    if (!canSave.value) return

    isSaving.value = true
    error.value = null

    try {
        const finalSector = form.value.sector === 'Otro'
            ? customSector.value.trim()
            : form.value.sector

        const data = {
            institution_name: form.value.institution_name.trim(),
            sector: finalSector,
            description: form.value.description.trim() || null,
            ubicacion: form.value.ubicacion.trim() || null,
            contact_phone: form.value.contact_phone.trim() || null,
            contact_email: form.value.contact_email.trim() || null,
            weights: form.value.weights,
            requirements: form.value.requirements,
            thresholds: form.value.thresholds
        }

        if (isEditMode.value) {
            await adminProfilesStore.updateProfileAction(profileId.value, data)
        } else {
            await adminProfilesStore.createProfileAction(data)
        }

        router.push('/admin/profiles')
    } catch (err) {
        error.value = err.response?.data?.detail || 'Error guardando el perfil'
    } finally {
        isSaving.value = false
    }
}

const cancel = () => router.push('/admin/profiles')
</script>

<template>
    <AppLayout>
        <div class="max-w-4xl mx-auto py-8 px-4">
            <!-- Encabezado -->
            <header class="mb-8">
                <button @click="cancel" class="flex items-center text-slate-600 hover:text-slate-800 mb-4">
                    <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                    Volver
                </button>
                <h1 class="text-3xl font-bold text-slate-800">
                    {{ isEditMode ? 'Editar Perfil' : 'Nuevo Perfil' }}
                </h1>
                <p class="mt-2 text-slate-600">
                    {{ isEditMode ? 'Modifica los datos del perfil institucional' : 'Crea un nuevo perfil institucional' }}
                </p>
            </header>

            <!-- Cargando -->
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

                <!-- ─── Informacion Basica ─── -->
                <div class="bg-white rounded-xl shadow-md p-6">
                    <h2 class="text-lg font-semibold text-slate-800 mb-4">Informacion Basica</h2>

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
                            <label class="block text-sm font-medium text-slate-700 mb-1">Sector *</label>
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
                            <div v-if="form.sector === 'Otro'" class="mt-3">
                                <label class="block text-sm font-medium text-slate-700 mb-1">
                                    Especificar Sector *
                                </label>
                                <input
                                    v-model="customSector"
                                    type="text"
                                    required
                                    placeholder="Ej: Biotecnologia"
                                    class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-slate-50"
                                />
                            </div>
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Descripcion</label>
                            <textarea
                                v-model="form.description"
                                rows="3"
                                class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                placeholder="Descripcion breve de la institucion..."
                            ></textarea>
                        </div>

                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Ubicacion</label>
                            <input
                                v-model="form.ubicacion"
                                type="text"
                                class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                placeholder="Ej: La Paz, Bolivia"
                            />
                            <p class="text-xs text-slate-400 mt-1">
                                Se usara para autocompletar la ubicacion al crear ofertas de esta institucion.
                            </p>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-medium text-slate-700 mb-1">
                                    Telefono de Contacto
                                </label>
                                <input
                                    v-model="form.contact_phone"
                                    type="tel"
                                    class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                    placeholder="Ej: +591 2 1234567"
                                />
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-slate-700 mb-1">
                                    Correo de Contacto
                                </label>
                                <input
                                    v-model="form.contact_email"
                                    type="email"
                                    class="w-full px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                    placeholder="Ej: rrhh@empresa.com"
                                />
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Botones -->
                <div class="flex justify-end gap-4">
                    <button type="button" @click="cancel"
                        class="px-6 py-3 text-slate-600 hover:text-slate-800 font-medium">
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
    </AppLayout>
</template>

