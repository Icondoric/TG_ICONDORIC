<script setup>
import { ref } from 'vue'

const props = defineProps({
  initialData: Object,
  required: true
})

const formData = ref(JSON.parse(JSON.stringify(props.initialData))) // Deep copy to avoid mutating prop directly initially
const saved = ref(false)

const saveProfile = () => {
  // In a real app, this would send a PUT request to update the profile in the DB
  console.log("Saving data:", formData.value)
  saved.value = true
  setTimeout(() => saved.value = false, 3000)
}

const addSkill = () => {
  formData.value.skills.push({ name: "", categories: [] })
}

const removeSkill = (index) => {
  formData.value.skills.splice(index, 1)
}

// --- New List Management Logic ---

// Languages
const addLanguage = () => {
  if (!formData.value.personal_info.languages) formData.value.personal_info.languages = []
  formData.value.personal_info.languages.push("")
}
const removeLanguage = (index) => {
  formData.value.personal_info.languages.splice(index, 1)
}

// Experience
const addExperience = () => {
    if (!formData.value.experience_structured) formData.value.experience_structured = []
    formData.value.experience_structured.push({ role: "", company: "", duration: "", description: "" })
}
const removeExperience = (index) => {
    formData.value.experience_structured.splice(index, 1)
}

// Education
const addEducation = () => {
    if (!formData.value.education_structured) formData.value.education_structured = []
    formData.value.education_structured.push({ degree: "", institution: "", year: "" })
}
const removeEducation = (index) => {
    formData.value.education_structured.splice(index, 1)
}
</script>

