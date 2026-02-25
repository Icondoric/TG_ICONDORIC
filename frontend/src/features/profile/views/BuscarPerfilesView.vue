<template>
  <AppLayout>
    <div class="max-w-8xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-slate-800">Buscar Perfiles</h1>
        <p class="mt-1 text-slate-500">Busca y gestiona los perfiles profesionales digitalizados de los usuarios.</p>
      </div>

      <!-- Layout dual panel -->
      <div class="flex gap-6 items-start">

        <!-- ═══════════════════════════════════════
             Panel izquierdo: lista de usuarios
        ════════════════════════════════════════ -->
        <div class="w-80 flex-shrink-0 space-y-4">

          <!-- Búsqueda -->
          <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 space-y-3">
            <h2 class="text-sm font-semibold text-slate-700 uppercase tracking-wide">Filtros</h2>

            <div>
              <label class="block text-xs font-medium text-slate-600 mb-1">Buscar</label>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Nombre o correo..."
                class="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                @keyup.enter="buscar"
              />
            </div>

            <div>
              <label class="block text-xs font-medium text-slate-600 mb-1">Rol</label>
              <select
                v-model="filterRole"
                class="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="all">Todos los roles</option>
                <option value="estudiante">Estudiante</option>
                <option value="titulado">Titulado</option>
                <option value="operador">Operador</option>
                <option value="administrador">Administrador</option>
              </select>
            </div>

            <button
              @click="buscar"
              class="w-full px-4 py-2 bg-slate-800 text-white text-sm font-medium rounded-lg hover:bg-slate-700 transition-colors"
            >
              Buscar
            </button>
          </div>

          <!-- Lista de usuarios -->
          <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">

            <!-- Cargando -->
            <div v-if="loadingUsers" class="flex justify-center items-center py-10">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-slate-700"></div>
            </div>

            <!-- Sin resultados -->
            <div v-else-if="users.length === 0" class="py-10 px-4 text-center">
              <svg class="mx-auto h-10 w-10 text-slate-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              <p class="text-sm text-slate-400">No se encontraron usuarios</p>
            </div>

            <!-- Lista -->
            <ul v-else class="divide-y divide-slate-100">
              <li
                v-for="user in users"
                :key="user.id"
                @click="selectUser(user)"
                :class="[
                  'flex items-center gap-3 px-4 py-3 cursor-pointer transition-colors',
                  selectedUser?.id === user.id
                    ? 'bg-slate-800 text-white'
                    : 'hover:bg-slate-50'
                ]"
              >
                <!-- Avatar -->
                <div
                  :class="[
                    'w-9 h-9 rounded-full flex items-center justify-center flex-shrink-0 text-sm font-bold',
                    selectedUser?.id === user.id
                      ? 'bg-white text-slate-800'
                      : 'bg-slate-100 text-slate-600'
                  ]"
                >
                  {{ getUserInitial(user) }}
                </div>

                <!-- Info -->
                <div class="min-w-0 flex-1">
                  <p :class="['text-sm font-medium truncate', selectedUser?.id === user.id ? 'text-white' : 'text-slate-800']">
                    {{ user.nombre_completo || user.email }}
                  </p>
                  <p :class="['text-xs truncate', selectedUser?.id === user.id ? 'text-slate-300' : 'text-slate-400']">
                    {{ user.email }}
                  </p>
                  <div class="flex items-center gap-1.5 mt-1">
                    <span
                      :class="[
                        'text-xs px-1.5 py-0.5 rounded font-medium',
                        selectedUser?.id === user.id
                          ? 'bg-white/20 text-white'
                          : getRoleBadgeClass(user.rol)
                      ]"
                    >
                      {{ user.rol }}
                    </span>
                    <!-- Indicador de perfil -->
                    <span
                      v-if="user.tiene_perfil"
                      :class="[
                        'text-xs px-1.5 py-0.5 rounded font-medium',
                        selectedUser?.id === user.id
                          ? 'bg-white/20 text-white'
                          : user.perfil_completo ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                      ]"
                    >
                      {{ user.perfil_completo ? 'Completo' : 'Incompleto' }}
                    </span>
                  </div>
                </div>
              </li>
            </ul>

            <!-- Paginación -->
            <div v-if="usersTotal > PAGE_SIZE" class="flex items-center justify-between px-4 py-3 border-t border-slate-100">
              <button
                @click="prevPage"
                :disabled="usersPage <= 1"
                class="text-xs text-slate-500 hover:text-slate-700 disabled:opacity-40 disabled:cursor-not-allowed"
              >
                ← Anterior
              </button>
              <span class="text-xs text-slate-400">
                Pág. {{ usersPage }} · {{ usersTotal }} resultados
              </span>
              <button
                @click="nextPage"
                :disabled="usersPage * PAGE_SIZE >= usersTotal"
                class="text-xs text-slate-500 hover:text-slate-700 disabled:opacity-40 disabled:cursor-not-allowed"
              >
                Siguiente →
              </button>
            </div>

            <!-- Total si hay pocos -->
            <div v-else-if="users.length > 0" class="px-4 py-2 border-t border-slate-100 text-xs text-slate-400 text-right">
              {{ usersTotal }} usuario{{ usersTotal !== 1 ? 's' : '' }}
            </div>
          </div>
        </div>

        <!-- ═══════════════════════════════════════
             Panel derecho: perfil del usuario
        ════════════════════════════════════════ -->
        <div class="flex-1 min-w-0">

          <!-- Estado vacío: ningún usuario seleccionado -->
          <div v-if="!selectedUser" class="bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col items-center justify-center py-24 px-8 text-center">
            <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mb-4">
              <svg class="w-8 h-8 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-slate-700">Selecciona un usuario</h3>
            <p class="mt-2 text-sm text-slate-400 max-w-xs">
              Elige un usuario de la lista para ver y editar su perfil profesional digitalizado.
            </p>
          </div>

          <!-- Cargando perfil -->
          <div v-else-if="loadingProfile" class="bg-white rounded-xl shadow-sm border border-slate-200 flex justify-center items-center py-24">
            <div class="text-center">
              <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-slate-700 mx-auto"></div>
              <p class="mt-4 text-sm text-slate-500">Cargando perfil de {{ selectedUser.nombre_completo || selectedUser.email }}...</p>
            </div>
          </div>

          <!-- Error cargando perfil -->
          <div v-else-if="profileError" class="bg-white rounded-xl shadow-sm border border-slate-200 flex flex-col items-center justify-center py-24 px-8 text-center">
            <div class="w-14 h-14 bg-yellow-50 rounded-full flex items-center justify-center mb-4">
              <svg class="w-7 h-7 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-base font-semibold text-slate-700">Sin perfil digitalizado</h3>
            <p class="mt-2 text-sm text-slate-400">{{ profileError }}</p>
          </div>

          <!-- Perfil cargado -->
          <div v-else-if="selectedProfile" class="space-y-5">

            <!-- Cabecera del usuario -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-4">
                  <div class="w-14 h-14 rounded-full bg-slate-800 flex items-center justify-center text-white text-xl font-bold flex-shrink-0">
                    {{ getUserInitial(selectedUser) }}
                  </div>
                  <div>
                    <h2 class="text-xl font-bold text-slate-800">
                      {{ selectedProfile.nombre_completo || selectedUser.nombre_completo || 'Sin nombre' }}
                    </h2>
                    <p class="text-sm text-slate-500">{{ selectedUser.email }}</p>
                    <div class="flex items-center gap-2 mt-1.5">
                      <span :class="['text-xs px-2 py-0.5 rounded-full font-medium', getRoleBadgeClass(selectedUser.rol)]">
                        {{ selectedUser.rol }}
                      </span>
                      <span v-if="selectedProfile.cv_filename" class="text-xs text-slate-400 flex items-center gap-1">
                        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        {{ selectedProfile.cv_filename }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Score de completitud -->
                <div class="text-center flex-shrink-0">
                  <div class="text-3xl font-bold" :class="selectedProfile.completeness_score >= 0.7 ? 'text-green-600' : selectedProfile.completeness_score >= 0.4 ? 'text-yellow-600' : 'text-red-500'">
                    {{ Math.round(selectedProfile.completeness_score * 100) }}%
                  </div>
                  <div class="text-xs text-slate-400 mt-0.5">Completitud</div>
                  <div class="w-20 h-2 bg-slate-100 rounded-full mt-1.5 overflow-hidden">
                    <div
                      class="h-full rounded-full transition-all"
                      :class="selectedProfile.completeness_score >= 0.7 ? 'bg-green-500' : selectedProfile.completeness_score >= 0.4 ? 'bg-yellow-500' : 'bg-red-400'"
                      :style="{ width: `${selectedProfile.completeness_score * 100}%` }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Información personal -->
            <PersonalInfoCard
              :profile="selectedProfile"
              @edit="openEditModal('personal_info')"
            />

            <!-- Datos extraídos por Gemini -->
            <DigitalizationSummary
              :profile="selectedProfile"
              :geminiPersonalInfo="geminiPersonalInfo"
              :geminiEducation="geminiEducation"
              :geminiExperience="geminiExperience"
              :hasGeminiData="hasGeminiData"
            />

            <!-- Competencias (editable) -->
            <CompetenciasCard
              :profile="selectedProfile"
              :readOnly="false"
              @edit="openEditModal"
            />

            <!-- Formación y Experiencia (editable) -->
            <EducationExperienceGrid
              :profile="selectedProfile"
              :geminiEducation="geminiEducation"
              :geminiExperience="geminiExperience"
              :readOnly="false"
              @edit="openEditModal"
            />

          </div>
        </div>
      </div>
    </div>

    <!-- Modal de edición -->
    <EditProfileModal
      :editModal="editModal"
      :editForm="editForm"
      :saving="saving"
      :newHardSkill="newHardSkill"
      :newSoftSkill="newSoftSkill"
      :newLanguage="newLanguage"
      @close="closeEditModal"
      @save="saveChanges"
      @addSkill="addSkill"
      @removeSkill="removeSkill"
      @updateField="updateField"
      @update:newHardSkill="newHardSkill = $event"
      @update:newSoftSkill="newSoftSkill = $event"
      @update:newLanguage="newLanguage = $event"
    />
  </AppLayout>
</template>

<script setup>
import { onMounted } from 'vue'
import AppLayout from '@/shared/components/AppLayout.vue'
import PersonalInfoCard from '../components/PersonalInfoCard.vue'
import CompetenciasCard from '../components/CompetenciasCard.vue'
import EducationExperienceGrid from '../components/EducationExperienceGrid.vue'
import DigitalizationSummary from '../components/DigitalizationSummary.vue'
import EditProfileModal from '../components/EditProfileModal.vue'
import { useAdminProfileEditor } from '../composables/useAdminProfileEditor'

const PAGE_SIZE = 20

const {
  // Lista
  users, loadingUsers, searchQuery, filterRole,
  usersPage, usersTotal,
  loadUsers,
  // Perfil seleccionado
  selectedUser, selectedProfile, loadingProfile, profileError,
  selectUser,
  geminiPersonalInfo, geminiEducation, geminiExperience, hasGeminiData,
  // Modal
  editModal, editForm, saving,
  newHardSkill, newSoftSkill, newLanguage,
  openEditModal, closeEditModal,
  addSkill, removeSkill, updateField, saveChanges,
  // Helpers
  formatDate, getRoleBadgeClass, getUserInitial
} = useAdminProfileEditor()

function buscar() {
  usersPage.value = 1
  loadUsers()
}

function prevPage() {
  if (usersPage.value > 1) {
    usersPage.value--
    loadUsers()
  }
}

function nextPage() {
  if (usersPage.value * PAGE_SIZE < usersTotal.value) {
    usersPage.value++
    loadUsers()
  }
}

onMounted(() => {
  loadUsers()
})
</script>
