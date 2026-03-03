<template>
  <AppLayout>
    <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <router-link to="/admin/system/roles" class="text-blue-600 hover:text-blue-800 flex items-center mb-4">
          <svg class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Volver a Roles
        </router-link>
        <h1 class="text-3xl font-bold text-gray-900">{{ isEditing ? 'Editar Rol' : 'Nuevo Rol' }}</h1>
      </div>

      <!-- Form -->
      <form @submit.prevent="saveRole" class="bg-white rounded-lg shadow p-6">
        <div v-if="error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-red-700 whitespace-pre-line">{{ error }}</p>
        </div>

        <div class="space-y-6">
          <!-- Nombre -->
          <div>
            <label class="block text-sm font-medium text-gray-700">Nombre del Rol *</label>
            <input
              v-model="form.nombre"
              type="text"
              required
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              placeholder="Ej: supervisor, coordinador"
            />
            <p class="mt-1 text-xs text-gray-500">No puede coincidir con los roles del sistema (estudiante, titulado, operador, administrador).</p>
          </div>

          <!-- Descripción -->
          <div>
            <label class="block text-sm font-medium text-gray-700">Descripción</label>
            <textarea
              v-model="form.descripcion"
              rows="2"
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              placeholder="Describe brevemente para qué es este rol..."
            />
          </div>

          <!-- Módulos y sub-módulos jerárquicos -->
          <div>
            <div class="flex items-center justify-between mb-3">
              <label class="block text-sm font-medium text-gray-700">Permisos de acceso *</label>
              <div class="flex gap-3 text-xs">
                <button type="button" @click="selectAll" class="text-blue-600 hover:text-blue-800">Seleccionar todo</button>
                <span class="text-gray-300">|</span>
                <button type="button" @click="clearAll" class="text-gray-500 hover:text-gray-700">Limpiar</button>
              </div>
            </div>
            <p class="text-xs text-gray-500 mb-3">Marca los módulos y los sub-apartados a los que tendrá acceso este rol.</p>

            <div class="space-y-2 border border-gray-200 rounded-lg overflow-hidden">
              <div
                v-for="mod in MODULES"
                :key="mod.id"
                class="border-b border-gray-100 last:border-b-0"
              >
                <!-- Módulo principal -->
                <label class="flex items-center gap-3 px-4 py-3 bg-gray-50 cursor-pointer hover:bg-gray-100 select-none">
                  <input
                    type="checkbox"
                    :checked="isModuleChecked(mod.id)"
                    :indeterminate.prop="isModuleIndeterminate(mod.id)"
                    @change="toggleModule(mod.id, $event.target.checked)"
                    class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <span class="text-sm font-semibold text-gray-800">{{ mod.label }}</span>
                  <span class="ml-auto text-xs text-gray-400">
                    {{ countChecked(mod.id) }}/{{ SUB_MODULES[mod.id].length }}
                  </span>
                </label>

                <!-- Sub-módulos (visible siempre, dimmed si módulo no activo) -->
                <div class="px-4 py-2 grid grid-cols-1 sm:grid-cols-2 gap-1.5"
                     :class="countChecked(mod.id) === 0 ? 'opacity-50' : ''">
                  <label
                    v-for="sub in SUB_MODULES[mod.id]"
                    :key="sub.id"
                    class="flex items-center gap-2 py-1 cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      :value="sub.id"
                      :checked="isSubChecked(mod.id, sub.id)"
                      @change="toggleSub(mod.id, sub.id, $event.target.checked)"
                      class="h-3.5 w-3.5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <span class="text-xs text-gray-700">{{ sub.label }}</span>
                  </label>
                </div>
              </div>
            </div>

            <p v-if="totalChecked === 0" class="mt-2 text-xs text-amber-600">
              Selecciona al menos un sub-módulo.
            </p>
          </div>
        </div>

        <!-- Actions -->
        <div class="mt-8 pt-6 border-t border-gray-200 flex justify-end gap-4">
          <router-link
            to="/admin/system/roles"
            class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Cancelar
          </router-link>
          <button
            type="submit"
            :disabled="saving || totalChecked === 0"
            class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {{ saving ? 'Guardando...' : (isEditing ? 'Guardar Cambios' : 'Crear Rol') }}
          </button>
        </div>
      </form>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AppLayout from '@/shared/components/AppLayout.vue'
