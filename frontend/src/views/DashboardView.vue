<script setup>
import FileUpload from '../components/FileUpload.vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
</script>

<template>
  <div class="max-w-7xl mx-auto py-12 px-4">
    <header class="mb-10 text-center">
        <h1 class="text-4xl font-extrabold text-slate-900 tracking-tight sm:text-5xl">
          Digitalización de Perfiles
        </h1>
        <p class="mt-4 text-xl text-slate-600">
          Bienvenido, {{ auth.user?.email || 'Estudiante' }}. Sube tu CV para comenzar.
        </p>
    </header>

    <div class="bg-white rounded-lg shadow p-6">
        <FileUpload /> 
    </div>
  </div>
</template>
