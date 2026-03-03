<template>
  <AppLayout>

    <!-- ══════════════════════════════════════════════════════
         CARGANDO
    ══════════════════════════════════════════════════════ -->
    <div v-if="loading" class="min-h-[80vh] flex flex-col items-center justify-center select-none px-4">
      <div class="relative w-44 h-44 mb-10">
        <div class="absolute inset-0   rounded-full bg-emi-navy-100 animate-ping opacity-20" style="animation-duration:2.2s"></div>
        <div class="absolute inset-6   rounded-full bg-emi-navy-200 animate-ping opacity-30" style="animation-duration:2.2s;animation-delay:.45s"></div>
        <div class="absolute inset-12  rounded-full bg-emi-navy-300 animate-ping opacity-40" style="animation-duration:2.2s;animation-delay:.9s"></div>
        <div class="absolute inset-0 flex items-center justify-center">
          <div class="w-20 h-20 bg-gradient-to-br from-emi-navy-600 to-emi-navy-800 rounded-full flex items-center justify-center shadow-2xl">
            <svg class="w-9 h-9 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
      </div>
      <h2 class="text-2xl sm:text-3xl font-bold text-emi-navy-700 text-center mb-3">{{ loadingPhase }}</h2>
      <p class="text-gray-400 text-sm text-center max-w-sm leading-relaxed">
        Nuestro sistema analiza tu perfil completo y lo compara con cada oferta disponible para encontrar la que mejor se adapta a tus habilidades y formación.
      </p>
      <div class="flex gap-2.5 mt-8">
        <div class="w-2.5 h-2.5 bg-emi-navy-400 rounded-full animate-bounce" style="animation-delay:0s"></div>
        <div class="w-2.5 h-2.5 bg-emi-navy-400 rounded-full animate-bounce" style="animation-delay:.15s"></div>
        <div class="w-2.5 h-2.5 bg-emi-navy-400 rounded-full animate-bounce" style="animation-delay:.3s"></div>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════
         NO ELEGIBLE
    ══════════════════════════════════════════════════════ -->
    <div v-else-if="!isEligible" class="max-w-2xl mx-auto px-4 py-12">
      <EligibilityWarning
        :reason="eligibilityReason"
        :action="eligibilityAction"
        :missingFields="missingFields"
      />
    </div>

    <!-- ══════════════════════════════════════════════════════
         ERROR
    ══════════════════════════════════════════════════════ -->
    <div v-else-if="error" class="max-w-lg mx-auto px-4 py-20 text-center">
      <div class="w-16 h-16 bg-danger-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-danger-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <p class="text-danger-600 text-sm mb-6 whitespace-pre-line">{{ error }}</p>
      <button @click="loadRecommendations" class="btn-emi-primary">Reintentar</button>
    </div>

    <!-- ══════════════════════════════════════════════════════
         SIN RECOMENDACIONES
    ══════════════════════════════════════════════════════ -->
    <div v-else-if="!bestMatch" class="max-w-lg mx-auto px-4 py-20 text-center">
      <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
      </div>
      <h3 class="text-lg font-semibold text-gray-700 mb-2">No hay recomendaciones disponibles</h3>
      <p class="text-gray-500 text-sm mb-8 max-w-sm mx-auto">No encontramos ofertas activas para tu perfil. Asegúrate de que tu CV esté completo y actualizado.</p>
      <div class="flex justify-center gap-3 flex-wrap">
        <router-link to="/digitalizacion/mi-perfil"
          class="px-5 py-2.5 border border-emi-navy-300 text-emi-navy-600 rounded-lg hover:bg-emi-navy-50 transition-colors font-medium text-sm">
          Revisar Mi Perfil
        </router-link>
        <button @click="loadRecommendations(true)" class="btn-emi-primary text-sm">Reintentar</button>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════
         CONTENIDO PRINCIPAL
    ══════════════════════════════════════════════════════ -->
    <div v-else class="px-4 sm:px-6 lg:px-10 xl:px-16 py-8 max-w-screen-xl mx-auto">

      <!-- Encabezado de página -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-emi-navy-500">Mejor Correspondencia</h1>
        <p class="mt-2 text-gray-600">
          Tu oferta con mayor compatibilidad
          <span v-if="totalCount > 1"> — evaluada entre {{ totalCount }} ofertas activas</span>
        </p>
      </div>

      <!-- ── Layout principal: 2 columnas ── -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 xl:gap-8">

        <!-- ════════════════════════════════
             COLUMNA IZQUIERDA (2/3)
        ════════════════════════════════ -->
        <div class="lg:col-span-2 space-y-6">

          <!-- Score Hero -->
          <div class="bg-gradient-to-br from-emi-navy-700 via-emi-navy-800 to-emi-navy-900 rounded-2xl p-6 sm:p-8 text-white shadow-xl">
            <div class="flex flex-col sm:flex-row items-center sm:items-start gap-6">

              <!-- Círculo de puntuación -->
              <div class="relative w-32 h-32 shrink-0">
                <svg class="w-32 h-32 -rotate-90" viewBox="0 0 120 120">
                  <circle cx="60" cy="60" r="50" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="10"/>
                  <circle cx="60" cy="60" r="50" fill="none"
                    :stroke="scoreRingColor" stroke-width="10" stroke-linecap="round"
                    :stroke-dasharray="`${bestMatch.match_score * 314.16} 314.16`"
                    style="transition:stroke-dasharray 1.4s cubic-bezier(.4,0,.2,1)"
                  />
                </svg>
                <div class="absolute inset-0 flex flex-col items-center justify-center">
                  <span class="text-4xl font-extrabold leading-none">{{ Math.round(bestMatch.match_score * 100) }}</span>
                  <span class="text-sm opacity-60 mt-0.5">/ 100</span>
                </div>
              </div>

              <!-- Lado derecho del hero -->
              <div class="flex-1 w-full">
                <div class="flex flex-wrap items-center gap-3 mb-4">
                  <span :class="[
                    'px-4 py-1.5 rounded-full text-sm font-bold tracking-wide',
                    bestMatch.clasificacion === 'APTO'        ? 'bg-emi-gold-400 text-emi-navy-900' :
                    bestMatch.clasificacion === 'CONSIDERADO' ? 'bg-info-500 text-white' :
                                                                'bg-danger-500 text-white'
                  ]">{{ bestMatch.clasificacion }}</span>
                  <span class="text-sm opacity-70">Compatibilidad general</span>
                </div>

                <p class="text-sm opacity-75 mb-5 leading-relaxed">
                  {{ scoreExplanation }}
                </p>

                <!-- Barras por dimensión -->
                <div class="space-y-2">
                  <div v-for="[key, label, val] in dimensionRows" :key="key"
                    class="grid grid-cols-[1fr_auto_3rem] items-center gap-3">
                    <div class="bg-white/15 rounded-full h-2 overflow-hidden">
                      <div class="h-2 rounded-full transition-all duration-700"
                        :class="val >= 0.7 ? 'bg-emi-gold-400' : val >= 0.4 ? 'bg-info-500' : 'bg-danger-500'"
                        :style="{ width: (val * 100) + '%' }"
                      ></div>
                    </div>
                    <span class="text-xs opacity-60 text-right w-28 truncate">{{ label }}</span>
                    <span class="text-xs font-bold text-right">{{ Math.round(val * 100) }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- ¿Por qué esta oferta? -->
          <div class="card-emi">
            <div class="flex items-center gap-3 mb-5">
              <div class="w-9 h-9 bg-emi-gold-100 rounded-xl flex items-center justify-center shrink-0">
                <svg class="w-5 h-5 text-emi-gold-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <div>
                <h2 class="text-base font-semibold text-emi-navy-800">¿Por qué el sistema eligió esta oferta?</h2>
                <p class="text-xs text-gray-400 mt-0.5">Análisis personalizado basado en tu CV</p>
              </div>
            </div>

            <!-- Intro -->
            <p class="text-sm text-gray-600 leading-relaxed mb-5 p-4 bg-gray-50 rounded-xl border-l-4 border-emi-navy-300">
              El motor de recomendación evaluó tu perfil contra <strong>{{ totalCount }} ofertas activas</strong> disponibles
              para {{ userRole === 'estudiante' ? 'estudiantes' : 'titulados' }}.
              Esta oferta obtuvo el puntaje más alto de compatibilidad con un
              <strong>{{ Math.round(bestMatch.match_score * 100) }}%</strong> de coincidencia global,
              calculado ponderando tus habilidades técnicas, habilidades blandas, formación académica, experiencia e idiomas.
            </p>

            <!-- Fortalezas / Oportunidades en 2 columnas -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-5">
              <!-- Fortalezas -->
              <div class="bg-success-50 rounded-xl p-4 border border-success-100">
                <h3 class="text-xs font-bold text-success-700 uppercase tracking-wide mb-3 flex items-center gap-1.5">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Tus fortalezas para esta oferta
                </h3>
                <ul class="space-y-2">
                  <li v-if="hardSkillsScore >= 0.5" class="flex items-start gap-2 text-sm text-success-700">
                    <span class="mt-1 w-1.5 h-1.5 rounded-full bg-success-500 shrink-0"></span>
                    Habilidades técnicas: <strong>{{ Math.round(hardSkillsScore * 100) }}%</strong> de cobertura
                  </li>
                  <li v-if="softSkillsScore >= 0.5" class="flex items-start gap-2 text-sm text-success-700">
                    <span class="mt-1 w-1.5 h-1.5 rounded-full bg-success-500 shrink-0"></span>
                    Habilidades blandas: <strong>{{ Math.round(softSkillsScore * 100) }}%</strong> de cobertura
                  </li>
                  <li v-if="educationScore >= 0.5" class="flex items-start gap-2 text-sm text-success-700">
                    <span class="mt-1 w-1.5 h-1.5 rounded-full bg-success-500 shrink-0"></span>
                    Formación académica valorada con <strong>{{ Math.round(educationScore * 100) }}%</strong>
                  </li>
                  <li v-if="matchedSkillsCount > 0" class="flex items-start gap-2 text-sm text-success-700">
                    <span class="mt-1 w-1.5 h-1.5 rounded-full bg-success-500 shrink-0"></span>
                    Tienes <strong>{{ matchedSkillsCount }} habilidades</strong> requeridas
                  </li>
                  <li v-if="matchedLanguagesCount > 0" class="flex items-start gap-2 text-sm text-success-700">
                    <span class="mt-1 w-1.5 h-1.5 rounded-full bg-success-500 shrink-0"></span>
                    Cumples con <strong>{{ matchedLanguagesCount }} idioma(s)</strong> solicitados
                  </li>
                  <li v-if="noStrengths" class="text-sm text-success-600 italic">
                    Aún no se identificaron fortalezas destacadas.
                  </li>
                </ul>
              </div>

              <!-- Oportunidades de mejora -->
              <div class="bg-warning-50 rounded-xl p-4 border border-warning-100">
                <h3 class="text-xs font-bold text-warning-700 uppercase tracking-wide mb-3 flex items-center gap-1.5">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                  </svg>
                  Áreas a mejorar
                </h3>
                <ul class="space-y-2">
                  <li v-if="missingSkillsCount > 0" class="flex items-start gap-2 text-sm text-warning-700">
                    <span class="mt-1 w-1.5 h-1.5 rounded-full bg-warning-500 shrink-0"></span>
                    <strong>{{ missingSkillsCount }} habilidades</strong> técnicas por adquirir
                  </li>
                  <li v-if="hardSkillsScore < 0.5" class="flex items-start gap-2 text-sm text-warning-700">
                    <span class="mt-1 w-1.5 h-1.5 rounded-full bg-warning-500 shrink-0"></span>
                    Reforzar habilidades técnicas aumentaría tu puntuación significativamente
                  </li>
                  <li v-if="languagesScore < 0.5 && languagesScore >= 0" class="flex items-start gap-2 text-sm text-warning-700">
                    <span class="mt-1 w-1.5 h-1.5 rounded-full bg-warning-500 shrink-0"></span>
                    Mejorar tus idiomas puede elevar tu compatibilidad
                  </li>
                  <li v-if="experienceScore < 0.4" class="flex items-start gap-2 text-sm text-warning-700">
                    <span class="mt-1 w-1.5 h-1.5 rounded-full bg-warning-500 shrink-0"></span>
                    La oferta requiere más experiencia que la registrada en tu perfil
                  </li>
                  <li v-if="noImprovements" class="text-sm text-warning-600 italic">
                    No se detectaron brechas significativas. ¡Excelente perfil!
                  </li>
                </ul>
              </div>
            </div>

            <!-- Habilidades matched como chips -->
            <div v-if="matchedSkillsList.length > 0">
              <p class="text-xs text-emi-navy-400 uppercase tracking-wide font-semibold mb-2">Habilidades que ya tienes</p>
              <div class="flex flex-wrap gap-1.5">
                <span v-for="skill in matchedSkillsList" :key="skill"
                  class="px-2.5 py-1 bg-success-100 text-success-700 rounded-full text-xs font-medium">
                  ✓ {{ skill }}
                </span>
              </div>
            </div>

            <div v-if="missingSkillsList.length > 0" class="mt-3">
              <p class="text-xs text-emi-navy-400 uppercase tracking-wide font-semibold mb-2">Habilidades por desarrollar</p>
              <div class="flex flex-wrap gap-1.5">
                <span v-for="skill in missingSkillsList" :key="skill"
                  class="px-2.5 py-1 bg-warning-100 text-warning-700 rounded-full text-xs font-medium">
                  + {{ skill }}
                </span>
              </div>
            </div>
          </div>

          <!-- Análisis de compatibilidad -->
          <div class="card-emi">
            <div class="flex items-center gap-2 mb-4">
              <div class="flex-1 h-px bg-gray-200"></div>
              <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider px-2">
                Análisis de Compatibilidad
              </span>
              <div class="flex-1 h-px bg-gray-200"></div>
            </div>

            <div v-if="bestMatch.scores_detalle" class="mb-4">
              <h4 class="font-semibold text-gray-900 mb-3">Detalle de Scores</h4>
              <div class="space-y-3">
                <div v-for="(value, key) in bestMatch.scores_detalle" :key="key">
                  <ProgressBar :value="value * 100" :label="formatScoreLabel(key)" />
                </div>
              </div>
            </div>

            <MatchDetailSection
              v-if="bestMatch.match_details"
              :matchDetails="bestMatch.match_details"
              :clasificacion="bestMatch.clasificacion"
            />
          </div>

          <!-- Descripción de la oferta -->
          <div v-if="bestMatch.oferta?.descripcion" class="card-emi">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-9 h-9 bg-emi-navy-100 rounded-xl flex items-center justify-center shrink-0">
                <svg class="w-5 h-5 text-emi-navy-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h2 class="text-base font-semibold text-emi-navy-800">Descripción de la oferta</h2>
            </div>
            <p class="text-sm text-gray-600 leading-relaxed whitespace-pre-line">{{ bestMatch.oferta.descripcion }}</p>
          </div>


        </div>
        <!-- fin columna izquierda -->

        <!-- ════════════════════════════════
             COLUMNA DERECHA — sticky
        ════════════════════════════════ -->
        <div class="space-y-4 lg:sticky lg:top-6 lg:self-start">

          <!-- Card de acción principal -->
          <div class="card-emi !p-0 overflow-hidden">
            <!-- Banner superior -->
            <div class="h-2 w-full" :class="
              bestMatch.clasificacion === 'APTO'        ? 'bg-gradient-to-r from-emi-gold-400 to-emi-gold-500' :
              bestMatch.clasificacion === 'CONSIDERADO' ? 'bg-gradient-to-r from-info-500 to-info-600' :
                                                          'bg-gradient-to-r from-danger-500 to-danger-600'
            "></div>

            <div class="p-5">
              <!-- Clasificación badge + score mini -->
              <div class="flex items-center justify-between mb-4">
                <span :class="[
                  'badge-emi',
                  bestMatch.clasificacion === 'APTO'        ? 'badge-gold' :
                  bestMatch.clasificacion === 'CONSIDERADO' ? 'bg-info-100 text-info-700' :
                                                              'bg-danger-100 text-danger-700'
                ]">{{ bestMatch.clasificacion }}</span>
                <span class="text-2xl font-extrabold text-emi-navy-700">
                  {{ Math.round(bestMatch.match_score * 100) }}%
                </span>
              </div>

              <!-- Nombre oferta (truncado) -->
              <h3 class="font-semibold text-emi-navy-800 text-sm leading-snug mb-1 line-clamp-2">
                {{ bestMatch.oferta?.titulo }}
              </h3>
              <p class="text-xs text-gray-400 mb-4">{{ bestMatch.oferta?.institution_name }}</p>

              <!-- Info rápida -->
              <div class="space-y-2 mb-5">
                <div v-if="bestMatch.oferta?.tipo" class="flex items-center gap-2 text-sm text-gray-600">
                  <svg class="w-4 h-4 text-gray-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                  </svg>
                  <span class="capitalize">{{ bestMatch.oferta.tipo }}</span>
                </div>
                <div v-if="bestMatch.oferta?.modalidad" class="flex items-center gap-2 text-sm text-gray-600">
                  <svg class="w-4 h-4 text-gray-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
                  </svg>
                  <span class="capitalize">{{ bestMatch.oferta.modalidad }}</span>
                </div>
                <div v-if="bestMatch.oferta?.ubicacion" class="flex items-center gap-2 text-sm text-gray-600">
                  <svg class="w-4 h-4 text-gray-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  <span>{{ bestMatch.oferta.ubicacion }}</span>
                </div>
                <div v-if="bestMatch.oferta?.fecha_cierre" class="flex items-center gap-2 text-sm text-gray-600">
                  <svg class="w-4 h-4 text-gray-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                  </svg>
                  <span>Cierre: {{ formatDate(bestMatch.oferta.fecha_cierre) }}</span>
                </div>
                <div v-if="bestMatch.oferta?.cupos_disponibles" class="flex items-center gap-2 text-sm text-gray-600">
                  <svg class="w-4 h-4 text-gray-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  <span>{{ bestMatch.oferta.cupos_disponibles }} cupo(s) disponible(s)</span>
                </div>
              </div>

              <!-- Resultado de postulación -->
              <div v-if="postResult" class="mb-4 p-3 rounded-xl border" :class="
                postResult.clasificacion === 'APTO'        ? 'bg-success-50 border-success-100' :
                postResult.clasificacion === 'CONSIDERADO' ? 'bg-info-50 border-info-100' :
                                                             'bg-danger-50 border-danger-100'
              ">
                <p class="text-xs font-bold mb-1" :class="
                  postResult.clasificacion === 'APTO'        ? 'text-success-700' :
                  postResult.clasificacion === 'CONSIDERADO' ? 'text-info-700' : 'text-danger-700'
                ">¡Postulación enviada!</p>
                <p class="text-xs text-gray-600">
                  Resultado: <strong>{{ postResult.clasificacion }}</strong> con
                  <strong>{{ Math.round((postResult.match_score || 0) * 100) }}%</strong> de compatibilidad.
                </p>
                <p class="text-xs text-gray-400 mt-1">
                  Puedes ver el detalle en tu historial de postulaciones.
                </p>
              </div>

              <!-- Error postulación -->
              <div v-if="postError" class="mb-4 p-3 bg-danger-50 border border-danger-100 rounded-xl">
                <p class="text-xs text-danger-700 whitespace-pre-line">{{ postError }}</p>
              </div>

              <!-- Botón de postulación -->
              <button
                v-if="!postResult"
                @click="postular"
                :disabled="postulando"
                class="w-full py-3 flex items-center justify-center gap-2"
                :class="postulando
                  ? 'btn-emi-primary opacity-50 cursor-not-allowed'
                  : 'btn-emi-secondary'"
              >
                <svg v-if="postulando" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                </svg>
                <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
                </svg>
                {{ postulando ? 'Procesando postulación...' : 'Postularse a esta oferta' }}
              </button>

              <!-- Ya postulado -->
              <div v-else class="w-full py-3 rounded-xl bg-success-100 text-success-700 font-semibold text-sm text-center flex items-center justify-center gap-2">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                Postulación enviada
              </div>

              <p class="text-xs text-gray-400 text-center mt-3 leading-relaxed">
                Al postularte, el sistema evaluará tu CV en tiempo real contra los requisitos de esta oferta.
              </p>
            </div>
          </div>

          <!-- Ver más opciones -->
          <div class="card-emi text-center">
            <p class="text-sm text-gray-500 mb-3">
              ¿Quieres comparar con todas las opciones disponibles?
            </p>
            <router-link to="/correspondencia-perfiles"
              class="btn-emi-primary inline-flex items-center justify-center gap-2 w-full">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
              </svg>
              Ver más opciones de ofertas
            </router-link>
            <button @click="loadRecommendations(true)" :disabled="refreshing"
              class="mt-2 w-full flex items-center justify-center gap-2 px-4 py-2 rounded-lg text-sm text-emi-navy-500 hover:text-emi-navy-700 hover:bg-emi-navy-50 transition-colors disabled:opacity-50">
              <svg :class="['w-3.5 h-3.5', refreshing && 'animate-spin']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              {{ refreshing ? 'Recalculando...' : 'Recalcular recomendación' }}
            </button>
          </div>

        </div>
        <!-- fin columna derecha -->

      </div>
    </div>

  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import AppLayout from '@/shared/components/AppLayout.vue'
