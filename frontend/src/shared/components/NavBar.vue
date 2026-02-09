<template>
  <nav
    v-if="shouldShowNavBar"
    class="fixed w-full top-0 left-0 z-50 transition-all duration-300"
    :class="navClasses"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <div @click="handleNavigation('/')" class="flex items-center cursor-pointer group">
          <img 
            src="@/shared/assets/icons/logoEmi.png"
            alt="Logo EMI" 
            class="h-10 w-auto transition-transform duration-300 group-hover:scale-105" 
          />
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden lg:flex items-center gap-6">
          <!-- Public Links (for non-admin users) -->
          <template v-if="!authStore.isAdminOrOperator">
            <a
              @click.prevent="handleNavigation('/')"
              :class="linkClasses"
            >
              Inicio
            </a>
            <a
              @click.prevent="scrollToSection('features')"
              :class="linkClasses"
            >
              Características
            </a>
            <a
              @click.prevent="scrollToSection('how-it-works')"
              :class="linkClasses"
            >
              Cómo Funciona
            </a>
          </template>

          <!-- Auth Buttons -->
          <template v-if="!authStore.isAuthenticated">
            <Button
              variant="ghost"
              size="sm"
              @click="handleNavigation('/login')"
            >
              Iniciar Sesión
            </Button>
            <Button
              variant="gold"
              size="sm"
              @click="handleNavigation('/register')"
            >
              Registrarse
            </Button>
          </template>

          <!-- Student/Graduate Menu -->
          <template v-else-if="!authStore.isAdminOrOperator">
            <Button
              :variant="route.path.startsWith('/mi-perfil') ? 'primary' : 'outline'"
              size="sm"
              @click="handleNavigation('/mi-perfil')"
            >
              Mi Perfil
            </Button>
            <Button
              variant="ghost"
              size="sm"
              @click="authStore.logout()"
              class="text-red-600 hover:text-red-700 hover:bg-red-50"
            >
              Cerrar Sesión
            </Button>
          </template>

          <!-- Admin Menu -->
          <template v-else>
            <a
              @click.prevent="handleNavigation('/')"
              :class="linkClasses"
            >
              Inicio
            </a>
            <Button
              :variant="route.path === '/admin' ? 'gold' : 'outline'"
              size="sm"
              @click="handleNavigation('/admin')"
            >
              Dashboard
            </Button>
            <Button
              :variant="route.path.startsWith('/admin/ofertas') ? 'gold' : 'ghost'"
              size="sm"
              @click="handleNavigation('/admin/ofertas')"
            >
              Ofertas
            </Button>
            <Button
              variant="ghost"
              size="sm"
              @click="authStore.logout()"
              class="text-red-600 hover:text-red-700 hover:bg-red-50"
            >
              Cerrar Sesión
            </Button>
          </template>
        </div>

        <!-- Mobile Menu Button -->
        <button
          @click="toggleMobileMenu"
          class="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
          :class="{ 'text-white hover:bg-white/10': isDashboardPage }"
        >
          <svg
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              v-if="!isMobileMenuOpen"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"
            />
            <path
              v-else
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-2"
    >
      <div
        v-if="isMobileMenuOpen"
        class="lg:hidden border-t"
        :class="isDashboardPage ? 'border-white/20 bg-emi-navy-600' : 'border-gray-200 bg-white'"
      >
        <div class="px-4 py-4 space-y-3">
          <!-- Public Links Mobile -->
          <template v-if="!authStore.isAdminOrOperator">
            <a
              @click.prevent="handleNavigation('/')"
              :class="mobileLinkClasses"
            >
              Inicio
            </a>
            <a
              @click.prevent="scrollToSection('features')"
              :class="mobileLinkClasses"
            >
              Características
            </a>
            <a
              @click.prevent="scrollToSection('how-it-works')"
              :class="mobileLinkClasses"
            >
              Cómo Funciona
            </a>
          </template>

          <!-- Auth Buttons Mobile -->
          <template v-if="!authStore.isAuthenticated">
            <Button
              variant="outline"
              size="md"
              full-width
              @click="handleNavigation('/login')"
            >
              Iniciar Sesión
            </Button>
            <Button
              variant="gold"
              size="md"
              full-width
              @click="handleNavigation('/register')"
            >
              Registrarse
            </Button>
          </template>

          <!-- Student Menu Mobile -->
          <template v-else-if="!authStore.isAdminOrOperator">
            <Button
              variant="primary"
              size="md"
              full-width
              @click="handleNavigation('/mi-perfil')"
            >
              Mi Perfil
            </Button>
            <Button
              variant="outline"
              size="md"
              full-width
              @click="authStore.logout()"
              class="text-red-600 border-red-600 hover:bg-red-50"
            >
              Cerrar Sesión
            </Button>
          </template>

          <!-- Admin Menu Mobile -->
          <template v-else>
            <a
              @click.prevent="handleNavigation('/')"
              :class="mobileLinkClasses"
            >
              Inicio
            </a>
            <Button
              variant="gold"
              size="md"
              full-width
              @click="handleNavigation('/admin')"
            >
              Dashboard
            </Button>
            <Button
              variant="outline"
              size="md"
              full-width
              @click="handleNavigation('/admin/ofertas')"
            >
              Ofertas
            </Button>
            <Button
              variant="outline"
              size="md"
              full-width
              @click="authStore.logout()"
              class="text-red-600 border-red-600 hover:bg-red-50"
            >
              Cerrar Sesión
            </Button>
          </template>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/features/auth/store/auth.store'
