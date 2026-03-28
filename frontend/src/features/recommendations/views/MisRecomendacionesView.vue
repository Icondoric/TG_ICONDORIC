<template>
  <AppLayout>

    <!-- ══════════════════════════════════════════════════════
         CARGANDO
    ══════════════════════════════════════════════════════ -->
    <div v-if="loading" class="min-h-[80vh] flex flex-col items-center justify-center select-none px-4">
      <div class="relative w-44 h-44 mb-10">
        <div class="absolute inset-0  rounded-full bg-emi-navy-100 animate-ping opacity-20" style="animation-duration:2.2s"></div>
        <div class="absolute inset-6  rounded-full bg-emi-navy-200 animate-ping opacity-30" style="animation-duration:2.2s;animation-delay:.45s"></div>
        <div class="absolute inset-12 rounded-full bg-emi-navy-300 animate-ping opacity-40" style="animation-duration:2.2s;animation-delay:.9s"></div>
        <div class="absolute inset-0 flex items-center justify-center">
          <div class="w-20 h-20 bg-gradient-to-br from-emi-navy-600 to-emi-navy-800 rounded-full flex items-center justify-center shadow-2xl">
            <svg class="w-9 h-9 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
          </div>
        </div>
      </div>
      <h2 class="text-2xl sm:text-3xl font-bold text-emi-navy-700 text-center mb-3">{{ loadingPhase }}</h2>
      <p class="text-gray-400 text-sm text-center max-w-sm leading-relaxed">
        Nuestro sistema analiza tu perfil completo y lo compara con cada oferta disponible para determinar en cuáles eres apto o considerado.
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
         CONTENIDO PRINCIPAL
    ══════════════════════════════════════════════════════ -->
    <div v-else class="px-4 sm:px-6 lg:px-10 xl:px-16 py-8 max-w-screen-xl mx-auto">

      <!-- Encabezado de página -->
      <div class="mb-8 flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold text-emi-navy-500">Lista de Perfiles Calificados</h1>
          <p class="mt-2 text-gray-500">
            Ofertas en las que eres apto o considerado
            <span v-if="totalEvaluadas > 0">
              , evaluadas entre <strong class="text-emi-navy-600">{{ totalEvaluadas }}</strong> ofertas activas
            </span>
          </p>
          <div class="flex items-center gap-2 mt-3 flex-wrap">
            <span class="badge-emi badge-gold">APTO: {{ aptoCount }}</span>
            <span class="px-2.5 py-1 rounded-full text-xs font-semibold bg-info-100 text-info-700">CONSIDERADO: {{ consideradoCount }}</span>
            <span v-if="noAptoCount > 0" class="px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-400">
              {{ noAptoCount }} oferta(s) sin calificación suficiente
            </span>
          </div>
        </div>
        <button
          @click="loadRecommendations(true)"
          :disabled="refreshing"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium text-emi-navy-600 border border-emi-navy-200 hover:bg-emi-navy-50 transition-colors disabled:opacity-50 shrink-0 self-start"
        >
          <svg :class="['w-4 h-4', refreshing && 'animate-spin']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          {{ refreshing ? 'Recalculando...' : 'Recalcular' }}
        </button>
      </div>

      <!-- ══ SIN OFERTAS CALIFICADAS ══ -->
      <div v-if="qualifiedRecommendations.length === 0" class="max-w-lg mx-auto py-20 text-center">
        <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-700 mb-2">No calificaste en ninguna oferta activa</h3>
        <p class="text-gray-500 text-sm mb-8 max-w-sm mx-auto">
          Tu perfil fue evaluado contra {{ totalEvaluadas }} oferta(s), pero no alcanzaste el umbral de APTO o CONSIDERADO en ninguna. Completa o mejora tu perfil para aumentar tus posibilidades.
        </p>
        <div class="flex justify-center gap-3 flex-wrap">
          <router-link to="/digitalizacion/mi-perfil"
            class="px-5 py-2.5 border border-emi-navy-300 text-emi-navy-600 rounded-lg hover:bg-emi-navy-50 transition-colors font-medium text-sm">
            Revisar Mi Perfil
          </router-link>
          <button @click="loadRecommendations(true)" class="btn-emi-primary text-sm">Recalcular</button>
        </div>
      </div>

      <!-- ══ LISTA DE OFERTAS CALIFICADAS ══ -->
      <div v-else class="space-y-5">
        <div
          v-for="rec in qualifiedRecommendations"
          :key="rec.oferta_id"
          class="card-emi !p-0 overflow-hidden"
        >
          <!-- Franja superior -->
          <div class="h-1 w-full" :class="
            rec.clasificacion === 'APTO'
              ? 'bg-gradient-to-r from-emi-gold-400 to-emi-gold-500'
              : 'bg-gradient-to-r from-info-400 to-info-500'
          "></div>

          <div class="p-5">

            <!-- ── Cabecera de la tarjeta ── -->
            <div class="flex items-start gap-4">

              <!-- Score -->
              <div class="shrink-0 text-center min-w-[56px]">
                <div class="text-3xl font-black leading-none"
                  :class="rec.clasificacion === 'APTO' ? 'text-emi-gold-600' : 'text-info-700'">
                  {{ Math.round(rec.match_score * 100) }}%
                </div>
                <div class="text-[10px] text-gray-400 mt-1 font-medium leading-tight">compatibilidad</div>
              </div>

              <!-- Info básica -->
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 flex-wrap mb-1.5">
                  <span :class="['badge-emi text-xs', rec.clasificacion === 'APTO' ? 'badge-gold' : 'bg-info-100 text-info-700']">
                    {{ rec.clasificacion }}
                  </span>
                  <span v-if="rec.oferta?.tipo" :class="[
                    'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium',
                    rec.oferta.tipo === 'pasantia' ? 'bg-purple-100 text-purple-700' : 'bg-emi-navy-100 text-emi-navy-700'
                  ]">
                    {{ rec.oferta.tipo === 'pasantia' ? 'Pasantía' : 'Empleo' }}
                  </span>
                  <span v-if="rec.oferta?.modalidad"
                    class="inline-flex items-center px-2 py-0.5 rounded-full text-xs bg-gray-100 text-gray-500">
                    {{ rec.oferta.modalidad }}
                  </span>
                </div>
                <h3 class="text-base font-semibold text-emi-navy-800 leading-snug">{{ rec.oferta?.titulo }}</h3>
                <p class="text-sm text-gray-500 mt-0.5">
                  {{ rec.oferta?.institution_name }}
                  <span v-if="rec.oferta?.sector" class="text-gray-400"> · {{ rec.oferta.sector }}</span>
                </p>
                <div class="mt-2 flex flex-wrap gap-3 text-xs text-gray-400">
                  <span v-if="rec.oferta?.ubicacion" class="flex items-center gap-1">
                    <svg class="h-3.5 w-3.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                    </svg>
                    {{ rec.oferta.ubicacion }}
                  </span>
                  <span v-if="rec.oferta?.cupos_disponibles" class="flex items-center gap-1">
                    <svg class="h-3.5 w-3.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
                    </svg>
                    {{ rec.oferta.cupos_disponibles }} cupo(s)
                  </span>
                  <span v-if="rec.oferta?.fecha_cierre" class="flex items-center gap-1">
                    <svg class="h-3.5 w-3.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                    </svg>
                    Cierra {{ formatDate(rec.oferta.fecha_cierre) }}
                  </span>
                </div>
              </div>

              <!-- ── Mini estadísticas (derecha) ── -->
              <div v-if="rec.scores_detalle" class="hidden sm:flex flex-col justify-center gap-2 shrink-0 w-44 border-l border-gray-100 pl-4">
                <template v-for="dim in [
                  { label: 'Habilidades Técnicas', val: rec.scores_detalle.hard_skills_score  ?? 0 },
                  { label: 'Habilidades Blandas',  val: rec.scores_detalle.soft_skills_score  ?? 0 },
                  { label: 'Formación Académica',  val: rec.scores_detalle.education_score    ?? 0 },
                  { label: 'Experiencia',          val: rec.scores_detalle.experience_score   ?? 0 },
                  { label: 'Idiomas',              val: rec.scores_detalle.languages_score    ?? 0 },
                ]" :key="dim.label">
                  <div>
                    <div class="flex justify-between items-center mb-1">
                      <span class="text-[10px] text-gray-500 leading-none">{{ dim.label }}</span>
                      <span class="text-[10px] font-bold leading-none"
                        :class="dim.val >= 0.7 ? 'text-success-600' : dim.val >= 0.4 ? 'text-warning-600' : 'text-danger-500'">
                        {{ Math.round(dim.val * 100) }}%
                      </span>
                    </div>
                    <div class="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
                      <div class="h-full rounded-full transition-all duration-700"
                        :class="dim.val >= 0.7 ? 'bg-success-500' : dim.val >= 0.4 ? 'bg-warning-500' : 'bg-danger-500'"
                        :style="{ width: Math.round(dim.val * 100) + '%' }"/>
                    </div>
                  </div>
                </template>
              </div>
            </div>

            <!-- Skills coincidentes (preview, solo cuando está colapsado) -->
            <div v-if="expandedId !== rec.oferta_id && getMatchedSkills(rec).length > 0" class="mt-3 pl-20">
              <div class="flex flex-wrap gap-1.5">
                <span v-for="skill in getMatchedSkills(rec).slice(0, 5)" :key="skill"
                  class="inline-flex items-center gap-0.5 px-2 py-0.5 rounded-full text-xs font-medium bg-success-100 text-success-700">
                  <svg class="h-2.5 w-2.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
                  </svg>
                  {{ skill }}
                </span>
                <span v-if="getMatchedSkills(rec).length > 5"
                  class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-success-50 text-success-600">
                  +{{ getMatchedSkills(rec).length - 5 }} más
                </span>
              </div>
            </div>

            <!-- ── Controles ── -->
            <div class="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between gap-3 flex-wrap">
              <button
                @click="toggleExpand(rec.oferta_id)"
                class="inline-flex items-center gap-1 text-sm font-medium text-emi-navy-500 hover:text-emi-navy-700 transition-colors"
              >
                <svg :class="['h-4 w-4 transition-transform duration-200', expandedId === rec.oferta_id ? 'rotate-180' : '']"
                  fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
                {{ expandedId === rec.oferta_id ? 'Ocultar análisis' : 'Ver análisis completo' }}
              </button>

              <!-- Postulación ya enviada -->
              <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-success-100 text-success-700 text-sm font-medium"
                v-if="postResults[rec.oferta_id]">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                Postulación enviada
              </div>

              <!-- No cumple requisitos de carrera/semestre -->
              <template v-else-if="!getOfferEligibility(rec).eligible">
                <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-lg text-sm font-semibold bg-warning-50 text-warning-700 border border-warning-200 cursor-not-allowed">
                  <svg class="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                  </svg>
                  No habilitado
                </div>
              </template>

              <!-- Botón normal de postulación -->
              <button v-else
                @click="postular(rec)"
                :disabled="postulando === rec.oferta_id"
                class="inline-flex items-center gap-2 px-4 py-1.5 rounded-lg text-sm font-semibold transition-all"
                :class="postulando === rec.oferta_id ? 'bg-emi-navy-300 text-white cursor-not-allowed' : 'btn-emi-secondary'"
              >
                <svg v-if="postulando === rec.oferta_id" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                </svg>
                <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
                </svg>
                {{ postulando === rec.oferta_id ? 'Procesando...' : 'Postularme' }}
              </button>
            </div>

            <!-- Razón de bloqueo por elegibilidad -->
            <div v-if="!postResults[rec.oferta_id] && !getOfferEligibility(rec).eligible"
              class="mt-2 px-3 py-2 bg-warning-50 border border-warning-200 rounded-lg flex items-start gap-2">
              <svg class="w-4 h-4 text-warning-600 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <p class="text-xs text-warning-700">{{ getOfferEligibility(rec).reason }}</p>
            </div>

            <!-- Error al postular -->
            <div v-if="postErrors[rec.oferta_id]" class="mt-2 px-3 py-2 bg-danger-50 border border-danger-200 rounded-lg">
              <p class="text-xs text-danger-700">{{ postErrors[rec.oferta_id] }}</p>
            </div>

            <!-- ════════════════════════════════════════════════════
                 PANEL EXPANDIBLE
            ════════════════════════════════════════════════════ -->
            <div v-show="expandedId === rec.oferta_id" class="mt-6 space-y-8">

              <!-- ──────────────────────────────────────────────
                   1. DETALLE DE LA OFERTA
              ────────────────────────────────────────────── -->
              <section>
                <!-- Encabezado de sección -->
                <div class="flex items-center gap-2 mb-4">
                  <div class="w-7 h-7 bg-emi-navy-100 rounded-lg flex items-center justify-center shrink-0">
                    <svg class="w-4 h-4 text-emi-navy-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                    </svg>
                  </div>
                  <h4 class="text-sm font-bold text-emi-navy-800 uppercase tracking-wide">Detalle de la Oferta</h4>
                </div>

                <!-- Descripción -->
                <p v-if="rec.oferta?.descripcion" class="text-sm text-gray-600 leading-relaxed mb-4 p-4 bg-gray-50 rounded-xl border-l-4 border-emi-navy-200">
                  {{ rec.oferta.descripcion }}
                </p>

                <!-- Grid: datos básicos + requisitos formales -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">

                  <!-- Datos generales -->
                  <div class="bg-gray-50 rounded-xl p-4">
                    <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Información general</p>
                    <dl class="space-y-2">
                      <div v-if="rec.oferta?.tipo" class="flex gap-2">
                        <dt class="text-xs text-gray-400 w-20 shrink-0">Tipo</dt>
                        <dd class="text-xs text-gray-700 font-medium capitalize">{{ rec.oferta.tipo }}</dd>
                      </div>
                      <div v-if="rec.oferta?.modalidad" class="flex gap-2">
                        <dt class="text-xs text-gray-400 w-20 shrink-0">Modalidad</dt>
                        <dd class="text-xs text-gray-700 capitalize">{{ rec.oferta.modalidad }}</dd>
                      </div>
                      <div v-if="rec.oferta?.ubicacion" class="flex gap-2">
                        <dt class="text-xs text-gray-400 w-20 shrink-0">Ubicación</dt>
                        <dd class="text-xs text-gray-700">{{ rec.oferta.ubicacion }}</dd>
                      </div>
                      <div v-if="rec.oferta?.cupos_disponibles" class="flex gap-2">
                        <dt class="text-xs text-gray-400 w-20 shrink-0">Cupos</dt>
                        <dd class="text-xs text-gray-700">{{ rec.oferta.cupos_disponibles }}</dd>
                      </div>
                      <div v-if="rec.oferta?.fecha_inicio" class="flex gap-2">
                        <dt class="text-xs text-gray-400 w-20 shrink-0">Inicio</dt>
                        <dd class="text-xs text-gray-700">{{ formatDate(rec.oferta.fecha_inicio) }}</dd>
                      </div>
                      <div v-if="rec.oferta?.fecha_cierre" class="flex gap-2">
                        <dt class="text-xs text-gray-400 w-20 shrink-0">Cierre</dt>
                        <dd class="text-xs text-gray-700 font-semibold text-emi-navy-600">{{ formatDate(rec.oferta.fecha_cierre) }}</dd>
                      </div>
                    </dl>
                  </div>

                  <!-- Requisitos formales -->
                  <div class="bg-gray-50 rounded-xl p-4">
                    <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Requisitos formales</p>
                    <dl class="space-y-2">
                      <div v-if="rec.match_details?.education?.required_level" class="flex gap-2">
                        <dt class="text-xs text-gray-400 w-24 shrink-0">Formación</dt>
                        <dd class="text-xs text-gray-700">{{ rec.match_details.education.required_level }}</dd>
                      </div>
                      <div v-if="rec.match_details?.experience?.required_years != null" class="flex gap-2">
                        <dt class="text-xs text-gray-400 w-24 shrink-0">Experiencia</dt>
                        <dd class="text-xs text-gray-700">
                          {{ rec.match_details.experience.required_years > 0
                            ? `≥ ${rec.match_details.experience.required_years} año(s)`
                            : 'Sin requisito mínimo' }}
                        </dd>
                      </div>
                      <div v-if="getRequiredSkillsCount(rec) > 0" class="flex gap-2">
                        <dt class="text-xs text-gray-400 w-24 shrink-0">Habilidades</dt>
                        <dd class="text-xs text-gray-700">{{ getRequiredSkillsCount(rec) }} habilidades requeridas</dd>
                      </div>
                      <div v-if="getRequiredLangsCount(rec) > 0" class="flex gap-2">
                        <dt class="text-xs text-gray-400 w-24 shrink-0">Idiomas</dt>
                        <dd class="text-xs text-gray-700">{{ getAllRequiredLangs(rec).join(', ') }}</dd>
                      </div>
                    </dl>
                  </div>
                </div>
              </section>

              <!-- ──────────────────────────────────────────────
                   2. ANÁLISIS DE COMPATIBILIDAD
              ────────────────────────────────────────────── -->
              <section>
                <div class="flex items-center gap-2 mb-4">
                  <div class="w-7 h-7 bg-emi-navy-100 rounded-lg flex items-center justify-center shrink-0">
                    <svg class="w-4 h-4 text-emi-navy-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                    </svg>
                  </div>
                  <h4 class="text-sm font-bold text-emi-navy-800 uppercase tracking-wide">Análisis de Compatibilidad</h4>
                </div>

                <div class="space-y-2.5">

                  <!-- ── Habilidades Técnicas ── -->
                  <div class="border border-gray-200 rounded-xl overflow-hidden">
                    <div class="px-4 py-3 bg-gray-50 flex items-center gap-3">
                      <svg class="w-4 h-4 text-emi-navy-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/>
                      </svg>
                      <div class="flex-1 min-w-0">
                        <div class="flex justify-between items-center mb-1.5">
                          <span class="text-sm font-semibold text-gray-800">Habilidades Técnicas</span>
                          <span class="text-xs font-bold" :class="scoreColorText(rec.scores_detalle?.hard_skills_score ?? 0)">
                            {{ Math.round((rec.scores_detalle?.hard_skills_score ?? 0) * 100) }}%
                          </span>
                        </div>
                        <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div class="h-full rounded-full transition-all duration-700"
                            :class="scoreColorBg(rec.scores_detalle?.hard_skills_score ?? 0)"
                            :style="{ width: Math.round((rec.scores_detalle?.hard_skills_score ?? 0) * 100) + '%' }"/>
                        </div>
                      </div>
                    </div>
                    <div v-if="getHardSkillsTotal(rec) > 0" class="grid grid-cols-2 divide-x divide-gray-100 border-t border-gray-100">
                      <div class="px-4 py-3">
                        <p class="text-xs font-medium text-gray-400 mb-2">Requeridas por la oferta</p>
                        <div class="flex flex-wrap gap-1">
                          <span v-for="s in [...(rec.match_details?.hard_skills?.matched||[]), ...(rec.match_details?.hard_skills?.missing||[])]"
                            :key="'rh-'+s" class="px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">{{ s }}</span>
                        </div>
                      </div>
                      <div class="px-4 py-3">
                        <p class="text-xs font-medium text-gray-400 mb-2">Lo que tienes tú</p>
                        <div class="flex flex-wrap gap-1">
                          <span v-for="s in rec.match_details?.hard_skills?.matched || []" :key="'hm-'+s"
                            class="inline-flex items-center gap-0.5 px-2 py-0.5 rounded-full text-xs font-medium bg-success-100 text-success-700">
                            <svg class="h-2.5 w-2.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
                            </svg>{{ s }}
                          </span>
                          <span v-for="s in rec.match_details?.hard_skills?.missing || []" :key="'hmi-'+s"
                            class="inline-flex items-center gap-0.5 px-2 py-0.5 rounded-full text-xs font-medium bg-danger-100 text-danger-700">
                            <svg class="h-2.5 w-2.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/>
                            </svg>{{ s }}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div v-else class="px-4 py-2.5 border-t border-gray-100">
                      <p class="text-xs text-gray-400 italic">Esta oferta no especificó habilidades técnicas.</p>
                    </div>
                  </div>

                  <!-- ── Habilidades Blandas ── -->
                  <div class="border border-gray-200 rounded-xl overflow-hidden">
                    <div class="px-4 py-3 bg-gray-50 flex items-center gap-3">
                      <svg class="w-4 h-4 text-emi-navy-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
                      </svg>
                      <div class="flex-1 min-w-0">
                        <div class="flex justify-between items-center mb-1.5">
                          <span class="text-sm font-semibold text-gray-800">Habilidades Blandas</span>
                          <span class="text-xs font-bold" :class="scoreColorText(rec.scores_detalle?.soft_skills_score ?? 0)">
                            {{ Math.round((rec.scores_detalle?.soft_skills_score ?? 0) * 100) }}%
                          </span>
                        </div>
                        <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div class="h-full rounded-full transition-all duration-700"
                            :class="scoreColorBg(rec.scores_detalle?.soft_skills_score ?? 0)"
                            :style="{ width: Math.round((rec.scores_detalle?.soft_skills_score ?? 0) * 100) + '%' }"/>
                        </div>
                      </div>
                    </div>
                    <div v-if="getSoftSkillsTotal(rec) > 0" class="grid grid-cols-2 divide-x divide-gray-100 border-t border-gray-100">
                      <div class="px-4 py-3">
                        <p class="text-xs font-medium text-gray-400 mb-2">Requeridas por la oferta</p>
                        <div class="flex flex-wrap gap-1">
                          <span v-for="s in [...(rec.match_details?.soft_skills?.matched||[]), ...(rec.match_details?.soft_skills?.missing||[])]"
                            :key="'rs-'+s" class="px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">{{ s }}</span>
                        </div>
                      </div>
                      <div class="px-4 py-3">
                        <p class="text-xs font-medium text-gray-400 mb-2">Lo que tienes tú</p>
                        <div class="flex flex-wrap gap-1">
                          <span v-for="s in rec.match_details?.soft_skills?.matched || []" :key="'sm-'+s"
                            class="inline-flex items-center gap-0.5 px-2 py-0.5 rounded-full text-xs font-medium bg-success-100 text-success-700">
                            <svg class="h-2.5 w-2.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
                            </svg>{{ s }}
                          </span>
                          <span v-for="s in rec.match_details?.soft_skills?.missing || []" :key="'smi-'+s"
                            class="inline-flex items-center gap-0.5 px-2 py-0.5 rounded-full text-xs font-medium bg-danger-100 text-danger-700">
                            <svg class="h-2.5 w-2.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/>
                            </svg>{{ s }}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div v-else class="px-4 py-2.5 border-t border-gray-100">
                      <p class="text-xs text-gray-400 italic">Esta oferta no especificó habilidades blandas.</p>
                    </div>
                  </div>

                  <!-- ── Formación Académica ── -->
                  <div class="border border-gray-200 rounded-xl overflow-hidden">
                    <div class="px-4 py-3 bg-gray-50 flex items-center gap-3">
                      <svg class="w-4 h-4 text-emi-navy-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"/>
                      </svg>
                      <div class="flex-1 min-w-0">
                        <div class="flex justify-between items-center mb-1.5">
                          <span class="text-sm font-semibold text-gray-800">Formación Académica</span>
                          <span class="text-xs font-bold" :class="scoreColorText(rec.scores_detalle?.education_score ?? 0)">
                            {{ Math.round((rec.scores_detalle?.education_score ?? 0) * 100) }}%
                          </span>
                        </div>
                        <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div class="h-full rounded-full transition-all duration-700"
                            :class="scoreColorBg(rec.scores_detalle?.education_score ?? 0)"
                            :style="{ width: Math.round((rec.scores_detalle?.education_score ?? 0) * 100) + '%' }"/>
                        </div>
                      </div>
                    </div>
                    <div class="grid grid-cols-2 divide-x divide-gray-100 border-t border-gray-100">
                      <div class="px-4 py-3">
                        <p class="text-xs font-medium text-gray-400 mb-2">Nivel requerido</p>
                        <span v-if="rec.match_details?.education?.required_level"
                          class="px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
                          {{ rec.match_details.education.required_level }}
                        </span>
                        <span v-else class="text-xs text-gray-400 italic">No especificado</span>
                      </div>
                      <div class="px-4 py-3">
                        <p class="text-xs font-medium text-gray-400 mb-2">Tu nivel</p>
                        <div class="flex items-center gap-1.5">
                          <span v-if="rec.match_details?.education" :class="[
                            'px-2.5 py-1 rounded-full text-xs font-medium',
                            rec.match_details.education.meets_requirement ? 'bg-success-100 text-success-700' : 'bg-danger-100 text-danger-700'
                          ]">{{ rec.match_details.education.cv_level || 'No registrado' }}</span>
                          <StatusIcon v-if="rec.match_details?.education" :ok="rec.match_details.education.meets_requirement" />
                          <span v-else class="text-xs text-gray-400 italic">Sin datos en tu CV</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- ── Experiencia Laboral ── -->
                  <div class="border border-gray-200 rounded-xl overflow-hidden">
                    <div class="px-4 py-3 bg-gray-50 flex items-center gap-3">
                      <svg class="w-4 h-4 text-emi-navy-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                      </svg>
                      <div class="flex-1 min-w-0">
                        <div class="flex justify-between items-center mb-1.5">
                          <span class="text-sm font-semibold text-gray-800">Experiencia Laboral</span>
                          <span class="text-xs font-bold" :class="scoreColorText(rec.scores_detalle?.experience_score ?? 0)">
                            {{ Math.round((rec.scores_detalle?.experience_score ?? 0) * 100) }}%
                          </span>
                        </div>
                        <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div class="h-full rounded-full transition-all duration-700"
                            :class="scoreColorBg(rec.scores_detalle?.experience_score ?? 0)"
                            :style="{ width: Math.round((rec.scores_detalle?.experience_score ?? 0) * 100) + '%' }"/>
                        </div>
                      </div>
                    </div>
                    <div class="grid grid-cols-2 divide-x divide-gray-100 border-t border-gray-100">
                      <div class="px-4 py-3">
                        <p class="text-xs font-medium text-gray-400 mb-2">Experiencia requerida</p>
                        <span v-if="rec.match_details?.experience?.required_years > 0"
                          class="px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
                          Al menos {{ rec.match_details.experience.required_years }} año(s)
                        </span>
                        <span v-else class="text-xs text-gray-400 italic">No requiere experiencia previa</span>
                      </div>
                      <div class="px-4 py-3">
                        <p class="text-xs font-medium text-gray-400 mb-2">Tu experiencia</p>
                        <div class="flex items-center gap-1.5">
                          <span v-if="rec.match_details?.experience" :class="[
                            'px-2.5 py-1 rounded-full text-xs font-medium',
                            rec.match_details.experience.meets_minimum ? 'bg-success-100 text-success-700' : 'bg-danger-100 text-danger-700'
                          ]">{{ rec.match_details.experience.cv_years }} año(s)</span>
                          <StatusIcon v-if="rec.match_details?.experience" :ok="rec.match_details.experience.meets_minimum" />
                          <span v-else class="text-xs text-gray-400 italic">Sin datos en tu CV</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- ── Idiomas ── -->
                  <div class="border border-gray-200 rounded-xl overflow-hidden">
                    <div class="px-4 py-3 bg-gray-50 flex items-center gap-3">
                      <svg class="w-4 h-4 text-emi-navy-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/>
                      </svg>
                      <div class="flex-1 min-w-0">
                        <div class="flex justify-between items-center mb-1.5">
                          <span class="text-sm font-semibold text-gray-800">Idiomas</span>
                          <span class="text-xs font-bold" :class="scoreColorText(rec.scores_detalle?.languages_score ?? 0)">
                            {{ Math.round((rec.scores_detalle?.languages_score ?? 0) * 100) }}%
                          </span>
                        </div>
                        <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div class="h-full rounded-full transition-all duration-700"
                            :class="scoreColorBg(rec.scores_detalle?.languages_score ?? 0)"
                            :style="{ width: Math.round((rec.scores_detalle?.languages_score ?? 0) * 100) + '%' }"/>
                        </div>
                      </div>
                    </div>
                    <div v-if="getRequiredLangsCount(rec) > 0" class="grid grid-cols-2 divide-x divide-gray-100 border-t border-gray-100">
                      <div class="px-4 py-3">
                        <p class="text-xs font-medium text-gray-400 mb-2">Requeridos</p>
                        <div class="flex flex-wrap gap-1">
                          <span v-for="l in getAllRequiredLangs(rec)" :key="'rl-'+l"
                            class="px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">{{ l }}</span>
                        </div>
                      </div>
                      <div class="px-4 py-3">
                        <p class="text-xs font-medium text-gray-400 mb-2">Los que dominas</p>
                        <div class="flex flex-wrap gap-1">
                          <span v-for="l in rec.match_details?.languages?.matched || []" :key="'lm-'+l"
                            class="inline-flex items-center gap-0.5 px-2 py-0.5 rounded-full text-xs font-medium bg-success-100 text-success-700">
                            <svg class="h-2.5 w-2.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
                            </svg>{{ l }}
                          </span>
                          <span v-for="l in rec.match_details?.languages?.missing || []" :key="'lmi-'+l"
                            class="inline-flex items-center gap-0.5 px-2 py-0.5 rounded-full text-xs font-medium bg-danger-100 text-danger-700">
                            <svg class="h-2.5 w-2.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/>
                            </svg>{{ l }}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div v-else class="px-4 py-2.5 border-t border-gray-100">
                      <p class="text-xs text-gray-400 italic">Esta oferta no requiere idiomas específicos.</p>
                    </div>
                  </div>

                  <!-- Otras habilidades del CV -->
                  <div v-if="getExtraSkills(rec).length > 0" class="p-4 bg-emi-navy-50 rounded-xl border border-emi-navy-100">
                    <p class="text-xs font-semibold text-emi-navy-700 mb-1">Otras habilidades que tienes</p>
                    <p class="text-xs text-emi-navy-500 mb-2.5">Están en tu CV pero esta oferta no las exigía — suman a tu perfil general.</p>
                    <div class="flex flex-wrap gap-1.5">
                      <span v-for="skill in getExtraSkills(rec)" :key="skill"
                        class="px-2.5 py-1 rounded-full text-xs font-medium bg-emi-navy-100 text-emi-navy-700 border border-emi-navy-200">
                        {{ skill }}
                      </span>
                    </div>
                  </div>

                </div>
              </section>

              <!-- ──────────────────────────────────────────────
                   3. ¿POR QUÉ EL SISTEMA CALIFICÓ ESTA OFERTA?
              ────────────────────────────────────────────── -->
              <section>
                <div class="flex items-center gap-2 mb-4">
                  <div class="w-7 h-7 bg-emi-gold-100 rounded-lg flex items-center justify-center shrink-0">
                    <svg class="w-4 h-4 text-emi-gold-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                    </svg>
                  </div>
                  <h4 class="text-sm font-bold text-emi-navy-800 uppercase tracking-wide">¿Por qué el sistema calificó esta oferta?</h4>
                </div>

                <!-- Contexto -->
                <div class="p-4 bg-gray-50 rounded-xl border-l-4 border-emi-navy-200 mb-4">
                  <p class="text-sm text-gray-600 leading-relaxed">
                    El motor de recomendación evaluó tu perfil contra cada oferta activa de forma ponderada,
                    considerando habilidades técnicas, blandas, formación, experiencia e idiomas.
                    Esta oferta alcanzó la clasificación
                    <strong :class="rec.clasificacion === 'APTO' ? 'text-emi-gold-600' : 'text-info-600'">
                      {{ rec.clasificacion }}
                    </strong>
                    con un puntaje de <strong class="text-emi-navy-700">{{ Math.round(rec.match_score * 100) }} / 100</strong>.
                  </p>
                </div>

                <!-- Fortalezas y áreas de mejora -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">

                  <!-- Fortalezas -->
                  <div class="bg-success-50 rounded-xl p-4 border border-success-100">
                    <h5 class="text-xs font-bold text-success-700 uppercase tracking-wide mb-3 flex items-center gap-1.5">
                      <svg class="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                      </svg>
                      Lo que jala a tu favor
                    </h5>
                    <ul class="space-y-2">
                      <li v-if="(rec.scores_detalle?.hard_skills_score ?? 0) >= 0.5"
                        class="flex items-start gap-2 text-sm text-success-800">
                        <span class="mt-1.5 w-1.5 h-1.5 rounded-full bg-success-500 shrink-0"></span>
                        Habilidades técnicas con <strong>{{ Math.round((rec.scores_detalle.hard_skills_score) * 100) }}%</strong> de cobertura
                      </li>
                      <li v-if="(rec.scores_detalle?.soft_skills_score ?? 0) >= 0.5"
                        class="flex items-start gap-2 text-sm text-success-800">
                        <span class="mt-1.5 w-1.5 h-1.5 rounded-full bg-success-500 shrink-0"></span>
                        Habilidades blandas con <strong>{{ Math.round((rec.scores_detalle.soft_skills_score) * 100) }}%</strong> de cobertura
                      </li>
                      <li v-if="(rec.scores_detalle?.education_score ?? 0) >= 0.5"
                        class="flex items-start gap-2 text-sm text-success-800">
                        <span class="mt-1.5 w-1.5 h-1.5 rounded-full bg-success-500 shrink-0"></span>
                        Formación académica valorada con <strong>{{ Math.round((rec.scores_detalle.education_score) * 100) }}%</strong>
                      </li>
                      <li v-if="getMatchedSkills(rec).length > 0"
                        class="flex items-start gap-2 text-sm text-success-800">
                        <span class="mt-1.5 w-1.5 h-1.5 rounded-full bg-success-500 shrink-0"></span>
                        Cumples con <strong>{{ getMatchedSkills(rec).length }} habilidades</strong> que la oferta requiere
                      </li>
                      <li v-if="(rec.match_details?.languages?.matched?.length ?? 0) > 0"
                        class="flex items-start gap-2 text-sm text-success-800">
                        <span class="mt-1.5 w-1.5 h-1.5 rounded-full bg-success-500 shrink-0"></span>
                        Dominas <strong>{{ rec.match_details.languages.matched.length }} idioma(s)</strong> solicitados
                      </li>
                      <li v-if="hasNoStrengths(rec)" class="text-sm text-success-700 italic">
                        Aún no se identificaron fortalezas destacadas.
                      </li>
                    </ul>
                  </div>

                  <!-- Áreas de mejora -->
                  <div class="bg-warning-50 rounded-xl p-4 border border-warning-100">
                    <h5 class="text-xs font-bold text-warning-700 uppercase tracking-wide mb-3 flex items-center gap-1.5">
                      <svg class="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                      </svg>
                      Qué podrías mejorar
                    </h5>
                    <ul class="space-y-2">
                      <li v-if="getMissingSkills(rec).length > 0"
                        class="flex items-start gap-2 text-sm text-warning-800">
                        <span class="mt-1.5 w-1.5 h-1.5 rounded-full bg-warning-500 shrink-0"></span>
                        Faltan <strong>{{ getMissingSkills(rec).length }} habilidades técnicas</strong> que pide la oferta
                      </li>
                      <li v-if="(rec.scores_detalle?.hard_skills_score ?? 0) < 0.5"
                        class="flex items-start gap-2 text-sm text-warning-800">
                        <span class="mt-1.5 w-1.5 h-1.5 rounded-full bg-warning-500 shrink-0"></span>
                        Fortalecer habilidades técnicas elevaría considerablemente tu puntuación
                      </li>
                      <li v-if="(rec.scores_detalle?.languages_score ?? 0) < 0.5"
                        class="flex items-start gap-2 text-sm text-warning-800">
                        <span class="mt-1.5 w-1.5 h-1.5 rounded-full bg-warning-500 shrink-0"></span>
                        Mejorar tu nivel de idiomas puede elevar tu compatibilidad
                      </li>
                      <li v-if="(rec.scores_detalle?.experience_score ?? 0) < 0.4"
                        class="flex items-start gap-2 text-sm text-warning-800">
                        <span class="mt-1.5 w-1.5 h-1.5 rounded-full bg-warning-500 shrink-0"></span>
                        La oferta requiere más experiencia de la que tienes registrada
                      </li>
                      <li v-if="hasNoImprovements(rec)" class="text-sm text-warning-700 italic">
                        ¡Sin brechas significativas! Tu perfil es muy competitivo.
                      </li>
                    </ul>
                  </div>
                </div>
              </section>

            </div>
            <!-- fin panel expandible -->

          </div>
        </div>
        <!-- fin v-for -->
      </div>

    </div>

  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, defineComponent, h } from 'vue'