import ProgressBar from '@/shared/components/ui/ProgressBar.vue'
import EligibilityWarning from '../components/EligibilityWarning.vue'
import MatchDetailSection from '../components/MatchDetailSection.vue'
import { useRecommendations } from '../composables/useRecommendations'
import { postularDesdeRecomendacion } from '../api/postulaciones.api'
import { formatApiError } from '@/shared/utils/apiError'

// ── Fases del texto de carga ──────────────────────────────
const PHASES = [
  'Analizando tu perfil...',
  'Calculando compatibilidades...',
  'Encontrando tu mejor oportunidad...',
]
const phaseIndex = ref(0)
const loadingPhase = computed(() => PHASES[phaseIndex.value])
let phaseTimer = null

const {
  recommendations,
  loading,
  refreshing,
  error,
  isEligible,
  eligibilityReason,
  eligibilityAction,
  missingFields,
  userRole,
  bestMatch,
  formatScoreLabel,
  formatDate,
  loadRecommendations
} = useRecommendations()

onMounted(() => {
  phaseTimer = setInterval(() => {
    phaseIndex.value = (phaseIndex.value + 1) % PHASES.length
  }, 1400)
})
onUnmounted(() => clearInterval(phaseTimer))

// ── Total de ofertas evaluadas ───────────────────────────
const totalCount = computed(() => recommendations.value.length)

