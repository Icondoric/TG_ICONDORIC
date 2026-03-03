<template>
  <AppLayout>
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <router-link to="/admin/users" class="text-emi-navy-500 hover:text-emi-gold flex items-center mb-4 transition-colors">
          <svg class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Volver a Usuarios
        </router-link>
        <h1 class="text-3xl font-bold text-emi-navy-500">Nuevo Usuario</h1>
      </div>

      <!-- Form -->
      <form @submit.prevent="saveUser" class="card-emi p-6">
        <!-- Error -->
        <div v-if="error" class="mb-6 p-4 bg-danger-50 border border-danger-200 rounded-lg">
          <p class="text-danger-700 whitespace-pre-line">{{ error }}</p>
        </div>

        <!-- Success -->
        <div v-if="success" class="mb-6 p-4 bg-success-50 border border-success-200 rounded-lg">
          <p class="text-success-700">{{ success }}</p>
        </div>

        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700">Nombre Completo *</label>
            <input
              v-model="form.nombre_completo"
              type="text"
              required
              class="mt-1 block w-full border-slate-300 rounded-md shadow-sm focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
              placeholder="Ej: Juan Perez Lopez"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Email *</label>
            <input
              v-model="form.email"
              type="email"
              required
              class="mt-1 block w-full border-slate-300 rounded-md shadow-sm focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
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
                class="block w-full border-slate-300 rounded-md shadow-sm focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
                placeholder="Minimo 6 caracteres"
              />
              <button
                type="button"
                @click="generatePassword"
                class="btn-emi-secondary whitespace-nowrap"
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
              class="mt-1 block w-full border-slate-300 rounded-md shadow-sm focus:ring-emi-navy-500 focus:border-emi-navy-500 transition-colors"
            >
              <option value="">Seleccionar...</option>
              <optgroup label="Roles del sistema">
                <option value="estudiante">Estudiante</option>
                <option value="titulado">Titulado</option>
                <option value="operador">Operador</option>
                <option value="administrador">Administrador</option>
              </optgroup>
              <optgroup v-if="customRoles.length" label="Roles personalizados">
                <option v-for="r in customRoles" :key="r.id" :value="r.nombre">
                  {{ r.nombre }}
                </option>
              </optgroup>
            </select>
          </div>
        </div>

        <!-- Actions -->
        <div class="mt-8 pt-6 border-t border-slate-200 flex justify-end gap-4">
          <router-link
            to="/admin/users"
            class="px-4 py-2 border border-slate-300 rounded-md text-slate-700 hover:bg-slate-50 transition-colors"
          >
            Cancelar
          </router-link>
          <button
            type="submit"
            :disabled="saving"
            class="btn-emi-primary"
          >
            {{ saving ? 'Creando...' : 'Crear Usuario' }}
          </button>
        </div>
      </form>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { createUser } from '@/features/admin/api/users.api'
import { fetchRoles } from '@/features/system/api/roles.api'
import AppLayout from '@/shared/components/AppLayout.vue'
import { formatApiError } from '@/shared/utils/apiError'

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
const customRoles = ref([])

onMounted(async () => {
  try {
    customRoles.value = await fetchRoles()
  } catch {
    // Si falla la carga de roles personalizados, el select muestra solo los fijos
  }
})

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
    error.value = formatApiError(e, 'Error creando usuario')
  } finally {
    saving.value = false
  }
}
</script>
