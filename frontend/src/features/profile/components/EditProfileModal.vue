<template>
  <div v-if="editModal.show" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50 p-4">
    <Card class="w-full max-w-2xl max-h-[90vh] overflow-y-auto" :hoverable="false">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-900">{{ editModal.title }}</h3>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Skills Edit -->
      <div v-if="editModal.type === 'skills'" class="space-y-6">
        <!-- Hard Skills -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Habilidades Tecnicas</label>
          <div class="flex flex-wrap gap-2 mb-2">
            <Badge v-for="(skill, index) in editForm.hard_skills" :key="skill" variant="navy">
              {{ skill }}
              <button @click="$emit('removeSkill', 'hard_skills', index)" class="ml-1 hover:text-red-500">&times;</button>
            </Badge>
          </div>
          <div class="flex gap-2">
            <input
              :value="newHardSkill"
              @input="$emit('update:newHardSkill', $event.target.value)"
              @keyup.enter="$emit('addSkill', 'hard_skills', newHardSkill); $emit('update:newHardSkill', '')"
              type="text"
              placeholder="Agregar habilidad tecnica..."
              class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
            />
            <button
              @click="$emit('addSkill', 'hard_skills', newHardSkill); $emit('update:newHardSkill', '')"
              class="px-4 py-2 bg-emi-navy-500 text-white rounded-lg hover:bg-emi-navy-600 transition-colors"
            >
              Agregar
            </button>
          </div>
        </div>

        <!-- Soft Skills -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Habilidades Blandas</label>
          <div class="flex flex-wrap gap-2 mb-2">
            <Badge v-for="(skill, index) in editForm.soft_skills" :key="skill" variant="gold">
              {{ skill }}
              <button @click="$emit('removeSkill', 'soft_skills', index)" class="ml-1 hover:text-red-500">&times;</button>
            </Badge>
          </div>
          <div class="flex gap-2">
            <input
              :value="newSoftSkill"
              @input="$emit('update:newSoftSkill', $event.target.value)"
              @keyup.enter="$emit('addSkill', 'soft_skills', newSoftSkill); $emit('update:newSoftSkill', '')"
              type="text"
              placeholder="Agregar habilidad blanda..."
              class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-gold-500 focus:border-transparent"
            />
            <button
              @click="$emit('addSkill', 'soft_skills', newSoftSkill); $emit('update:newSoftSkill', '')"
              class="px-4 py-2 bg-emi-gold-500 text-emi-navy-800 rounded-lg hover:bg-emi-gold-400 transition-colors"
            >
              Agregar
            </button>
          </div>
        </div>

        <!-- Languages -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Idiomas</label>
          <div class="flex flex-wrap gap-2 mb-2">
            <Badge v-for="(lang, index) in editForm.languages" :key="lang" variant="neutral">
              {{ lang }}
              <button @click="$emit('removeSkill', 'languages', index)" class="ml-1 hover:text-red-500">&times;</button>
            </Badge>
          </div>
          <div class="flex gap-2">
            <input
              :value="newLanguage"
              @input="$emit('update:newLanguage', $event.target.value)"
              @keyup.enter="$emit('addSkill', 'languages', newLanguage); $emit('update:newLanguage', '')"
              type="text"
              placeholder="Agregar idioma..."
              class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-transparent"
            />
            <button
              @click="$emit('addSkill', 'languages', newLanguage); $emit('update:newLanguage', '')"
              class="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
            >
              Agregar
            </button>
          </div>
        </div>
      </div>

      <!-- Education Edit -->
      <div v-if="editModal.type === 'education'" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Nivel Educativo</label>
          <select
            :value="editForm.education_level"
            @input="$emit('updateField', 'education_level', $event.target.value)"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
          >
            <option value="">Seleccionar nivel...</option>
            <option value="Bachiller">Bachiller</option>
            <option value="Tecnico Superior">Tecnico Superior</option>
            <option value="Licenciatura">Licenciatura</option>
            <option value="Ingenieria">Ingenieria</option>
            <option value="Especialidad">Especialidad</option>
            <option value="Maestria">Maestria</option>
            <option value="Doctorado">Doctorado</option>
          </select>
        </div>
      </div>

      <!-- Experience Edit -->
      <div v-if="editModal.type === 'experience'" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Anos de Experiencia</label>
          <input
            :value="editForm.experience_years"
            @input="$emit('updateField', 'experience_years', Number($event.target.value))"
            type="number"
            min="0"
            max="50"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
          />
        </div>
      </div>

      <div class="mt-6 flex justify-end gap-3">
        <button
          @click="$emit('close')"
          class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
        >
          Cancelar
        </button>
        <button
          @click="$emit('save')"
          :disabled="saving"
          class="btn-emi-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ saving ? 'Guardando...' : 'Guardar Cambios' }}
        </button>
      </div>
    </Card>
  </div>
</template>

<script setup>
import Card from '@/shared/components/ui/Card.vue'
import Badge from '@/shared/components/ui/Badge.vue'

defineProps({
  editModal: { type: Object, required: true },
  editForm: { type: Object, required: true },
  saving: { type: Boolean, default: false },
  newHardSkill: { type: String, default: '' },
  newSoftSkill: { type: String, default: '' },
  newLanguage: { type: String, default: '' }
})

defineEmits(['close', 'save', 'addSkill', 'removeSkill', 'updateField', 'update:newHardSkill', 'update:newSoftSkill', 'update:newLanguage'])
</script>