// ── Postulación ──────────────────────────────────────────
const postulando = ref(false)
const postResult = ref(null)
const postError  = ref(null)

const postular = async () => {
  if (!bestMatch.value?.oferta?.id) return
  postulando.value = true
  postError.value = null
  try {
    const result = await postularDesdeRecomendacion(bestMatch.value.oferta.id)
    postResult.value = result
  } catch (e) {
    postError.value = formatApiError(e, 'Error al procesar la postulación')
  } finally {
    postulando.value = false
  }
}

// ── Color del aro ─────────────────────────────────────────
const scoreRingColor = computed(() => {
  const s = bestMatch.value?.match_score ?? 0
  if (s >= 0.7) return '#F59E0B'
  if (s >= 0.4) return '#38BDF8'
  return '#F87171'
})

// ── Filas de dimensiones ─────────────────────────────────
const dimensionRows = computed(() => {
  const s = bestMatch.value?.scores_detalle || {}
  return [
    ['hard_skills_score', 'Habs. Técnicas',  s.hard_skills_score  ?? 0],
    ['soft_skills_score', 'Habs. Blandas',   s.soft_skills_score  ?? 0],
    ['education_score',   'Formación',        s.education_score    ?? 0],
    ['experience_score',  'Experiencia',      s.experience_score   ?? 0],
    ['languages_score',   'Idiomas',          s.languages_score    ?? 0],
  ]
})

