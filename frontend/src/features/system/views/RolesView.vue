<template>
  <AppLayout>
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Roles del Sistema</h1>
          <p class="mt-1 text-sm text-gray-500">Gestiona los roles personalizados y sus permisos de acceso.</p>
        </div>
        <router-link
          to="/admin/system/roles/new"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm font-medium"
        >
          + Nuevo Rol
        </router-link>
      </div>

      <!-- Error -->
      <div v-if="store.error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
        <p class="text-red-700">{{ store.error }}</p>
      </div>

      <!-- Loading -->
      <div v-if="store.loading" class="text-center py-12 text-gray-500">Cargando roles...</div>

      <!-- Empty -->
      <div v-else-if="!store.roles.length" class="text-center py-12 bg-white rounded-lg shadow">
        <p class="text-gray-500">No hay roles personalizados. Crea el primero.</p>
      </div>

      <!-- Table -->
      <div v-else class="bg-white shadow rounded-lg overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Descripción</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Módulos</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="role in store.roles" :key="role.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="text-sm font-semibold text-gray-900">{{ role.nombre }}</span>
              </td>
              <td class="px-6 py-4">
                <span class="text-sm text-gray-600">{{ role.descripcion || '—' }}</span>
              </td>
              <td class="px-6 py-4">
                <div class="flex flex-wrap gap-1">
                  <template v-if="Object.keys(role.modulos_permitidos).length">
                    <span
                      v-for="(subs, modId) in role.modulos_permitidos"
                      :key="modId"
                      class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800"
                      :title="subs.join(', ')"
                    >
                      {{ moduleLabel(modId) }}
                      <span class="bg-blue-200 rounded px-1 font-bold">{{ subs.length }}</span>
                    </span>
                  </template>
                  <span v-else class="text-xs text-gray-400">Sin acceso</span>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm">
                <router-link
                  :to="`/admin/system/roles/${role.id}/edit`"
                  class="text-blue-600 hover:text-blue-800 mr-4"
                >
                  Editar
                </router-link>
                <button
                  @click="confirmDelete(role)"
                  class="text-red-600 hover:text-red-800"
                >
                  Eliminar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Confirm delete modal -->
      <div v-if="roleToDelete" class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg shadow-xl p-6 max-w-sm w-full mx-4">
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Eliminar rol</h3>
          <p class="text-gray-600 text-sm mb-6">
            ¿Estás seguro de que deseas eliminar el rol <strong>{{ roleToDelete.nombre }}</strong>?
            Los usuarios con este rol perderán sus permisos.
          </p>
          <div class="flex justify-end gap-3">
            <button
              @click="roleToDelete = null"
              class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 text-sm"
            >
              Cancelar
            </button>
            <button
              @click="handleDelete"
              :disabled="deleting"
              class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50 text-sm"
            >
              {{ deleting ? 'Eliminando...' : 'Eliminar' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppLayout from '@/shared/components/AppLayout.vue'
import { useRolesStore } from '@/features/system/store/roles.store'
import { MODULES, SUB_MODULES } from '@/shared/constants/modules'
import { formatApiError } from '@/shared/utils/apiError'

const store = useRolesStore()
const roleToDelete = ref(null)
const deleting = ref(false)

const moduleLabel = (id) => MODULES.find(m => m.id === id)?.label ?? id

const confirmDelete = (role) => {
  roleToDelete.value = role
}

const handleDelete = async () => {
  deleting.value = true
  try {
    await store.deleteRoleAction(roleToDelete.value.id)
    roleToDelete.value = null
  } catch (e) {
    store.error = formatApiError(e, 'Error eliminando rol')
  } finally {
    deleting.value = false
  }
}

onMounted(() => store.loadRoles())
</script>
