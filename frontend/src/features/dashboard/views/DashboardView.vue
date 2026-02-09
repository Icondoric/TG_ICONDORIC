<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/features/auth/store/auth.store'

const router = useRouter()
const auth = useAuthStore()

// Redirigir segun el rol
onMounted(() => {
  if (auth.isAuthenticated) {
    if (auth.isAdmin) {
      router.replace('/admin')
    } else if (auth.isOperator) {
      router.replace('/admin/users')
    } else {
      router.replace('/mi-perfil')
    }
  } else {
    router.replace('/')
  }
})
</script>

<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emi-navy-500"></div>
  </div>
</template>