// ── Scores individuales ───────────────────────────────────
const hardSkillsScore  = computed(() => bestMatch.value?.scores_detalle?.hard_skills_score  ?? 0)
const softSkillsScore  = computed(() => bestMatch.value?.scores_detalle?.soft_skills_score  ?? 0)
const educationScore   = computed(() => bestMatch.value?.scores_detalle?.education_score    ?? 0)
const experienceScore  = computed(() => bestMatch.value?.scores_detalle?.experience_score   ?? 0)
const languagesScore   = computed(() => bestMatch.value?.scores_detalle?.languages_score    ?? 0)

// ── Explicación textual del score ─────────────────────────
const scoreExplanation = computed(() => {
  const s = bestMatch.value?.match_score ?? 0
  if (s >= 0.85) return 'Excelente compatibilidad. Tu perfil encaja casi perfectamente con lo que busca esta oferta.'
  if (s >= 0.7)  return 'Muy buena compatibilidad. Cumples con los criterios más importantes de esta oferta.'
  if (s >= 0.55) return 'Compatibilidad moderada-alta. Tienes un buen perfil base con algunas áreas por fortalecer.'
  if (s >= 0.4)  return 'Compatibilidad moderada. Estás considerado, aunque reforzar ciertas áreas te haría más competitivo.'
  return 'Compatibilidad baja. Aun así, es la mejor oferta disponible para tu perfil actual.'
})

