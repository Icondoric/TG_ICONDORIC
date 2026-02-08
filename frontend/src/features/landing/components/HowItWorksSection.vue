<template>
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
</template>
