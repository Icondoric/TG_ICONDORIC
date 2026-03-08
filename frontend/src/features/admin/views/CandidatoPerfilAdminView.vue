<template>
  <AppLayout>
    <div class="max-w-3xl mx-auto px-6 py-8 space-y-6">

      <!-- Breadcrumb + título -->
      <div>
        <button
          @click="router.back()"
          class="inline-flex items-center gap-1.5 text-xs text-emi-navy-400 hover:text-emi-navy-600 font-medium transition-colors mb-2"
        >
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
          Volver
        </button>
        <h1 class="text-2xl font-bold text-emi-navy-500">Perfil del Candidato</h1>
        <p class="mt-1 text-sm text-gray-500">CV digitalizado y competencias extraídas automáticamente.</p>
      </div>

      <!-- Cargando -->
      <div v-if="loading" class="flex justify-center py-20">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-emi-navy-500"></div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="card-emi text-center py-12">
        <svg class="w-10 h-10 text-danger-400 mx-auto mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <p class="text-danger-600 font-semibold">{{ error }}</p>
      </div>

      <!-- Perfil cargado -->
      <template v-else-if="perfil">

        <!-- ── Datos personales ── -->
        <div class="card-emi space-y-4">
          <div class="flex items-center gap-3 mb-1">
            <div class="w-12 h-12 rounded-full bg-emi-navy-100 flex items-center justify-center text-emi-navy-700 font-bold text-lg">
              {{ initials }}
            </div>
            <div>
              <h2 class="text-lg font-bold text-emi-navy-800">{{ perfil.nombre_completo || 'Sin nombre' }}</h2>
              <p class="text-sm text-gray-500">{{ perfil.email_contacto || '—' }}</p>
            </div>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-2 border-t border-gray-100">
            <div v-if="perfil.telefono">
              <p class="text-xs text-gray-400 mb-0.5">Teléfono</p>
              <p class="text-sm font-medium text-gray-800">{{ perfil.telefono }}</p>
            </div>
            <div v-if="perfil.direccion">
              <p class="text-xs text-gray-400 mb-0.5">Dirección</p>
              <p class="text-sm font-medium text-gray-800">{{ perfil.direccion }}</p>
            </div>
            <div v-if="perfil.carrera">
              <p class="text-xs text-gray-400 mb-0.5">Carrera</p>
              <p class="text-sm font-medium text-gray-800">{{ perfil.carrera }}</p>
            </div>
            <div v-if="perfil.semestre_actual">
              <p class="text-xs text-gray-400 mb-0.5">Semestre actual</p>
              <p class="text-sm font-medium text-gray-800">{{ perfil.semestre_actual }}°</p>
            </div>
            <div v-if="perfil.cv_uploaded_at">
              <p class="text-xs text-gray-400 mb-0.5">CV subido</p>
              <p class="text-sm font-medium text-gray-800">{{ formatDate(perfil.cv_uploaded_at) }}</p>
            </div>
            <div v-if="perfil.cv_filename">
              <p class="text-xs text-gray-400 mb-0.5">Archivo</p>
              <p class="text-sm font-medium text-gray-800 truncate" :title="perfil.cv_filename">{{ perfil.cv_filename }}</p>
            </div>
          </div>
        </div>

        <!-- ── Resumen ML ── -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div class="card-emi text-center py-4">
            <div class="text-2xl font-black text-emi-navy-700">{{ perfil.experience_years ?? 0 }}</div>
            <div class="text-xs text-gray-400 mt-0.5">años de exp.</div>
          </div>
          <div class="card-emi text-center py-4">
            <div class="text-2xl font-black text-emi-navy-700">{{ (perfil.hard_skills || []).length }}</div>
            <div class="text-xs text-gray-400 mt-0.5">hab. técnicas</div>
          </div>
          <div class="card-emi text-center py-4">
            <div class="text-2xl font-black text-emi-navy-700">{{ (perfil.soft_skills || []).length }}</div>
            <div class="text-xs text-gray-400 mt-0.5">hab. blandas</div>
          </div>
          <div class="card-emi text-center py-4">
            <div class="text-2xl font-black text-emi-navy-700">{{ (perfil.languages || []).length }}</div>
            <div class="text-xs text-gray-400 mt-0.5">idiomas</div>
          </div>
        </div>

        <!-- ── Habilidades ── -->
        <div class="card-emi space-y-4">
          <h3 class="text-sm font-bold text-emi-navy-700 uppercase tracking-wide">Habilidades</h3>

          <div v-if="perfil.hard_skills?.length">
            <p class="text-xs text-gray-400 mb-2">Técnicas</p>
            <div class="flex flex-wrap gap-1.5">
              <span v-for="s in perfil.hard_skills" :key="s"
                class="px-2.5 py-0.5 bg-emi-navy-50 text-emi-navy-700 border border-emi-navy-200 rounded-full text-xs font-medium">
                {{ s }}
              </span>
            </div>
          </div>

          <div v-if="perfil.soft_skills?.length">
            <p class="text-xs text-gray-400 mb-2">Blandas</p>
            <div class="flex flex-wrap gap-1.5">
              <span v-for="s in perfil.soft_skills" :key="s"
                class="px-2.5 py-0.5 bg-gray-100 text-gray-700 border border-gray-200 rounded-full text-xs font-medium">
                {{ s }}
              </span>
            </div>
          </div>

          <div v-if="perfil.languages?.length">
            <p class="text-xs text-gray-400 mb-2">Idiomas</p>
            <div class="flex flex-wrap gap-1.5">
              <span v-for="l in perfil.languages" :key="l"
                class="px-2.5 py-0.5 bg-info-50 text-info-700 border border-info-200 rounded-full text-xs font-medium">
                {{ l }}
              </span>
            </div>
          </div>

          <div v-if="perfil.education_level">
            <p class="text-xs text-gray-400 mb-2">Nivel educativo</p>
            <span class="px-2.5 py-0.5 bg-emi-gold-50 text-emi-gold-700 border border-emi-gold-200 rounded-full text-xs font-medium">
              {{ perfil.education_level }}
            </span>
          </div>
        </div>

        <!-- ── Historial educativo (gemini_extraction) ── -->
        <div v-if="educacion.length" class="card-emi space-y-3">
          <h3 class="text-sm font-bold text-emi-navy-700 uppercase tracking-wide">Formación Académica</h3>
          <div v-for="(edu, i) in educacion" :key="i" class="flex gap-3 items-start">
            <div class="w-8 h-8 rounded-lg bg-emi-navy-100 flex items-center justify-center shrink-0 mt-0.5">
              <svg class="w-4 h-4 text-emi-navy-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"/>
              </svg>
            </div>
            <div>
              <p class="text-sm font-semibold text-gray-800">{{ edu.degree || edu.titulo || edu.title || 'Sin título' }}</p>
              <p class="text-xs text-gray-500">{{ edu.institution || edu.institucion || '—' }}</p>
              <p v-if="edu.year || edu.año || edu.fecha" class="text-xs text-gray-400">{{ edu.year || edu.año || edu.fecha }}</p>
            </div>
          </div>
        </div>

        <!-- ── Experiencia laboral (gemini_extraction) ── -->
        <div v-if="experiencia.length" class="card-emi space-y-3">
          <h3 class="text-sm font-bold text-emi-navy-700 uppercase tracking-wide">Experiencia Laboral</h3>
          <div v-for="(exp, i) in experiencia" :key="i" class="flex gap-3 items-start">
            <div class="w-8 h-8 rounded-lg bg-emi-gold-100 flex items-center justify-center shrink-0 mt-0.5">
              <svg class="w-4 h-4 text-emi-gold-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
            </div>
            <div class="flex-1">
              <p class="text-sm font-semibold text-gray-800">{{ exp.position || exp.cargo || exp.puesto || 'Sin cargo' }}</p>
              <p class="text-xs text-gray-500">{{ exp.company || exp.empresa || exp.organization || '—' }}</p>
              <p v-if="exp.duration || exp.duracion" class="text-xs text-gray-400">{{ exp.duration || exp.duracion }}</p>
              <p v-if="exp.description || exp.descripcion" class="text-xs text-gray-500 mt-1 leading-relaxed">{{ exp.description || exp.descripcion }}</p>
            </div>
          </div>
        </div>

      </template>

    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '@/shared/components/AppLayout.vue'
import { fetchUserProfile } from '../api/users.api'

const route = useRoute()
const router = useRouter()

const userId = route.params.userId
const perfil = ref(null)
const loading = ref(true)
const error = ref(null)

const initials = computed(() => {
  const name = perfil.value?.nombre_completo || ''
  return name.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase() || '?'
})

const educacion = computed(() => {
  const ge = perfil.value?.gemini_extraction || {}
  return ge.education || ge.educacion || ge.formacion || []
})

const experiencia = computed(() => {
  const ge = perfil.value?.gemini_extraction || {}
  return ge.experience || ge.experiencia || ge.work_experience || []
})

const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' })
}

onMounted(async () => {
  try {
    perfil.value = await fetchUserProfile(userId)
  } catch (e) {
    error.value = e.response?.status === 404 ? 'Este usuario no tiene perfil digitalizado.' : 'Error al cargar el perfil.'
  } finally {
    loading.value = false
  }
})
</script>