import AppLayout from '@/shared/components/AppLayout.vue'
import EligibilityWarning from '../components/EligibilityWarning.vue'
import { useRecommendations } from '../composables/useRecommendations'
import { postularDesdeRecomendacion } from '../api/postulaciones.api'
import { formatApiError } from '@/shared/utils/apiError'

// ── Icono de estado (check / x) ───────────────────────────
const StatusIcon = defineComponent({
  props: { ok: Boolean },
  setup(props) {
    return () => h('svg', {
      class: ['w-4 h-4 shrink-0', props.ok ? 'text-success-500' : 'text-danger-400'],
      fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor'
    }, [
      h('path', {
        'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2',
        d: props.ok ? 'M5 13l4 4L19 7' : 'M6 18L18 6M6 6l12 12'
      })
    ])
  }
})

// ── Fases de carga ─────────────────────────────────────────
const PHASES = [
  'Analizando tu perfil...',
  'Evaluando ofertas disponibles...',
  'Identificando donde calificas...',
]
const phaseIndex = ref(0)
const loadingPhase = computed(() => PHASES[phaseIndex.value])
let phaseTimer = null

const {
  recommendations,
  perfilSummary,
  loading,
  refreshing,
  error,
  isEligible,
  eligibilityReason,
  eligibilityAction,
  missingFields,
  userRole,
  formatDate,
  loadRecommendations
} = useRecommendations()

