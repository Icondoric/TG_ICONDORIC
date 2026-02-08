<template>
  <div class="landing-page">
    <!-- Navbar Component -->
    <NavBar />

    <!-- Hero Section -->
    <section class="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-emi-navy-900 via-emi-navy-800 to-emi-navy-900">
      <!-- Animated gradient mesh background -->
      <div class="absolute inset-0 opacity-30">
        <div class="absolute top-0 left-1/4 w-96 h-96 bg-emi-gold-500 rounded-full mix-blend-multiply filter blur-3xl animate-pulse-slow"></div>
        <div class="absolute top-1/3 right-1/4 w-96 h-96 bg-emi-navy-500 rounded-full mix-blend-multiply filter blur-3xl animate-pulse-slow" style="animation-delay: 1s;"></div>
        <div class="absolute bottom-1/4 left-1/3 w-96 h-96 bg-emi-gold-400 rounded-full mix-blend-multiply filter blur-3xl animate-pulse-slow" style="animation-delay: 2s;"></div>
      </div>

      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div class="grid lg:grid-cols-2 gap-12 items-center">
          <!-- Left: Content -->
          <div class="text-white space-y-8 animate-slide-up">
            <h1 class="font-display font-bold text-5xl lg:text-6xl leading-tight">
              Sistema de Evaluación de 
              <span class="text-gradient-emi bg-clip-text text-transparent bg-gradient-to-r from-emi-gold-400 to-emi-gold-600">
                Perfiles Profesionales
              </span> 
              Aplicando IA
            </h1>
            
            <p class="text-xl text-gray-300 leading-relaxed">
              Plataforma inteligente que aplica <span class="text-emi-gold-400 font-semibold">Procesamiento de Lenguaje Natural</span> y <span class="text-emi-gold-400 font-semibold">Machine Learning</span> para recomendar oportunidades laborales y de pasantía según tu perfil profesional
            </p>

            <!-- Stats badges -->
            <div class="flex flex-wrap gap-4 pt-4">
              <div class="glass px-6 py-4 rounded-2xl backdrop-blur-md bg-white/10 border border-white/20 hover:bg-white/15 transition-all duration-300 hover:scale-105">
                <div class="text-3xl font-bold text-emi-gold-400">92%</div>
                <div class="text-sm text-gray-300 mt-1">Precisión en evaluación</div>
              </div>
              <div class="glass px-6 py-4 rounded-2xl backdrop-blur-md bg-white/10 border border-white/20 hover:bg-white/15 transition-all duration-300 hover:scale-105">
                <div class="text-3xl font-bold text-emi-gold-400">&lt; 30s</div>
                <div class="text-sm text-gray-300 mt-1">Procesamiento NLP</div>
              </div>
              <div class="glass px-6 py-4 rounded-2xl backdrop-blur-md bg-white/10 border border-white/20 hover:bg-white/15 transition-all duration-300 hover:scale-105">
                <div class="text-3xl font-bold text-emi-gold-400">100+</div>
                <div class="text-sm text-gray-300 mt-1">Convenios activos</div>
              </div>
            </div>
          </div>

          <!-- Right: Upload Card -->
          <div class="animate-slide-up" style="animation-delay: 0.2s;">
            <div class="glass backdrop-blur-xl bg-white/95 rounded-3xl shadow-emi-lg p-8 border border-white/20">
              <h3 class="font-display font-bold text-2xl text-emi-navy-900 mb-2">Digitaliza tu Perfil</h3>
              <p class="text-gray-600 mb-6">Carga tu CV y recibe recomendaciones personalizadas de la EMI</p>
              
              <!-- Dropzone -->
              <div 
                class="relative group cursor-pointer transition-all duration-300"
                @click="triggerFileInput"
                @dragover.prevent="handleDragOver"
                @dragleave="handleDragLeave"
                @drop.prevent="handleDrop"
              >
                <div 
                  class="border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300"
                  :class="isDragging ? 'border-emi-gold-500 bg-emi-gold-50' : 'border-gray-300 hover:border-emi-navy-400 hover:bg-gray-50'"
                >
                  <div v-if="!isProcessing" class="space-y-4">
                    <!-- Icon -->
                    <div class="mx-auto w-20 h-20 bg-gradient-to-br from-emi-navy-500 to-emi-navy-700 rounded-2xl flex items-center justify-center transform group-hover:scale-110 transition-transform duration-300">
                      <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                    </div>
                    
                    <div>
                      <div class="text-lg font-semibold text-gray-900 mb-1">Arrastra tu CV aquí</div>
                      <div class="text-sm text-gray-500">o haz clic para seleccionar</div>
                      <div class="text-xs text-gray-400 mt-2">PDF, máx. 2MB</div>
                    </div>
                  </div>

                  <div v-else class="space-y-4">
                    <!-- Processing animation -->
                    <div class="mx-auto w-20 h-20 bg-gradient-to-br from-emi-gold-400 to-emi-gold-600 rounded-2xl flex items-center justify-center">
                      <svg class="w-10 h-10 text-white animate-spin" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                    </div>
                    <div>
                      <div class="text-lg font-semibold text-gray-900">Procesando con NLP...</div>
                      <div class="text-sm text-gray-500 mt-1">{{ processingFileName }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <input 
                type="file" 
                ref="fileInputRef" 
                accept=".pdf" 
                class="hidden" 
                @change="handleFileChange"
              >

              <button 
                class="w-full mt-6 bg-gradient-to-r from-emi-navy-600 to-emi-navy-700 hover:from-emi-navy-700 hover:to-emi-navy-800 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 hover:shadow-emi-lg flex items-center justify-center gap-2"
                @click="triggerFileInput"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Comenzar Evaluación
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-24 bg-gray-50" id="features">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16 animate-slide-up">
          <h2 class="font-display font-bold text-4xl lg:text-5xl text-emi-navy-900 mb-4">
            Tecnología de Vanguardia
          </h2>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            Sistema inteligente que conecta estudiantes y titulados de la EMI con oportunidades institucionales
          </p>
        </div>
        
        <div class="grid md:grid-cols-3 gap-8">
          <!-- Feature 1: NLP Extraction -->
          <div class="group bg-white rounded-2xl p-8 shadow-md hover:shadow-emi-lg transition-all duration-300 hover:-translate-y-2 animate-slide-up">
            <div class="w-16 h-16 bg-gradient-to-br from-emi-navy-500 to-emi-navy-700 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 class="font-display font-bold text-2xl text-emi-navy-900 mb-4">
              Extracción Automática con NLP
            </h3>
            <p class="text-gray-600 leading-relaxed">
              Procesamiento híbrido que combina <span class="font-semibold text-emi-navy-700">Regex</span> para datos de contacto y <span class="font-semibold text-emi-navy-700">spaCy</span> para identificar competencias técnicas y blandas en español
            </p>
          </div>

          <!-- Feature 2: ML Matching -->
          <div class="group bg-white rounded-2xl p-8 shadow-md hover:shadow-emi-lg transition-all duration-300 hover:-translate-y-2 animate-slide-up" style="animation-delay: 0.1s;">
            <div class="w-16 h-16 bg-gradient-to-br from-emi-gold-500 to-emi-gold-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 class="font-display font-bold text-2xl text-emi-navy-900 mb-4">
              Evaluación Inteligente con ML
            </h3>
            <p class="text-gray-600 leading-relaxed">
              Modelo de Machine Learning (<span class="font-semibold text-emi-navy-700">TF-IDF + Similitud Coseno</span>) que calcula la correspondencia entre tu perfil y las ofertas laborales con precisión del 92%
            </p>
          </div>

          <!-- Feature 3: Explainability -->
          <div class="group bg-white rounded-2xl p-8 shadow-md hover:shadow-emi-lg transition-all duration-300 hover:-translate-y-2 animate-slide-up" style="animation-delay: 0.2s;">
            <div class="w-16 h-16 bg-gradient-to-br from-emi-navy-500 to-emi-navy-700 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
            </div>
            <h3 class="font-display font-bold text-2xl text-emi-navy-900 mb-4">
              Explicabilidad Total
            </h3>
            <p class="text-gray-600 leading-relaxed">
              No solo recibes un porcentaje de compatibilidad. El sistema te muestra <span class="font-semibold text-emi-navy-700">exactamente</span> qué competencias coinciden y cuáles te faltan para cada oferta
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- How it Works -->
    <section class="py-24 bg-white" id="how-it-works">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16 animate-slide-up">
          <h2 class="font-display font-bold text-4xl lg:text-5xl text-emi-navy-900 mb-4">
            ¿Cómo Funciona?
          </h2>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            Proceso simple y transparente en 4 pasos
          </p>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <!-- Step 1 -->
          <div class="relative animate-slide-up">
            <div class="bg-gradient-to-br from-emi-navy-50 to-white rounded-2xl p-6 border border-emi-navy-100 hover:shadow-emi transition-all duration-300">
              <div class="w-12 h-12 bg-gradient-to-br from-emi-navy-600 to-emi-navy-700 rounded-xl flex items-center justify-center mb-4">
                <span class="text-white font-bold text-xl">1</span>
              </div>
              <h3 class="font-display font-bold text-xl text-emi-navy-900 mb-3">
                Sube tu CV
              </h3>
              <p class="text-gray-600 text-sm leading-relaxed">
                Carga tu currículum en PDF. El sistema extrae automáticamente tu información usando NLP
              </p>
            </div>
            <!-- Connector arrow (hidden on mobile) -->
            <div class="hidden lg:block absolute top-1/2 -right-4 transform -translate-y-1/2 z-10">
              <svg class="w-8 h-8 text-emi-gold-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </div>
          </div>

          <!-- Step 2 -->
          <div class="relative animate-slide-up" style="animation-delay: 0.1s;">
            <div class="bg-gradient-to-br from-emi-gold-50 to-white rounded-2xl p-6 border border-emi-gold-100 hover:shadow-gold transition-all duration-300">
              <div class="w-12 h-12 bg-gradient-to-br from-emi-gold-500 to-emi-gold-600 rounded-xl flex items-center justify-center mb-4">
                <span class="text-white font-bold text-xl">2</span>
              </div>
              <h3 class="font-display font-bold text-xl text-emi-navy-900 mb-3">
                Valida tus Datos
              </h3>
              <p class="text-gray-600 text-sm leading-relaxed">
                Revisa y corrige la información extraída. Tú tienes el control final sobre tu perfil
              </p>
            </div>
            <!-- Connector arrow -->
            <div class="hidden lg:block absolute top-1/2 -right-4 transform -translate-y-1/2 z-10">
              <svg class="w-8 h-8 text-emi-gold-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </div>
          </div>

          <!-- Step 3 -->
          <div class="relative animate-slide-up" style="animation-delay: 0.2s;">
            <div class="bg-gradient-to-br from-emi-navy-50 to-white rounded-2xl p-6 border border-emi-navy-100 hover:shadow-emi transition-all duration-300">
              <div class="w-12 h-12 bg-gradient-to-br from-emi-navy-600 to-emi-navy-700 rounded-xl flex items-center justify-center mb-4">
                <span class="text-white font-bold text-xl">3</span>
              </div>
              <h3 class="font-display font-bold text-xl text-emi-navy-900 mb-3">
                Evaluación ML
              </h3>
              <p class="text-gray-600 text-sm leading-relaxed">
                El modelo calcula la compatibilidad entre tu perfil y las ofertas disponibles
              </p>
            </div>
            <!-- Connector arrow -->
            <div class="hidden lg:block absolute top-1/2 -right-4 transform -translate-y-1/2 z-10">
              <svg class="w-8 h-8 text-emi-gold-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </div>
          </div>

          <!-- Step 4 -->
          <div class="animate-slide-up" style="animation-delay: 0.3s;">
            <div class="bg-gradient-to-br from-emi-gold-50 to-white rounded-2xl p-6 border border-emi-gold-100 hover:shadow-gold transition-all duration-300">
              <div class="w-12 h-12 bg-gradient-to-br from-emi-gold-500 to-emi-gold-600 rounded-xl flex items-center justify-center mb-4">
                <span class="text-white font-bold text-xl">4</span>
              </div>
              <h3 class="font-display font-bold text-xl text-emi-navy-900 mb-3">
                Recibe Recomendaciones
              </h3>
              <p class="text-gray-600 text-sm leading-relaxed">
                Obtén un ranking personalizado de oportunidades ordenadas por compatibilidad
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-24 bg-gradient-to-br from-emi-navy-900 via-emi-navy-800 to-emi-navy-900 relative overflow-hidden">
      <!-- Background decoration -->
      <div class="absolute inset-0 opacity-10">
        <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-emi-gold-500 rounded-full mix-blend-multiply filter blur-3xl"></div>
        <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-emi-navy-500 rounded-full mix-blend-multiply filter blur-3xl"></div>
      </div>

      <div class="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="font-display font-bold text-4xl lg:text-5xl text-white mb-6 animate-slide-up">
          ¿Listo para Descubrir tus Oportunidades?
        </h2>
        <p class="text-xl text-gray-300 mb-10 animate-slide-up" style="animation-delay: 0.1s;">
          Sistema desarrollado para el Vicerrectorado de Grado de la Escuela Militar de Ingeniería
        </p>
        <button 
          class="bg-gradient-to-r from-emi-gold-500 to-emi-gold-600 hover:from-emi-gold-600 hover:to-emi-gold-700 text-white font-bold py-4 px-10 rounded-xl text-lg transition-all duration-300 transform hover:scale-105 hover:shadow-gold animate-slide-up inline-flex items-center gap-3"
          style="animation-delay: 0.2s;"
          @click="scrollToTop"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Comenzar Evaluación
        </button>
      </div>
    </section>

    <!-- Footer -->
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

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import NavBar from '../components/NavBar.vue'

const router = useRouter()
const authStore = useAuthStore()
const fileInputRef = ref(null)
const isDragging = ref(false)
const isProcessing = ref(false)
const processingFileName = ref('')

const scrollToSection = (id) => {
  const element = document.getElementById(id)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
}

const triggerFileInput = () => {
  fileInputRef.value.click()
}

const handleDragOver = () => {
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

const handleDrop = (e) => {
  isDragging.value = false
  const file = e.dataTransfer.files[0]
  if (file) validateAndProcessFile(file)
}

const handleFileChange = (e) => {
  const file = e.target.files[0]
  if (file) validateAndProcessFile(file)
}

const validateAndProcessFile = (file) => {
  if (file.type !== 'application/pdf') {
    alert('Por favor sube un archivo PDF válido')
    return
  }
  
  if (file.size > 2 * 1024 * 1024) {
    alert('El archivo no debe superar 2MB')
    return
  }

  processFile(file)
}

const processFile = (file) => {
  isProcessing.value = true
  processingFileName.value = file.name
  
  // Simulation of processing
  setTimeout(() => {
    alert('En la versión completa, serías redirigido al formulario de validación con tus datos pre-llenados.')
    // Here we would navigate to the validation or register page with the file
    // router.push({ name: 'register', query: { from: 'upload' } }) 
    isProcessing.value = false
    processingFileName.value = ''
    router.push('/register') // Redirecting to register for now as per "Phase 1" flows likely needing auth or at least profile creation
  }, 2000)
}
</script>

<style scoped>
/* Scoped styles based on the provided CSS */
.landing-page {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #1f2937; /* var(--text-dark) */
  line-height: 1.6;
  overflow-x: hidden;
  --primary: #1e40af;
  --primary-dark: #1e3a8a;
  --secondary: #10b981;
  --accent: #f59e0b;
  --text-dark: #1f2937;
  --text-light: #6b7280;
  --bg-light: #f9fafb;
}

/* Navbar Styles Removed - Using Component */


/* Hero Section */
.hero {
  margin-top: 80px;
  min-height: 90vh;
  background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="2" fill="white" opacity="0.1"/></svg>');
  animation: float 20s linear infinite;
}

@keyframes float {
  to { transform: translateY(-100px); }
}

.hero-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 4rem 2rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  position: relative;
  z-index: 1;
}

.hero-content h1 {
  font-size: 3rem;
  color: white;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.hero-content p {
  font-size: 1.2rem;
  color: rgba(255,255,255,0.9);
  margin-bottom: 2rem;
}

.hero-stats {
  display: flex;
  gap: 3rem;
  margin-top: 2rem;
}

.stat {
  text-align: center;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: var(--accent);
  display: block;
}

.stat-label {
  color: rgba(255,255,255,0.8);
  font-size: 0.9rem;
}

/* Upload Card */
.upload-card {
  background: white;
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  text-align: center;
}

.upload-card h3 {
  color: var(--text-dark);
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

.upload-card p {
  color: var(--text-light);
  margin-bottom: 2rem;
}

.dropzone {
  border: 3px dashed #cbd5e1;
  border-radius: 12px;
  padding: 3rem 2rem;
  cursor: pointer;
  transition: all 0.3s;
  background: var(--bg-light);
}

.dropzone:hover, .dropzone.border-primary {
  border-color: var(--primary);
  background: rgba(30, 64, 175, 0.05);
  transform: scale(1.02);
}

.dropzone-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.btn-upload {
  width: 100%;
  background: var(--secondary);
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 1.5rem;
  transition: all 0.3s;
}

.btn-upload:hover {
  background: #059669;
  transform: translateY(-2px);
}

/* Features Section */
.features {
  padding: 6rem 2rem;
  background: white;
}

.features-container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  color: var(--text-dark);
  margin-bottom: 1rem;
}

.section-subtitle {
  text-align: center;
  color: var(--text-light);
  font-size: 1.2rem;
  margin-bottom: 4rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-card {
  padding: 2rem;
  border-radius: 12px;
  background: var(--bg-light);
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: var(--text-dark);
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

/* How it Works */
.how-it-works {
  padding: 6rem 2rem;
  background: var(--bg-light);
}

.steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 3rem;
  margin-top: 4rem;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.step {
  text-align: center;
}

.step-number {
  width: 60px;
  height: 60px;
  background: var(--primary);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0 auto 1.5rem;
}

/* About Section Styles */
.about-section {
    max-width: 1200px;
    margin: 4rem auto;
    padding: 0 2rem;
}

.section-header {
    text-align: center;
    margin-bottom: 4rem;
}

.section-title {
    font-size: 3rem;
    color: var(--primary);
    margin-bottom: 1rem;
    font-weight: 700;
}

.section-subtitle {
    font-size: 1.3rem;
    color: var(--text-light);
    max-width: 800px;
    margin: 0 auto;
}

/* Main Description */
.main-description {
    background: white;
    padding: 3rem;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 3rem;
}

.main-description h3 {
    color: var(--primary);
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.main-description p {
    color: var(--text-dark);
    font-size: 1.1rem;
    line-height: 1.8;
    margin-bottom: 1.2rem;
}

.highlight-box {
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    padding: 1.5rem;
    border-radius: 12px;
    border-left: 4px solid var(--primary);
    margin: 2rem 0;
}

.highlight-box strong {
    color: var(--primary);
}

/* Problem-Solution Grid */
.problem-solution {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin: 3rem 0;
}

.ps-card {
    background: white;
    padding: 2.5rem;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.ps-card h4 {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.ps-card.problem h4 {
    color: #dc2626;
}

.ps-card.solution h4 {
    color: var(--secondary);
}

.ps-list {
    list-style: none;
    padding: 0;
}

.ps-list li {
    padding: 0.8rem 0;
    padding-left: 2rem;
    position: relative;
    color: var(--text-dark);
}

.ps-list li::before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.problem .ps-list li::before {
    background: #dc2626;
}

.solution .ps-list li::before {
    background: var(--secondary);
}

/* Objectives Section */
.objectives {
    background: white;
    padding: 3rem;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin: 3rem 0;
}

.objectives h3 {
    color: var(--primary);
    font-size: 1.8rem;
    margin-bottom: 2rem;
    text-align: center;
}

.objective-item {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 2rem;
    padding: 1.5rem;
    background: var(--bg-light);
    border-radius: 12px;
    transition: all 0.3s;
}

.objective-item:hover {
    transform: translateX(10px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.objective-number {
    flex-shrink: 0;
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: bold;
}

.objective-content h4 {
    color: var(--text-dark);
    margin-bottom: 0.5rem;
    font-size: 1.2rem;
}

.objective-content p {
    color: var(--text-light);
}

/* Methodologies */
.methodologies {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin: 3rem 0;
}

.methodology-card {
    background: white;
    padding: 2.5rem;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    text-align: center;
    transition: all 0.3s;
}

.methodology-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}

.methodology-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.methodology-card h4 {
    color: var(--primary);
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.methodology-card p {
    color: var(--text-light);
}

.methodology-phases {
    margin-top: 1.5rem;
    text-align: left;
}

.phase-tag {
    display: inline-block;
    background: var(--bg-light);
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    font-size: 0.85rem;
    margin: 0.3rem; /* Adjusted for wrapping */
    color: var(--text-dark);
}

/* Team Section */
.team-section {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    padding: 3rem;
    border-radius: 16px;
    color: white;
    margin: 3rem 0;
}

.team-section h3 {
    font-size: 1.8rem;
    margin-bottom: 2rem;
    text-align: center;
    color: white; /* Ensure title is white */
}

.team-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}

.team-member {
    text-align: center;
    padding: 2rem;
    background: rgba(255,255,255,0.1);
    border-radius: 12px;
    backdrop-filter: blur(10px);
}

.team-avatar {
    width: 100px;
    height: 100px;
    background: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
    font-size: 2.5rem;
}

.team-name {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: white; 
}

.team-role {
    opacity: 0.9;
    font-size: 0.95rem;
    color: white;
}

/* Timeline */
.timeline {
    background: white;
    padding: 3rem;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin: 3rem 0;
}

.timeline h3 {
    color: var(--primary);
    font-size: 1.8rem;
    margin-bottom: 2rem;
    text-align: center;
}

.timeline-item {
    display: flex;
    gap: 2rem;
    margin-bottom: 2rem;
    position: relative;
}

.timeline-item::before {
    content: '';
    position: absolute;
    left: 29px;
    top: 60px;
    bottom: -20px;
    width: 2px;
    background: var(--bg-light);
}

.timeline-item:last-child::before {
    display: none;
}

.timeline-date {
    flex-shrink: 0;
    width: 60px;
    height: 60px;
    background: var(--primary);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 0.9rem;
    text-align: center;
}

.timeline-content {
    flex: 1;
    padding-top: 0.5rem;
}

.timeline-content h4 {
    color: var(--text-dark);
    margin-bottom: 0.5rem;
}

.timeline-content p {
    color: var(--text-light);
}

/* Stats */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    margin: 3rem 0;
}

.stat-card {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    text-align: center;
}

.stat-number {
    font-size: 3rem;
    font-weight: bold;
    color: var(--primary);
    display: block;
    margin-bottom: 0.5rem;
}

.stat-label {
    color: var(--text-light);
    font-size: 0.95rem;
}

@media (max-width: 768px) {
    .problem-solution {
        grid-template-columns: 1fr;
    }

    .main-description {
        padding: 2rem;
    }
    
    .timeline-item {
        gap: 1rem;
    }
}

/* CTA Section */
.cta {
  padding: 6rem 2rem;
  background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  text-align: center;
  color: white;
}

.cta h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.btn-cta {
  background: white;
  color: var(--primary);
  padding: 1rem 3rem;
  border: none;
  border-radius: 8px;
  font-size: 1.2rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-cta:hover {
  transform: scale(1.05);
}

/* Footer */
footer {
  background: var(--text-dark);
  color: white;
  padding: 3rem 2rem 1rem;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.footer-section h4 {
  margin-bottom: 1rem;
  color: var(--accent);
}

.footer-bottom {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.5);
}

@media (max-width: 768px) {
  .hero-container {
    grid-template-columns: 1fr;
  }

  .hero-content h1 {
    font-size: 2rem;
  }

  .nav-links {
    display: none;
  }
}
</style>
