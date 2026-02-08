<template>
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
        @click="$emit('scrollToTop')"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        Comenzar Evaluación
      </button>
    </div>
  </section>
</template>

<script setup>
defineEmits(['scrollToTop'])
</script>
