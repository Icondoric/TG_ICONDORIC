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
      <div v-if="editModal.type === 'education'" class="space-y-5">
        <!-- Nivel educativo -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nivel Educativo más alto</label>
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

        <!-- Lista de entradas de educación -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Entradas de Formación</label>

          <div class="space-y-2 mb-3">
            <div
              v-for="(edu, i) in editForm.gemini_education" :key="i"
              class="flex items-start gap-2 p-2.5 bg-gray-50 rounded-lg border border-gray-200"
            >
              <div class="flex-1 min-w-0">
                <p class="text-sm font-semibold text-gray-900 truncate">{{ edu.degree || '—' }}</p>
                <p class="text-xs text-gray-500 italic">{{ edu.institution || '' }}<span v-if="edu.year" class="ml-2 text-gray-400">{{ edu.year }}</span></p>
              </div>
              <button @click="$emit('removeEducationEntry', i)" class="text-gray-400 hover:text-red-500 flex-shrink-0 mt-0.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <p v-if="!editForm.gemini_education.length" class="text-sm text-gray-400 italic py-1">
              Sin entradas — agrega una a continuación
            </p>
          </div>

          <!-- Formulario nueva entrada -->
          <div class="border border-dashed border-emi-navy-300 rounded-lg p-3 space-y-2 bg-emi-navy-50">
            <p class="text-xs font-medium text-emi-navy-600 uppercase tracking-wide">Nueva entrada</p>
            <input
              :value="newEducationEntry.degree"
              @input="$emit('update:newEducationEntry', { ...newEducationEntry, degree: $event.target.value })"
              type="text" placeholder="Título / Grado *"
              class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
            />
            <input
              :value="newEducationEntry.institution"
              @input="$emit('update:newEducationEntry', { ...newEducationEntry, institution: $event.target.value })"
              type="text" placeholder="Institución"
              class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
            />
            <div class="flex gap-2">
              <input
                :value="newEducationEntry.year"
                @input="$emit('update:newEducationEntry', { ...newEducationEntry, year: $event.target.value })"
                type="text" placeholder="Año (ej. 2022)"
                class="flex-1 px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
              />
              <button
                @click="$emit('addEducationEntry', newEducationEntry)"
                class="px-4 py-1.5 text-sm bg-emi-navy-500 text-white rounded-lg hover:bg-emi-navy-600 transition-colors"
              >
                Agregar
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Experience Edit -->
      <div v-if="editModal.type === 'experience'" class="space-y-5">
        <!-- Años de experiencia -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Años totales de experiencia</label>
          <input
            :value="editForm.experience_years"
            @input="$emit('updateField', 'experience_years', Number($event.target.value))"
            type="number" min="0" max="50"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
          />
        </div>

        <!-- Lista de entradas de experiencia -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Entradas de Experiencia</label>

          <div class="space-y-2 mb-3">
            <div
              v-for="(exp, i) in editForm.gemini_experience" :key="i"
              class="flex items-start gap-2 p-2.5 bg-gray-50 rounded-lg border border-gray-200"
            >
              <div class="flex-1 min-w-0">
                <p class="text-sm font-semibold text-gray-900 truncate">{{ exp.role || exp.position || '—' }}</p>
                <p class="text-xs text-gray-500 italic">{{ exp.company || '' }}<span v-if="exp.duration" class="ml-2 text-gray-400">{{ exp.duration }}</span></p>
              </div>
              <button @click="$emit('removeExperienceEntry', i)" class="text-gray-400 hover:text-red-500 flex-shrink-0 mt-0.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <p v-if="!editForm.gemini_experience.length" class="text-sm text-gray-400 italic py-1">
              Sin entradas — agrega una a continuación
            </p>
          </div>

          <!-- Formulario nueva entrada -->
          <div class="border border-dashed border-emi-navy-300 rounded-lg p-3 space-y-2 bg-emi-navy-50">
            <p class="text-xs font-medium text-emi-navy-600 uppercase tracking-wide">Nueva entrada</p>
            <input
              :value="newExperienceEntry.role"
              @input="$emit('update:newExperienceEntry', { ...newExperienceEntry, role: $event.target.value })"
              type="text" placeholder="Cargo / Rol *"
              class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
            />
            <input
              :value="newExperienceEntry.company"
              @input="$emit('update:newExperienceEntry', { ...newExperienceEntry, company: $event.target.value })"
              type="text" placeholder="Empresa / Organización"
              class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
            />
            <div class="flex gap-2">
              <input
                :value="newExperienceEntry.duration"
                @input="$emit('update:newExperienceEntry', { ...newExperienceEntry, duration: $event.target.value })"
                type="text" placeholder="Período (ej. 2020–2023)"
                class="flex-1 px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
              />
              <button
                @click="$emit('addExperienceEntry', newExperienceEntry)"
                class="px-4 py-1.5 text-sm bg-emi-navy-500 text-white rounded-lg hover:bg-emi-navy-600 transition-colors"
              >
                Agregar
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Personal Info Edit -->
      <div v-if="editModal.type === 'personal_info'" class="space-y-4">
        <p class="text-sm text-gray-500">Estos datos se pre-cargan desde tu CV. Puedes corregirlos o completarlos manualmente.</p>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="sm:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Nombre completo</label>
            <input
              :value="editForm.nombre_completo"
              @input="$emit('updateField', 'nombre_completo', $event.target.value)"
              type="text"
              placeholder="Ej. Juan Pérez García"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Teléfono</label>
            <input
              :value="editForm.telefono"
              @input="$emit('updateField', 'telefono', $event.target.value)"
              type="tel"
              placeholder="Ej. +591 71234567"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email de contacto</label>
            <input
              :value="editForm.email_contacto"
              @input="$emit('updateField', 'email_contacto', $event.target.value)"
              type="email"
              placeholder="Ej. juan@example.com"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nacionalidad</label>
            <input
              :value="editForm.nacionalidad"
              @input="$emit('updateField', 'nacionalidad', $event.target.value)"
              type="text"
              placeholder="Ej. Boliviana"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Dirección / Ubicación</label>
            <input
              :value="editForm.direccion"
              @input="$emit('updateField', 'direccion', $event.target.value)"
              type="text"
              placeholder="Ej. La Paz, Bolivia"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
            />
          </div>
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
          class="px-4 py-2 bg-emi-navy-500 text-white rounded-lg hover:bg-emi-navy-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
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
  newLanguage: { type: String, default: '' },
  newEducationEntry: { type: Object, default: () => ({ degree: '', institution: '', year: '' }) },
  newExperienceEntry: { type: Object, default: () => ({ role: '', company: '', duration: '' }) }
})

defineEmits([
  'close', 'save', 'addSkill', 'removeSkill', 'updateField',
  'update:newHardSkill', 'update:newSoftSkill', 'update:newLanguage',
  'update:newEducationEntry', 'update:newExperienceEntry',
  'addEducationEntry', 'removeEducationEntry',
  'addExperienceEntry', 'removeExperienceEntry'
])
</script>
