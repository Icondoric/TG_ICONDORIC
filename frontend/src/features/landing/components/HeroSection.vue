<template>
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
              @click="$emit('triggerUpload')"
              @dragover.prevent="$emit('dragOver')"
              @dragleave="$emit('dragLeave')"
              @drop.prevent="$emit('drop', $event)"
            >
              <div
                class="border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300"
                :class="isDragging ? 'border-emi-gold-500 bg-emi-gold-50' : 'border-gray-300 hover:border-emi-navy-400 hover:bg-gray-50'"
              >
                <div v-if="!isProcessing" class="space-y-4">
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

            <button
              class="w-full mt-6 bg-gradient-to-r from-emi-navy-600 to-emi-navy-700 hover:from-emi-navy-700 hover:to-emi-navy-800 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 hover:shadow-emi-lg flex items-center justify-center gap-2"
              @click="$emit('triggerUpload')"
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
</template>

<script setup>
defineProps({
  isDragging: { type: Boolean, default: false },
  isProcessing: { type: Boolean, default: false },
  processingFileName: { type: String, default: '' }
})

defineEmits(['triggerUpload', 'dragOver', 'dragLeave', 'drop'])
</script>