onMounted(() => {
  phaseTimer = setInterval(() => {
    phaseIndex.value = (phaseIndex.value + 1) % PHASES.length
  }, 1400)
})
onUnmounted(() => clearInterval(phaseTimer))

// ── Filtrado: solo APTO y CONSIDERADO ────────────────────
const qualifiedRecommendations = computed(() =>
  recommendations.value.filter(r =>
    r.clasificacion === 'APTO' || r.clasificacion === 'CONSIDERADO'
  )
)

const totalEvaluadas   = computed(() => recommendations.value.length)
const aptoCount        = computed(() => recommendations.value.filter(r => r.clasificacion === 'APTO').length)
const consideradoCount = computed(() => recommendations.value.filter(r => r.clasificacion === 'CONSIDERADO').length)
const noAptoCount      = computed(() => recommendations.value.filter(r => r.clasificacion === 'NO_APTO').length)

// ── Expand ───────────────────────────────────────────────
const expandedId = ref(null)
const toggleExpand = (id) => {
  expandedId.value = expandedId.value === id ? null : id
}

// ── Postulaciones ─────────────────────────────────────────
const postulando  = ref(null)
const postResults = ref({})
const postErrors  = ref({})

const postular = async (rec) => {
  const ofertaId = rec.oferta_id
  if (!ofertaId) return
  postulando.value = ofertaId
  const newErrors = { ...postErrors.value }
  delete newErrors[ofertaId]
  postErrors.value = newErrors
  try {
    const result = await postularDesdeRecomendacion(ofertaId)
    postResults.value = { ...postResults.value, [ofertaId]: result }
    expandedId.value = ofertaId
  } catch (e) {
    postErrors.value = { ...postErrors.value, [ofertaId]: formatApiError(e, 'Error al procesar la postulación') }
  } finally {
    postulando.value = null
  }
}

