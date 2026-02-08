<script setup>
import { useAuthStore } from '@/features/auth/store/auth.store'
import NavBar from '@/shared/components/NavBar.vue'

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
