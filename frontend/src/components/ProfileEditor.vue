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