// ── Elegibilidad por oferta ────────────────────────────────
const getOfferEligibility = (rec) => {
  const reqs = rec.oferta?.requisitos_especificos || {}
  const carreras = reqs.carreras_aceptadas || []
  const semestreMin = reqs.semestre_minimo ?? null
  const semestreMax = reqs.semestre_maximo ?? null

  const miCarrera   = perfilSummary.value?.carrera ?? null
  const miSemestre  = perfilSummary.value?.semestre_actual ?? null

  // Filtro por carrera (aplica a todos: estudiantes y titulados)
  if (carreras.length > 0 && miCarrera && !carreras.includes(miCarrera)) {
    return { eligible: false, reason: `Esta oferta es para: ${carreras.join(', ')}` }
  }

  // Filtro por semestre (solo estudiantes)
  if (userRole.value === 'estudiante' && miSemestre !== null) {
    if (semestreMin !== null && miSemestre < semestreMin) {
      return { eligible: false, reason: `Requiere a partir del ${semestreMin}° semestre (tú estás en ${miSemestre}°)` }
    }
    if (semestreMax !== null && miSemestre > semestreMax) {
      return { eligible: false, reason: `Solo para hasta ${semestreMax}° semestre (tú estás en ${miSemestre}°)` }
    }
  }

  return { eligible: true, reason: null }
}

