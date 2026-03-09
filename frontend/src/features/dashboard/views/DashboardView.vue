<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/features/auth/store/auth.store'
import { FIXED_ROLE_MODULES } from '@/shared/constants/modules'

const router = useRouter()
const auth = useAuthStore()

const FIXED_ROLES = Object.keys(FIXED_ROLE_MODULES)

// Redirigir segun el rol
onMounted(() => {
  if (!auth.isAuthenticated) {
    router.replace('/')
    return
  }

  if (auth.isAdmin) {
    router.replace('/admin')
  } else if (auth.isOperator) {
    router.replace('/admin/users')
  } else if (!FIXED_ROLES.includes(auth.user?.rol)) {
    // Rol personalizado: redirigir al primer módulo disponible
    const mods = auth.allowedModules
    if (mods && 'gestion_usuarios' in mods) {
      router.replace('/admin/users')
    } else if (mods && 'oferta_laboral' in mods) {
      router.replace('/admin/convocatorias')
    } else if (mods && 'perfiles_institucionales' in mods) {
      router.replace('/admin/profiles')
    } else if (mods && 'informes_reportes' in mods) {
      router.replace('/admin/reports')
    } else if (mods && 'evaluacion_perfiles' in mods) {
      router.replace('/mis-recomendaciones')
    } else if (mods && 'digitalizacion_perfiles' in mods) {
      router.replace('/digitalizacion/mi-perfil')
    } else {
      router.replace('/digitalizacion/mi-perfil')
    }
  } else {
    router.replace('/digitalizacion/mi-perfil')
  }
})
</script>

<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emi-navy-500"></div>
  </div>
</template>
