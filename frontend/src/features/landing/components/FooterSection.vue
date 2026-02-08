<template>
  <footer class="bg-emi-navy-900 text-white py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid md:grid-cols-3 gap-8 mb-8">
        <!-- Column 1: About -->
        <div>
          <h3 class="font-display font-bold text-xl mb-4 text-emi-gold-400">Sistema EMI</h3>
          <p class="text-gray-400 text-sm leading-relaxed">
            Plataforma inteligente de evaluación de perfiles profesionales con IA para la Escuela Militar de Ingeniería
          </p>
        </div>

        <!-- Column 2: Quick Links -->
        <div>
          <h3 class="font-display font-bold text-xl mb-4 text-emi-gold-400">Enlaces Rápidos</h3>
          <ul class="space-y-2 text-sm">
            <li>
              <a href="#features" class="text-gray-400 hover:text-emi-gold-400 transition-colors duration-200">Características</a>
            </li>
            <li>
              <a href="#how-it-works" class="text-gray-400 hover:text-emi-gold-400 transition-colors duration-200">Cómo Funciona</a>
            </li>
            <li>
              <router-link to="/login" class="text-gray-400 hover:text-emi-gold-400 transition-colors duration-200">Iniciar Sesión</router-link>
            </li>
            <li>
              <router-link to="/register" class="text-gray-400 hover:text-emi-gold-400 transition-colors duration-200">Registrarse</router-link>
            </li>
          </ul>
        </div>

        <!-- Column 3: Contact -->
        <div>
          <h3 class="font-display font-bold text-xl mb-4 text-emi-gold-400">Contacto</h3>
          <ul class="space-y-2 text-sm text-gray-400">
            <li class="flex items-start gap-2">
              <svg class="w-5 h-5 text-emi-gold-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              <span>Escuela Militar de Ingeniería<br>Vicerrectorado de Grado</span>
            </li>
            <li class="flex items-center gap-2">
              <svg class="w-5 h-5 text-emi-gold-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <span>vinculacion@emi.edu.bo</span>
            </li>
          </ul>
        </div>
      </div>

      <!-- Bottom bar -->
      <div class="border-t border-gray-800 pt-8 text-center">
        <p class="text-gray-400 text-sm">
          © {{ new Date().getFullYear() }} Escuela Militar de Ingeniería. Trabajo de Grado - Ingeniería de Sistemas.
        </p>
        <p class="text-gray-500 text-xs mt-2">
          Desarrollado con Vue.js, FastAPI, spaCy y scikit-learn
        </p>
      </div>
    </div>
  </footer>
</template>