// ── Helpers de habilidades ────────────────────────────────
const getMatchedSkills = (rec) => {
  const md = rec.match_details
  if (!md) return []
  return [...(md.hard_skills?.matched || []), ...(md.soft_skills?.matched || [])]
}

const getMissingSkills = (rec) => {
  const md = rec.match_details
  if (!md) return []
  return [...(md.hard_skills?.missing || []), ...(md.soft_skills?.missing || [])]
}

// ── Helpers para la tabla ─────────────────────────────────
const getHardMatchedCount  = (rec) => (rec.match_details?.hard_skills?.matched || []).length
const getHardSkillsTotal   = (rec) => getHardMatchedCount(rec) + (rec.match_details?.hard_skills?.missing || []).length
const getHardSkillsCoverage= (rec) => {
  const total = getHardSkillsTotal(rec)
  return total === 0 ? 0 : Math.round((getHardMatchedCount(rec) / total) * 100)
}

const getSoftMatchedCount  = (rec) => (rec.match_details?.soft_skills?.matched || []).length
const getSoftSkillsTotal   = (rec) => getSoftMatchedCount(rec) + (rec.match_details?.soft_skills?.missing || []).length
const getSoftSkillsCoverage= (rec) => {
  const total = getSoftSkillsTotal(rec)
  return total === 0 ? 0 : Math.round((getSoftMatchedCount(rec) / total) * 100)
}