<template>
  <div class="bg-white p-8 rounded-xl shadow-lg border border-slate-100">
    <form @submit.prevent="saveProfile" class="space-y-6">

      <!-- Personal Info -->
      <section>
        <h3 class="text-lg font-semibold text-slate-700 mb-4 border-b pb-2">Información de Contacto</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Email Detectado</label>
            <input v-model="formData.personal_info.email" type="email" class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all" />
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Teléfono Detectado</label>
            <input v-model="formData.personal_info.phone" type="text" class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all" />
          </div>
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-slate-700 mb-1">Carrera / Título</label>
            <input v-model="formData.personal_info.degree" type="text" placeholder="Ej. Ingeniería de Sistemas" class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all" />
          </div>
          <div class="md:col-span-2">
             <label class="block text-sm font-medium text-slate-700 mb-1">Nombres Detectados (Candidatos)</label>
             <div class="flex gap-2 flex-wrap">
                <span v-for="name in formData.personal_info.detected_names" :key="name" class="px-3 py-1 bg-slate-100 rounded-full text-sm text-slate-700 border">
                    {{ name }}
                </span>
                <span v-if="!formData.personal_info.detected_names?.length" class="text-sm text-slate-400 italic">No se detectaron nombres claros</span>
             </div>
          </div>
        </div>
      </section>

      <!-- Professional Summary & Languages -->
      <section>
        <h3 class="text-lg font-semibold text-slate-700 mb-4 border-b pb-2">Perfil Profesional</h3>

        <div class="mb-6">
            <label class="block text-sm font-medium text-slate-700 mb-1">Resumen Profesional</label>
            <textarea v-model="formData.personal_info.summary" rows="3" class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all resize-none"></textarea>
        </div>

        <div>
            <div class="flex justify-between items-center mb-2">
                <label class="block text-sm font-medium text-slate-700">Idiomas</label>
                <button type="button" @click="addLanguage" class="text-sm text-blue-600 hover:text-blue-700 font-medium">+ Agregar</button>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                <div v-for="(lang, index) in formData.personal_info.languages" :key="index" class="relative group">
                    <input v-model="formData.personal_info.languages[index]" type="text" class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all" placeholder="Ej. Inglés Avanzado" />
                    <button type="button" @click="removeLanguage(index)" class="absolute right-2 top-2 text-slate-400 hover:text-red-500 font-bold opacity-0 group-hover:opacity-100 transition-all">&times;</button>
                </div>
            </div>
        </div>
      </section>

      <!-- Experience -->
      <section>
        <div class="flex justify-between items-center mb-4 border-b pb-2">
            <h3 class="text-lg font-semibold text-slate-700">Experiencia Laboral</h3>
            <button type="button" @click="addExperience" class="text-sm text-blue-600 hover:text-blue-700 font-medium">+ Agregar Experiencia</button>
        </div>

        <div class="space-y-4">
            <div v-for="(exp, index) in formData.experience_structured" :key="index" class="relative group bg-slate-50 p-4 rounded-lg border border-slate-200">
                <button type="button" @click="removeExperience(index)" class="absolute right-4 top-4 text-slate-400 hover:text-red-600 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                </button>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-medium text-slate-500 mb-1">Cargo</label>
                        <input v-model="exp.role" type="text" class="w-full px-3 py-2 bg-white border border-slate-300 rounded focus:ring-2 focus:ring-blue-500 outline-none" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-500 mb-1">Empresa</label>
                        <input v-model="exp.company" type="text" class="w-full px-3 py-2 bg-white border border-slate-300 rounded focus:ring-2 focus:ring-blue-500 outline-none" />
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-500 mb-1">Fechas / Duración</label>
                        <input v-model="exp.duration" type="text" class="w-full px-3 py-2 bg-white border border-slate-300 rounded focus:ring-2 focus:ring-blue-500 outline-none" />
                    </div>
                    <div class="md:col-span-2">
                        <label class="block text-xs font-medium text-slate-500 mb-1">Descripción</label>
                        <textarea v-model="exp.description" rows="2" class="w-full px-3 py-2 bg-white border border-slate-300 rounded focus:ring-2 focus:ring-blue-500 outline-none resize-none"></textarea>
                    </div>
                </div>
            </div>
            <div v-if="!formData.experience_structured?.length" class="text-center text-slate-400 italic py-4">No hay experiencia registrada</div>
        </div>
      </section>

      <!-- Education -->
      <section>
        <div class="flex justify-between items-center mb-4 border-b pb-2">
            <h3 class="text-lg font-semibold text-slate-700">Educación</h3>
            <button type="button" @click="addEducation" class="text-sm text-blue-600 hover:text-blue-700 font-medium">+ Agregar Educación</button>
        </div>

        <div class="space-y-3">
            <div v-for="(edu, index) in formData.education_structured" :key="index" class="relative group bg-slate-50 p-3 rounded-lg border border-slate-200 flex flex-col md:flex-row gap-3 items-start md:items-center">
                <div class="flex-1 w-full">
                    <label class="block text-xs font-medium text-slate-500 mb-1">Título / Carrera</label>
                    <input v-model="edu.degree" type="text" class="w-full px-3 py-1 bg-white border border-slate-300 rounded focus:ring-2 focus:ring-blue-500 outline-none" />
                </div>
                <div class="flex-1 w-full">
                     <label class="block text-xs font-medium text-slate-500 mb-1">Institución</label>
                    <input v-model="edu.institution" type="text" class="w-full px-3 py-1 bg-white border border-slate-300 rounded focus:ring-2 focus:ring-blue-500 outline-none" />
                </div>
                <div class="w-full md:w-32">
                     <label class="block text-xs font-medium text-slate-500 mb-1">Año</label>
                    <input v-model="edu.year" type="text" class="w-full px-3 py-1 bg-white border border-slate-300 rounded focus:ring-2 focus:ring-blue-500 outline-none" />
                </div>
                <button type="button" @click="removeEducation(index)" class="mt-5 text-slate-400 hover:text-red-500 font-bold p-1">
                    &times;
                </button>
            </div>
             <div v-if="!formData.education_structured?.length" class="text-center text-slate-400 italic py-4">No hay educación registrada</div>
        </div>
      </section>

      <!-- Skills -->
      <section>
        <div class="flex justify-between items-center mb-4 border-b pb-2">
            <h3 class="text-lg font-semibold text-slate-700">Competencias Identificadas</h3>
            <button type="button" @click="addSkill" class="text-sm text-blue-600 hover:text-blue-700 font-medium">+ Agregar</button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          <div v-for="(skill, index) in formData.skills" :key="index" class="relative group bg-slate-50 p-2 rounded-lg border border-slate-200">
            <div class="mb-2">
                <input
                    v-if="typeof skill === 'object'"
                    v-model="skill.name"
                    type="text"
                    class="w-full px-3 py-1 bg-white border border-slate-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all text-sm font-medium"
                />
                <input
                    v-else
                    v-model="formData.skills[index]"
                    type="text"
                    class="w-full px-3 py-1 bg-white border border-slate-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all text-sm font-medium"
                />
            </div>

            <!-- Type Badges -->
            <div v-if="skill.categories && skill.categories.length" class="flex flex-wrap gap-1 mb-1">
                <span v-for="cat in skill.categories" :key="cat"
                      :class="{
                          'bg-blue-100 text-blue-700': cat === 'digital' || cat === 'tech_tool',
                          'bg-green-100 text-green-700': cat === 'language' || cat === 'transversal',
                          'bg-purple-100 text-purple-700': cat === 'devops' || cat === 'occupation',
                          'bg-gray-100 text-gray-600': !['digital', 'language', 'transversal', 'devops', 'tech_tool'].includes(cat)
                      }"
                      class="text-[10px] px-2 py-0.5 rounded-full uppercase tracking-wider font-bold">
                    {{ cat.replace('_', ' ') }}
                </span>
            </div>

            <button type="button" @click="removeSkill(index)" class="absolute -right-2 -top-2 bg-white text-red-400 hover:text-red-600 border rounded-full w-6 h-6 flex items-center justify-center shadow-sm hover:shadow opacity-0 group-hover:opacity-100 transition-all font-bold">
                &times;
            </button>
          </div>
          <div v-if="formData.skills.length === 0" class="col-span-full text-center text-slate-500 italic py-4">
            No se identificaron competencias automáticamente. Añade algunas manualmente.
          </div>
        </div>
      </section>

      <!-- Actions -->
      <div class="pt-6 flex items-center justify-end gap-4 border-t mt-8">
        <span v-if="saved" class="text-green-600 font-medium animate-pulse">¡Datos guardados correctamente!</span>
        <button type="submit" class="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-0.5">
          Confirmar y Guardar Perfil
        </button>
      </div>

    </form>
  </div>
</template>
