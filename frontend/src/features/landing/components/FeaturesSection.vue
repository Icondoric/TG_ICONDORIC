<template>
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
</template>