import Button from '@/shared/components/ui/Button.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const isScrolled = ref(false)
const isMobileMenuOpen = ref(false)

// Detect if we're on a dashboard page
const isDashboardPage = computed(() => {
  const dashboardRoutes = ['/mi-perfil', '/mis-recomendaciones', '/admin']
  return dashboardRoutes.some(r => route.path.startsWith(r))
})

// Determine if NavBar should be shown
const shouldShowNavBar = computed(() => {
  const publicRoutes = ['/', '/login', '/register', '/evaluation']
  const isDashboard = isDashboardPage.value
  return publicRoutes.includes(route.path) || !isDashboard
})

// NavBar classes with glassmorphism
const navClasses = computed(() => {
  if (isDashboardPage.value) {
    return 'bg-emi-navy-600 shadow-lg'
  }
  return isScrolled.value
    ? 'glass backdrop-blur-xl bg-white/95 shadow-emi'
    : 'bg-white/80 backdrop-blur-md shadow-sm'
})

// Link classes
const linkClasses = computed(() => {
  return isDashboardPage.value
    ? 'text-white hover:text-emi-gold-400 font-medium text-sm cursor-pointer transition-colors'
    : 'text-gray-700 hover:text-emi-gold-500 font-medium text-sm cursor-pointer transition-colors'
})

const mobileLinkClasses = computed(() => {
  return isDashboardPage.value
    ? 'block py-2 text-white hover:text-emi-gold-400 font-medium cursor-pointer transition-colors'
    : 'block py-2 text-gray-700 hover:text-emi-gold-500 font-medium cursor-pointer transition-colors'
})

const handleNavigation = (path) => {
  router.push(path)
  isMobileMenuOpen.value = false
}

const scrollToSection = (id) => {
  if (route.path !== '/') {
    router.push('/')
    setTimeout(() => {
      const element = document.getElementById(id)
      if (element) element.scrollIntoView({ behavior: 'smooth' })
    }, 100)
  } else {
    const element = document.getElementById(id)
    if (element) element.scrollIntoView({ behavior: 'smooth' })
  }
  isMobileMenuOpen.value = false
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

onMounted(() => {
  window.addEventListener('scroll', () => {
    isScrolled.value = window.scrollY > 50
  })
})
</script>