const getLangMatchedCount = (rec) => (rec.match_details?.languages?.matched || []).length
const getRequiredLangsCount = (rec) =>
  getLangMatchedCount(rec) + (rec.match_details?.languages?.missing || []).length
const getAllRequiredLangs = (rec) => [
  ...(rec.match_details?.languages?.matched || []),
  ...(rec.match_details?.languages?.missing || [])
]
const getLangCoverage = (rec) => {
  const total = getRequiredLangsCount(rec)
  return total === 0 ? 0 : Math.round((getLangMatchedCount(rec) / total) * 100)
}

const getRequiredSkillsCount = (rec) => getHardSkillsTotal(rec) + getSoftSkillsTotal(rec)

const getExtraSkills = (rec) => {
  const md = rec.match_details
  if (!md) return []
  const cvHard   = md.cv_skills?.hard || []
  const matched  = new Set((md.hard_skills?.matched || []).map(s => s.toLowerCase()))
  const missing  = new Set((md.hard_skills?.missing || []).map(s => s.toLowerCase()))
  const preferred= new Set((md.hard_skills?.preferred_matched || []).map(s => s.toLowerCase()))
  const known    = new Set([...matched, ...missing, ...preferred])
  return cvHard.filter(s => !known.has(s.toLowerCase())).slice(0, 10)
}

// ── Helpers de color por score ────────────────────────────
const scoreColorText = (val) =>
  val >= 0.7 ? 'text-success-600' : val >= 0.4 ? 'text-warning-600' : 'text-danger-500'
const scoreColorBg = (val) =>
  val >= 0.7 ? 'bg-success-500' : val >= 0.4 ? 'bg-warning-500' : 'bg-danger-500'

// ── Fortalezas / mejoras ──────────────────────────────────
const hasNoStrengths = (rec) => {
  const sd = rec.scores_detalle || {}
  return (sd.hard_skills_score ?? 0) < 0.5 &&
         (sd.soft_skills_score ?? 0) < 0.5 &&
         (sd.education_score   ?? 0) < 0.5 &&
         getMatchedSkills(rec).length === 0
}

const hasNoImprovements = (rec) => {
  const sd = rec.scores_detalle || {}
  return getMissingSkills(rec).length === 0 &&
         (sd.hard_skills_score ?? 0) >= 0.5 &&
         (sd.languages_score   ?? 0) >= 0.5 &&
         (sd.experience_score  ?? 0) >= 0.4
}
</script>