import { useRolesStore } from '@/features/system/store/roles.store'
import { fetchRole } from '@/features/system/api/roles.api'
import { MODULES, SUB_MODULES } from '@/shared/constants/modules'
import { formatApiError } from '@/shared/utils/apiError'

const router = useRouter()
const route = useRoute()
const store = useRolesStore()

const isEditing = computed(() => !!route.params.id)
const saving = ref(false)
const error = ref(null)

const form = reactive({
  nombre: '',
  descripcion: '',
  // { moduleId: [submoduleId, ...] }
  modulos_permitidos: {},
})

// ──────────────────────────────────────
// Helpers para el estado de checkboxes
// ──────────────────────────────────────
const isModuleChecked = (moduleId) => {
  const subs = form.modulos_permitidos[moduleId]
  return !!subs && subs.length === SUB_MODULES[moduleId].length
}

const isModuleIndeterminate = (moduleId) => {
  const subs = form.modulos_permitidos[moduleId]
  return !!subs && subs.length > 0 && subs.length < SUB_MODULES[moduleId].length
}

const isSubChecked = (moduleId, subId) => {
  return form.modulos_permitidos[moduleId]?.includes(subId) ?? false
}

const countChecked = (moduleId) => form.modulos_permitidos[moduleId]?.length ?? 0

const totalChecked = computed(() =>
  Object.values(form.modulos_permitidos).reduce((acc, subs) => acc + subs.length, 0)
)

// ──────────────────────────────────────
// Handlers
// ──────────────────────────────────────
const toggleModule = (moduleId, checked) => {
  if (checked) {
    form.modulos_permitidos[moduleId] = SUB_MODULES[moduleId].map(s => s.id)
  } else {
    delete form.modulos_permitidos[moduleId]
  }
}

const toggleSub = (moduleId, subId, checked) => {
  if (checked) {
    if (!form.modulos_permitidos[moduleId]) form.modulos_permitidos[moduleId] = []
    if (!form.modulos_permitidos[moduleId].includes(subId)) {
      form.modulos_permitidos[moduleId].push(subId)
    }
  } else {
    if (!form.modulos_permitidos[moduleId]) return
    form.modulos_permitidos[moduleId] = form.modulos_permitidos[moduleId].filter(s => s !== subId)
    if (form.modulos_permitidos[moduleId].length === 0) {
      delete form.modulos_permitidos[moduleId]
    }
  }
}

const selectAll = () => {
  MODULES.forEach(mod => {
    form.modulos_permitidos[mod.id] = SUB_MODULES[mod.id].map(s => s.id)
  })
}

const clearAll = () => {
  MODULES.forEach(mod => delete form.modulos_permitidos[mod.id])
}

// ──────────────────────────────────────
// Lifecycle
// ──────────────────────────────────────
onMounted(async () => {
  if (isEditing.value) {
    try {
      const role = await fetchRole(route.params.id)
      form.nombre = role.nombre
      form.descripcion = role.descripcion ?? ''
      // Copiar el objeto de permisos
      Object.assign(form.modulos_permitidos, role.modulos_permitidos)
    } catch (e) {
      error.value = formatApiError(e, 'Error cargando el rol')
    }
  }
})

// ──────────────────────────────────────
// Submit
// ──────────────────────────────────────
const saveRole = async () => {
  if (totalChecked.value === 0) return

  saving.value = true
  error.value = null

  const payload = {
    nombre: form.nombre.trim(),
    descripcion: form.descripcion.trim() || null,
    modulos_permitidos: { ...form.modulos_permitidos },
  }

  try {
    if (isEditing.value) {
      await store.updateRoleAction(route.params.id, payload)
    } else {
      await store.createRoleAction(payload)
    }
    router.push('/admin/system/roles')
  } catch (e) {
    error.value = formatApiError(e, 'Error guardando el rol')
  } finally {
    saving.value = false
  }
}
</script>
