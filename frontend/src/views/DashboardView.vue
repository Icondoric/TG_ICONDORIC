<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

// Redirigir al nuevo sistema de perfil
onMounted(() => {
  if (auth.isAuthenticated) {
    if (auth.isAdmin) {
      router.replace('/admin')
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
