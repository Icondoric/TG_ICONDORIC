<template>
  <section class="py-24 bg-gray-50" id="features">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16 animate-slide-up">
        <h2 class="font-display font-bold text-4xl lg:text-5xl text-emi-navy-900 mb-4">
          Características Principales del SEPP
        </h2>
        <!-- 
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
        ...
        </p>
        -->
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
            Digitalización Estructurada con PLN
          </h3>
          <p class="text-gray-600 leading-relaxed">
            Utiliza un pipeline de Procesamiento de Lenguaje Natural que combina <span class="font-semibold text-emi-navy-700"> pdfplumber, spaCy y la API de Google Gemini </span> para leer tu currículum en PDF. El sistema extrae y estructura tu información en 5 dimensiones clave: <span class="font-semibold text-emi-navy-700"> habilidades técnicas, habilidades blandas, formación, experiencia e idiomas</span>.
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
            Evaluación Inteligente con Machine Learning
          </h3>
          <p class="text-gray-600 leading-relaxed">
            Implementa un modelo predictivo basado en <span class="font-semibold text-emi-navy-700">Regresión Ridge</span> Este algoritmo procesa un vector de 18 características para calcular la correspondencia exacta entre tu perfil y las demandas de la institución.
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
            Resultados Claros y Accionables
          </h3>
          <p class="text-gray-600 leading-relaxed">
            El sistema te clasifica en tres niveles objetivos <span class="font-semibold text-emi-navy-700">(APTO, CONSIDERADO o NO APTO)</span> basados en un umbral institucional. Además del porcentaje global, recibes un desglose visual por cada dimensión evaluada, identificando tus principales fortalezas y las debilidades frente a cada convocatoria.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>