// ── Skills ───────────────────────────────────────────────
const matchedSkillsList = computed(() => {
  const md = bestMatch.value?.match_details
  if (!md) return []
  return [
    ...(md.hard_skills?.matched || []),
    ...(md.soft_skills?.matched || []),
  ].slice(0, 12)
})

const missingSkillsList = computed(() => {
  const md = bestMatch.value?.match_details
  if (!md) return []
  return [
    ...(md.hard_skills?.missing || []),
    ...(md.soft_skills?.missing || []),
  ].slice(0, 8)
})

const matchedSkillsCount = computed(() => {
  const md = bestMatch.value?.match_details
  if (!md) return 0
  return (md.hard_skills?.matched?.length ?? 0) + (md.soft_skills?.matched?.length ?? 0)
})

const missingSkillsCount = computed(() => {
  const md = bestMatch.value?.match_details
  if (!md) return 0
  return (md.hard_skills?.missing?.length ?? 0) + (md.soft_skills?.missing?.length ?? 0)
})

const matchedLanguagesCount = computed(() => {
  return bestMatch.value?.match_details?.languages?.matched?.length ?? 0
})

// ── Helpers fortalezas/mejoras ────────────────────────────
const noStrengths = computed(() =>
  hardSkillsScore.value < 0.5 && softSkillsScore.value < 0.5 &&
  educationScore.value < 0.5 && matchedSkillsCount.value === 0
)
const noImprovements = computed(() =>
  missingSkillsCount.value === 0 && hardSkillsScore.value >= 0.5 &&
  languagesScore.value >= 0.5 && experienceScore.value >= 0.4
)
</script>
