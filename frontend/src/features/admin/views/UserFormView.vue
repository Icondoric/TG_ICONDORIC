<template>
  <AppLayout>
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <router-link to="/admin/users" class="text-blue-600 hover:text-blue-800 flex items-center mb-4">
          <svg class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Volver a Usuarios
        </router-link>
        <h1 class="text-3xl font-bold text-gray-900">Nuevo Usuario</h1>
      </div>

      <!-- Form -->
      <form @submit.prevent="saveUser" class="bg-white rounded-lg shadow p-6">
        <!-- Error -->
        <div v-if="error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-red-700">{{ error }}</p>
        </div>

        <!-- Success -->
        <div v-if="success" class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <p class="text-green-700">{{ success }}</p>
        </div>

        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700">Nombre Completo *</label>
            <input
              v-model="form.nombre_completo"
              type="text"
              required
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              placeholder="Ej: Juan Perez Lopez"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Email *</label>
            <input
              v-model="form.email"
              type="email"
              required
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              placeholder="usuario@email.com"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Contrasena *</label>
            <div class="mt-1 flex gap-2">
              <input
                v-model="form.password"
                type="text"
                required
                minlength="6"
                class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                placeholder="Minimo 6 caracteres"
              />
              <button
                type="button"
                @click="generatePassword"
                class="px-4 py-2 bg-gray-100 border border-gray-300 rounded-md text-sm text-gray-700 hover:bg-gray-200 whitespace-nowrap"
              >
                Generar
              </button>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Rol *</label>
            <select
              v-model="form.rol"
              required
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Seleccionar...</option>
              <option value="estudiante">Estudiante</option>
              <option value="titulado">Titulado</option>
              <option value="operador">Operador</option>
              <option value="administrador">Administrador</option>
            </select>
          </div>
        </div>

        <!-- Actions -->
        <div class="mt-8 pt-6 border-t border-gray-200 flex justify-end gap-4">
          <router-link
            to="/admin/users"
            class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Cancelar
          </router-link>
          <button
            type="submit"
            :disabled="saving"
            class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {{ saving ? 'Creando...' : 'Crear Usuario' }}
          </button>
        </div>
      </form>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { createUser } from '@/features/admin/api/users.api'
import AppLayout from '@/shared/components/AppLayout.vue'

const router = useRouter()

const form = reactive({
  nombre_completo: '',
  email: '',
  password: '',
  rol: ''
})

const saving = ref(false)
const error = ref(null)
const success = ref(null)

const generatePassword = () => {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789!@#$%'
  let password = ''
  for (let i = 0; i < 12; i++) {
    password += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  form.password = password
}

const saveUser = async () => {
  saving.value = true
  error.value = null
  success.value = null

  try {
    await createUser({
      nombre_completo: form.nombre_completo,
      email: form.email,
      password: form.password,
      rol: form.rol
    })

    router.push('/admin/users')

  } catch (e) {
    error.value = e.response?.data?.detail || 'Error creando usuario'
  } finally {
    saving.value = false
  }
}
</script>
