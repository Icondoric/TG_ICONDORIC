<script setup>
import { useAuthStore } from './stores/auth' // Keeping for potential global logic
import NavBar from './components/NavBar.vue'

const auth = useAuthStore()
</script>

<template>
  <div class="min-h-screen bg-slate-50">
    <!-- Navbar Global -->
    <NavBar v-if="!$route.meta.hideNavbar" />

    <main>
      <router-view></router-view>
    </main>
  </div>
</template>
