<template>
  <AppLayout>
    <div class="flex h-full min-h-screen">

      <!-- ═══════════════════════════════════════════════════════
           PANEL IZQUIERDO: Lista de ofertas + filtros
           ═══════════════════════════════════════════════════════ -->
      <div class="w-80 flex-shrink-0 border-r border-gray-200 bg-white flex flex-col">

        <!-- Encabezado panel izquierdo -->
        <div class="px-4 pt-6 pb-3 border-b border-gray-100">
          <h2 class="text-base font-bold text-slate-800">Ofertas Laborales</h2>
          <p class="text-xs text-slate-500 mt-0.5">Selecciona una oferta para ver el ranking</p>
        </div>

        <!-- Filtros -->
        <div class="px-4 py-3 space-y-2 border-b border-gray-100 bg-gray-50">

          <!-- Buscador -->
          <div class="relative">
            <svg class="absolute left-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-gray-400"
              fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            <input
              v-model="filters.search"
              @input="debouncedLoad"
              type="text"
              placeholder="Buscar oferta..."
              class="w-full pl-8 pr-3 py-1.5 text-xs border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-emi-navy-400"
            />
          </div>

          <!-- Tipo -->
          <div class="flex gap-1.5">
            <button
              v-for="t in tipoOptions"
              :key="t.value"
              @click="filters.tipo = t.value; loadOfertas()"
              :class="[
                'flex-1 text-xs py-1 rounded-lg font-medium transition-colors',
                filters.tipo === t.value
                  ? 'bg-emi-navy-500 text-white'
                  : 'bg-white text-gray-500 border border-gray-200 hover:border-emi-navy-300'
              ]"
            >{{ t.label }}</button>
          </div>

          <!-- Estado -->
          <div class="flex gap-1.5">
            <button
              v-for="e in estadoOptions"
              :key="e.value"
              @click="setEstado(e.value)"
              :class="[
                'flex-1 text-xs py-1 rounded-lg font-medium transition-colors',
                estadoKey === e.value
                  ? 'bg-emi-navy-500 text-white'
                  : 'bg-white text-gray-500 border border-gray-200 hover:border-emi-navy-300'
              ]"
            >{{ e.label }}</button>
          </div>

          <!-- Top N -->
          <div class="flex items-center gap-2">
            <span class="text-xs text-gray-500 whitespace-nowrap">Top candidatos:</span>
            <div class="flex gap-1 flex-1">
              <button
                v-for="n in [3, 5, 10]"
                :key="n"
                @click="topN = n; selectedOferta && loadRanking(selectedOferta.id)"
                :class="[
                  'flex-1 text-xs py-1 rounded-lg font-medium transition-colors',
                  topN === n
                    ? 'bg-emi-gold-500 text-white'
                    : 'bg-white text-gray-500 border border-gray-200 hover:border-emi-gold-300'
                ]"
              >{{ n }}</button>
            </div>
          </div>
        </div>

        <!-- Lista de ofertas -->
        <div class="flex-1 overflow-y-auto">
          <div v-if="loadingOfertas" class="flex justify-center py-10">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-emi-navy-500"></div>
          </div>

          <p v-else-if="ofertas.length === 0" class="text-center text-xs text-gray-400 py-10 px-4">
            No hay ofertas que coincidan con los filtros
          </p>

          <div v-else>
            <button
              v-for="oferta in ofertas"
              :key="oferta.id"
              @click="selectOferta(oferta)"
              :class="[
                'w-full text-left px-4 py-3 border-b border-gray-100 transition-colors',
                selectedOferta?.id === oferta.id
                  ? 'bg-emi-navy-50 border-l-2 border-l-emi-navy-500'
                  : 'hover:bg-gray-50'
              ]"
            >
              <div class="flex items-start justify-between gap-2">
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-1.5 mb-0.5">
                    <span :class="[
                      'inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium',
                      oferta.tipo === 'pasantia' ? 'bg-purple-100 text-purple-700' : 'bg-emi-navy-100 text-emi-navy-700'
                    ]">
                      {{ oferta.tipo === 'pasantia' ? 'Pasantía' : 'Empleo' }}
                    </span>
                    <span v-if="!oferta.is_active"
                      class="inline-flex items-center px-1.5 py-0.5 rounded text-xs bg-gray-100 text-gray-500">
                      Cerrada
                    </span>
                  </div>
                  <p class="text-xs font-semibold text-gray-900 truncate">{{ oferta.titulo }}</p>
                  <p v-if="oferta.institution_name" class="text-xs text-gray-400 truncate">
                    {{ oferta.institution_name }}
                  </p>
                </div>
                <!-- Badge postulaciones -->
                <div class="flex-shrink-0 text-center">
                  <span class="block text-sm font-bold text-emi-navy-600">{{ oferta.stats?.total ?? 0 }}</span>
                  <span class="text-xs text-gray-400">post.</span>
                </div>
              </div>

              <!-- Mini barra de stats -->
              <div v-if="oferta.stats?.total > 0" class="mt-2 flex gap-1 h-1">
                <div
                  :style="{ width: (oferta.stats.apto / oferta.stats.total * 100) + '%' }"
                  class="bg-emi-gold-400 rounded-l"
                  :title="`APTO: ${oferta.stats.apto}`"
                />
                <div
                  :style="{ width: (oferta.stats.considerado / oferta.stats.total * 100) + '%' }"
                  class="bg-emi-navy-400"
                  :title="`CONSIDERADO: ${oferta.stats.considerado}`"
                />
                <div
                  :style="{ width: (oferta.stats.no_apto / oferta.stats.total * 100) + '%' }"
                  class="bg-red-300 rounded-r"
                  :title="`NO APTO: ${oferta.stats.no_apto}`"
                />
              </div>
            </button>
          </div>
        </div>
      </div>

      <!-- ═══════════════════════════════════════════════════════
           PANEL DERECHO: Encabezado fijo + contenido scrolleable
           ═══════════════════════════════════════════════════════ -->
      <div class="flex-1 flex flex-col overflow-hidden bg-gray-50">

        <!-- Encabezado fijo de la sección -->
        <div class="flex-shrink-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between shadow-sm">
          <div>
            <h1 class="text-xl font-bold text-slate-800">Evaluación de Candidatos</h1>
            <p class="text-sm text-slate-400 mt-0.5">
              Análisis y recomendación de personal para convocatorias laborales
            </p>
          </div>
          <!-- Botón Generar Informe (visible solo con oferta seleccionada y candidatos) -->
          <button
            v-if="selectedOferta && rankingData?.candidatos?.length > 0"
            @click="handleGenerarInforme"
            :disabled="generandoPdf"
            class="inline-flex items-center gap-2 px-4 py-2 bg-emi-navy-600 hover:bg-emi-navy-700 disabled:opacity-60 disabled:cursor-not-allowed text-white text-sm font-semibold rounded-lg shadow-sm transition-colors"
          >
            <svg v-if="!generandoPdf" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <svg v-else class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            {{ generandoPdf ? 'Generando PDF...' : 'Generar Informe' }}
          </button>
        </div>

        <!-- Área scrolleable -->
        <div class="flex-1 overflow-y-auto">

        <!-- Estado vacío -->
        <div v-if="!selectedOferta" class="flex flex-col items-center justify-center h-full py-24 text-center px-8">
          <svg class="h-16 w-16 text-gray-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/>
          </svg>
          <p class="text-gray-400 font-medium">Selecciona una oferta</p>
          <p class="text-xs text-gray-300 mt-1">para ver la evaluación y el ranking de candidatos</p>
        </div>

        <!-- Contenido de la oferta seleccionada -->
        <div v-else class="max-w-4xl mx-auto px-6 py-8 space-y-6">

          <!-- ────────────────────────────────────────
               SECCIÓN 1: Encabezado de la evaluación
               ──────────────────────────────────────── -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">

            <!-- Header colorido -->
            <div class="bg-gradient-to-r from-emi-navy-600 to-emi-navy-800 px-6 py-5">
              <div class="flex items-start justify-between gap-4">
                <div>
                  <div class="flex items-center gap-2 mb-1">
                    <span :class="[
                      'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold',
                      selectedOferta.tipo === 'pasantia'
                        ? 'bg-purple-200 text-purple-800'
                        : 'bg-emi-gold-200 text-emi-gold-800'
                    ]">
                      {{ selectedOferta.tipo === 'pasantia' ? 'Pasantía' : 'Empleo' }}
                    </span>
                    <span v-if="!selectedOferta.is_active"
                      class="inline-flex items-center px-2 py-0.5 rounded-full text-xs bg-white/20 text-white">
                      Convocatoria cerrada
                    </span>
                  </div>
                  <h1 class="text-xl font-bold text-white">{{ selectedOferta.titulo }}</h1>
                  <p v-if="selectedOferta.institution_name" class="text-emi-navy-200 text-sm mt-0.5">
                    {{ selectedOferta.institution_name }}
                    <span v-if="selectedOferta.sector" class="opacity-70"> · {{ selectedOferta.sector }}</span>
                  </p>
                </div>
                <!-- Stats rápidas -->
                <div class="text-right text-white flex-shrink-0">
                  <div class="text-2xl font-bold">{{ rankingData?.total_postulantes ?? 0 }}</div>
                  <div class="text-xs text-emi-navy-200">postulante{{ rankingData?.total_postulantes !== 1 ? 's' : '' }}</div>
                </div>
              </div>
            </div>

            <!-- Detalles de la convocatoria -->
            <div class="px-6 py-5">
              <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">
                Evaluación de {{ selectedOferta.institution_name || 'la institución' }}
              </h3>
              <p class="text-xs text-gray-400 mb-4 leading-relaxed">
                A continuación se presentan los datos de esta convocatoria, incluyendo sus condiciones,
                modalidad y los requisitos que definen el perfil del candidato ideal buscado por la institución.
              </p>

              <!-- Descripción / Objetivo -->
              <p v-if="selectedOferta.descripcion" class="text-sm text-gray-700 leading-relaxed mb-4">
                {{ selectedOferta.descripcion }}
              </p>

              <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
                <div v-if="selectedOferta.cupos_disponibles" class="bg-gray-50 rounded-lg p-3">
                  <dt class="text-xs text-gray-400 mb-0.5">Cupos disponibles</dt>
                  <dd class="text-sm font-semibold text-gray-900">{{ selectedOferta.cupos_disponibles }}</dd>
                </div>
                <div v-if="selectedOferta.modalidad" class="bg-gray-50 rounded-lg p-3">
                  <dt class="text-xs text-gray-400 mb-0.5">Modalidad</dt>
                  <dd class="text-sm font-semibold text-gray-900 capitalize">{{ selectedOferta.modalidad }}</dd>
                </div>
                <div v-if="selectedOferta.ubicacion" class="bg-gray-50 rounded-lg p-3">
                  <dt class="text-xs text-gray-400 mb-0.5">Ubicación</dt>
                  <dd class="text-sm font-semibold text-gray-900">{{ selectedOferta.ubicacion }}</dd>
                </div>
                <div v-if="selectedOferta.area" class="bg-gray-50 rounded-lg p-3">
                  <dt class="text-xs text-gray-400 mb-0.5">Área</dt>
                  <dd class="text-sm font-semibold text-gray-900">{{ selectedOferta.area }}</dd>
                </div>
                <div v-if="selectedOferta.fecha_inicio" class="bg-gray-50 rounded-lg p-3">
                  <dt class="text-xs text-gray-400 mb-0.5">Fecha inicio</dt>
                  <dd class="text-sm font-semibold text-gray-900">{{ formatDate(selectedOferta.fecha_inicio) }}</dd>
                </div>
                <div v-if="selectedOferta.fecha_cierre" class="bg-gray-50 rounded-lg p-3">
                  <dt class="text-xs text-gray-400 mb-0.5">Fecha cierre</dt>
                  <dd class="text-sm font-semibold text-gray-900">{{ formatDate(selectedOferta.fecha_cierre) }}</dd>
                </div>
              </div>

              <!-- Contacto -->
              <div v-if="selectedOferta.contact_email || selectedOferta.contact_phone"
                class="mt-4 flex flex-wrap gap-4">
                <a v-if="selectedOferta.contact_email"
                  :href="'mailto:' + selectedOferta.contact_email"
                  class="inline-flex items-center gap-1.5 text-xs text-blue-600 hover:underline">
                  <svg class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                  </svg>
                  {{ selectedOferta.contact_email }}
                </a>
                <span v-if="selectedOferta.contact_phone"
                  class="inline-flex items-center gap-1.5 text-xs text-gray-600">
                  <svg class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                  </svg>
                  {{ selectedOferta.contact_phone }}
                </span>
              </div>

              <!-- Requisitos de la oferta -->
              <div v-if="selectedOferta.requirements && hasRequisitos(selectedOferta.requirements)"
                class="mt-4 pt-4 border-t border-gray-100">
                <h4 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Requisitos de la convocatoria</h4>
                <div class="space-y-2">
                  <div v-if="selectedOferta.requirements.required_education_level" class="flex gap-3">
                    <dt class="text-xs text-gray-400 w-36 flex-shrink-0">Nivel educativo mín.</dt>
                    <dd class="text-xs font-medium text-gray-800">{{ selectedOferta.requirements.required_education_level }}</dd>
                  </div>
                  <div v-if="selectedOferta.requirements.min_experience_years > 0" class="flex gap-3">
                    <dt class="text-xs text-gray-400 w-36 flex-shrink-0">Experiencia mín.</dt>
                    <dd class="text-xs font-medium text-gray-800">{{ selectedOferta.requirements.min_experience_years }} año(s)</dd>
                  </div>
                  <div v-if="selectedOferta.requirements.required_skills?.length > 0">
                    <dt class="text-xs text-gray-400 mb-1.5">Habilidades requeridas</dt>
                    <div class="flex flex-wrap gap-1.5">
                      <span v-for="s in selectedOferta.requirements.required_skills" :key="s"
                        class="px-2 py-0.5 bg-emi-navy-50 text-emi-navy-700 border border-emi-navy-200 rounded-full text-xs">
                        {{ s }}
                      </span>
                    </div>
                  </div>
                  <div v-if="selectedOferta.requirements.preferred_skills?.length > 0">
                    <dt class="text-xs text-gray-400 mb-1.5">Habilidades deseables</dt>
                    <div class="flex flex-wrap gap-1.5">
                      <span v-for="s in selectedOferta.requirements.preferred_skills" :key="s"
                        class="px-2 py-0.5 bg-gray-100 text-gray-600 border border-gray-200 rounded-full text-xs">
                        {{ s }}
                      </span>
                    </div>
                  </div>
                  <div v-if="selectedOferta.requirements.required_languages?.length > 0" class="flex gap-3">
                    <dt class="text-xs text-gray-400 w-36 flex-shrink-0">Idiomas</dt>
                    <dd class="text-xs font-medium text-gray-800">{{ selectedOferta.requirements.required_languages.join(', ') }}</dd>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- ────────────────────────────────────────
               SECCIÓN 2: Recomendación de personal
               ──────────────────────────────────────── -->
          <div>
            <div class="flex items-center justify-between mb-4">
              <div>
                <h2 class="text-lg font-bold text-slate-800">Recomendación de Personal</h2>
                <p class="text-sm text-slate-500 mt-0.5">
                  Top {{ topN }} candidatos con mayor índice de correspondencia, ordenados de forma descendente.
                </p>
                <p class="text-xs text-slate-400 mt-1">
                  El puntaje es calculado por el modelo de evaluación ML ponderando habilidades, formación,
                  experiencia e idiomas. Expande cada tarjeta para ver el desglose detallado.
                </p>
              </div>
              <!-- Distribución rápida -->
              <div v-if="rankingData?.total_postulantes > 0" class="flex gap-3 text-center">
                <div>
                  <div class="text-sm font-bold text-emi-gold-600">{{ statsApto }}</div>
                  <div class="text-xs text-gray-400">APTO</div>
                </div>
                <div>
                  <div class="text-sm font-bold text-emi-navy-600">{{ statsConsiderado }}</div>
                  <div class="text-xs text-gray-400">CONSID.</div>
                </div>
                <div>
                  <div class="text-sm font-bold text-red-500">{{ statsNoApto }}</div>
                  <div class="text-xs text-gray-400">NO APTO</div>
                </div>
              </div>
            </div>

            <!-- Loading ranking -->
            <div v-if="loadingRanking" class="flex justify-center py-12">
              <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-emi-navy-500"></div>
            </div>

            <!-- Sin postulaciones -->
            <div v-else-if="!rankingData || rankingData.candidatos.length === 0"
              class="bg-white rounded-xl shadow-sm border border-gray-200 text-center py-12 px-6">
              <svg class="mx-auto h-12 w-12 text-gray-300 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              <p class="text-gray-400 font-medium">Sin postulaciones aún</p>
              <p class="text-xs text-gray-300 mt-1">Nadie se ha postulado a esta oferta todavía</p>
            </div>

            <!-- Cards de candidatos -->
            <div v-else class="space-y-4">
              <div
                v-for="candidato in rankingData.candidatos"
                :key="candidato.usuario_id"
                class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden"
              >
                <!-- Header del candidato -->
                <div class="px-5 py-4">
                  <div class="flex items-start gap-4">

                    <!-- Rank badge -->
                    <div :class="[
                      'flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center text-sm font-black shadow-sm',
                      candidato.rank === 1 ? 'bg-emi-gold-400 text-white' :
                      candidato.rank === 2 ? 'bg-gray-300 text-gray-700' :
                      candidato.rank === 3 ? 'bg-amber-600 text-white' :
                      'bg-emi-navy-100 text-emi-navy-700'
                    ]">
                      #{{ candidato.rank }}
                    </div>

                    <!-- Info candidato -->
                    <div class="flex-1 min-w-0">
                      <div class="flex items-center gap-2 flex-wrap">
                        <h3 class="text-base font-bold text-gray-900">
                          {{ candidato.perfil.nombre_completo }}
                        </h3>
                        <Badge
                          :variant="candidato.clasificacion === 'APTO' ? 'gold'
                            : candidato.clasificacion === 'CONSIDERADO' ? 'navy' : 'danger'"
                        >
                          {{ candidato.clasificacion }}
                        </Badge>
                        <span v-if="candidato.perfil.rol"
                          class="text-xs px-2 py-0.5 bg-gray-100 text-gray-500 rounded-full capitalize">
                          {{ candidato.perfil.rol }}
                        </span>
                      </div>
                      <div class="flex flex-wrap gap-3 mt-1 text-xs text-gray-400">
                        <span v-if="candidato.perfil.email">{{ candidato.perfil.email }}</span>
                        <span v-if="candidato.perfil.telefono">{{ candidato.perfil.telefono }}</span>
                        <span v-if="candidato.perfil.education_level">
                          {{ candidato.perfil.education_level }}
                        </span>
                        <span v-if="candidato.perfil.experience_years > 0">
                          {{ candidato.perfil.experience_years }} año(s) exp.
                        </span>
                      </div>
                    </div>

                    <!-- Puntaje -->
                    <div class="flex-shrink-0 text-right">
                      <div :class="[
                        'text-3xl font-black leading-none',
                        candidato.clasificacion === 'APTO' ? 'text-emi-gold-600' :
                        candidato.clasificacion === 'CONSIDERADO' ? 'text-emi-navy-600' : 'text-red-500'
                      ]">
                        {{ Math.round(candidato.match_score * 100) }}%
                      </div>
                      <div class="text-xs text-gray-400 mt-0.5">compatibilidad</div>
                    </div>
                  </div>

                  <!-- Barra de score general -->
                  <div class="mt-3">
                    <ProgressBar :value="candidato.match_score * 100" :showLabel="false" size="sm" />
                  </div>

                  <!-- Tags de fortalezas y debilidades -->
                  <div v-if="candidato.fortalezas?.length || candidato.debilidades?.length"
                    class="mt-3 flex flex-wrap gap-2">
                    <span
                      v-for="f in candidato.fortalezas"
                      :key="f"
                      class="inline-flex items-center gap-1 px-2 py-0.5 bg-green-50 text-green-700 border border-green-200 rounded-full text-xs"
                    >
                      <svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                      </svg>
                      {{ f }}
                    </span>
                    <span
                      v-for="d in candidato.debilidades"
                      :key="d"
                      class="inline-flex items-center gap-1 px-2 py-0.5 bg-red-50 text-red-600 border border-red-200 rounded-full text-xs"
                    >
                      <svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      {{ d }}
                    </span>
                  </div>
                </div>

                <!-- Footer con acciones -->
                <div class="px-5 py-2.5 bg-gray-50 border-t border-gray-100 flex items-center justify-between">
                  <button
                    @click="toggleExpand(candidato.usuario_id)"
                    class="inline-flex items-center gap-1.5 text-sm text-blue-600 hover:text-blue-800 font-medium transition-colors"
                  >
                    <svg
                      :class="['h-4 w-4 transition-transform duration-200', expandedId === candidato.usuario_id ? 'rotate-180' : '']"
                      fill="none" viewBox="0 0 24 24" stroke="currentColor"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                    {{ expandedId === candidato.usuario_id ? 'Ocultar detalle' : 'Ver justificación detallada' }}
                  </button>

                  <router-link
                    :to="'/admin/users/' + candidato.usuario_id"
                    class="inline-flex items-center gap-1.5 text-xs text-slate-500 hover:text-slate-700 font-medium transition-colors"
                  >
                    <svg class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2"/>
                    </svg>
                    Ver perfil completo
                  </router-link>
                </div>

                <!-- Panel expandible: justificación detallada -->
                <div v-if="expandedId === candidato.usuario_id" class="px-5 py-4 border-t border-gray-200 space-y-5">

                  <!-- Perfil del candidato -->
                  <div>
                    <h4 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Resumen del Perfil</h4>
                    <p class="text-xs text-gray-400 mb-3">Datos de contacto y habilidades declaradas en el perfil del candidato.</p>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">

                      <div v-if="candidato.perfil.hard_skills?.length > 0">
                        <p class="text-xs text-gray-400 mb-1.5">Habilidades técnicas</p>
                        <div class="flex flex-wrap gap-1.5">
                          <span v-for="s in candidato.perfil.hard_skills.slice(0, 8)" :key="s"
                            class="px-2 py-0.5 bg-emi-navy-50 text-emi-navy-700 border border-emi-navy-200 rounded-full text-xs">
                            {{ s }}
                          </span>
                          <span v-if="candidato.perfil.hard_skills.length > 8"
                            class="px-2 py-0.5 bg-gray-100 text-gray-500 rounded-full text-xs">
                            +{{ candidato.perfil.hard_skills.length - 8 }} más
                          </span>
                        </div>
                      </div>

                      <div v-if="candidato.perfil.soft_skills?.length > 0">
                        <p class="text-xs text-gray-400 mb-1.5">Habilidades blandas</p>
                        <div class="flex flex-wrap gap-1.5">
                          <span v-for="s in candidato.perfil.soft_skills.slice(0, 6)" :key="s"
                            class="px-2 py-0.5 bg-gray-100 text-gray-600 border border-gray-200 rounded-full text-xs">
                            {{ s }}
                          </span>
                        </div>
                      </div>

                      <div v-if="candidato.perfil.languages?.length > 0">
                        <p class="text-xs text-gray-400 mb-1">Idiomas</p>
                        <p class="text-xs text-gray-700">{{ candidato.perfil.languages.join(', ') }}</p>
                      </div>

                      <div v-if="candidato.postulado_en">
                        <p class="text-xs text-gray-400 mb-1">Fecha de postulación</p>
                        <p class="text-xs text-gray-700">{{ formatDate(candidato.postulado_en) }}</p>
                      </div>
                    </div>
                  </div>

                  <!-- Scores por dimensión -->
                  <div v-if="candidato.scores_detalle && Object.keys(candidato.scores_detalle).length > 0">
                    <h4 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">
                      Justificación del Score — Detalle por Dimensión
                    </h4>
                    <p class="text-xs text-gray-400 mb-3">
                      Puntaje obtenido en cada dimensión evaluada. El puntaje global es la suma ponderada de estas dimensiones.
                    </p>
                    <div class="space-y-2.5">
                      <div v-for="(value, key) in candidato.scores_detalle" :key="key">
                        <ProgressBar :value="value * 100" :label="formatScoreLabel(key)" size="md" />
                      </div>
                    </div>
                  </div>

                  <!-- Match detail (skills matched/missing) -->
                  <MatchDetailSection
                    v-if="candidato.match_details"
                    :matchDetails="candidato.match_details"
                    :clasificacion="candidato.clasificacion"
                  />

                </div>
              </div>
            </div>
          </div>

        </div>
      </div><!-- fin área scrolleable -->
      </div><!-- fin panel derecho (flex-col) -->

    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '@/shared/components/AppLayout.vue'
import Badge from '@/shared/components/ui/Badge.vue'
import ProgressBar from '@/shared/components/ui/ProgressBar.vue'
import MatchDetailSection from '@/features/recommendations/components/MatchDetailSection.vue'
import { getOfertasConStats, getRankingCandidatos, generarInforme } from '../api/ranking.api'

const router = useRouter()

// ── Filtros ────────────────────────────────────────────
const filters = ref({ search: '', tipo: '' })
const estadoKey = ref('todas')  // 'activas' | 'cerradas' | 'todas'
const topN = ref(3)
const searchTimeout = ref(null)

const tipoOptions = [
  { value: '', label: 'Todas' },
  { value: 'pasantia', label: 'Pasantías' },
  { value: 'empleo', label: 'Empleos' },
]
const estadoOptions = [
  { value: 'todas', label: 'Todas' },
  { value: 'activas', label: 'Activas' },
  { value: 'cerradas', label: 'Cerradas' },
]

// ── Estado ─────────────────────────────────────────────
const ofertas = ref([])
const loadingOfertas = ref(false)
const selectedOferta = ref(null)
const rankingData = ref(null)
const loadingRanking = ref(false)
const expandedId = ref(null)
const generandoPdf = ref(false)

// ── Computed ───────────────────────────────────────────
const statsApto = computed(() =>
  rankingData.value?.candidatos.filter(c => c.clasificacion === 'APTO').length ?? 0
)
const statsConsiderado = computed(() =>
  rankingData.value?.candidatos.filter(c => c.clasificacion === 'CONSIDERADO').length ?? 0
)
const statsNoApto = computed(() =>
  rankingData.value?.candidatos.filter(c => c.clasificacion === 'NO_APTO').length ?? 0
)

// ── Helpers ────────────────────────────────────────────
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' })
}

const formatScoreLabel = (key) => ({
  hard_skills_score: 'Habilidades Técnicas',
  soft_skills_score: 'Habilidades Blandas',
  education_score: 'Formación Académica',
  experience_score: 'Experiencia',
  languages_score: 'Idiomas',
}[key] || key)

const hasRequisitos = (req) =>
  req && (
    req.required_education_level ||
    req.min_experience_years > 0 ||
    req.required_skills?.length > 0 ||
    req.preferred_skills?.length > 0 ||
    req.required_languages?.length > 0
  )

const toggleExpand = (id) => {
  expandedId.value = expandedId.value === id ? null : id
}

const setEstado = (value) => {
  estadoKey.value = value
  loadOfertas()
}

const debouncedLoad = () => {
  clearTimeout(searchTimeout.value)
  searchTimeout.value = setTimeout(loadOfertas, 300)
}

// ── Acciones ───────────────────────────────────────────
const loadOfertas = async () => {
  loadingOfertas.value = true
  try {
    const params = {
      include_expired: true,
    }
    if (filters.value.tipo) params.tipo = filters.value.tipo
    if (estadoKey.value === 'activas') params.is_active = true
    if (estadoKey.value === 'cerradas') params.is_active = false
    if (filters.value.search) params.search = filters.value.search

    const data = await getOfertasConStats(params)
    ofertas.value = data.ofertas || []
  } catch (e) {
    console.error('Error cargando ofertas:', e)
  } finally {
    loadingOfertas.value = false
  }
}

const selectOferta = async (oferta) => {
  selectedOferta.value = oferta
  expandedId.value = null
  rankingData.value = null
  await loadRanking(oferta.id)
}

const loadRanking = async (ofertaId) => {
  loadingRanking.value = true
  try {
    rankingData.value = await getRankingCandidatos(ofertaId, topN.value)
  } catch (e) {
    console.error('Error cargando ranking:', e)
  } finally {
    loadingRanking.value = false
  }
}

const handleGenerarInforme = async () => {
  if (!selectedOferta.value || generandoPdf.value) return
  generandoPdf.value = true
  try {
    const titulo = (selectedOferta.value.titulo || 'informe').slice(0, 30).replace(/\s+/g, '-').toLowerCase()
    await generarInforme(selectedOferta.value.id, topN.value, `informe-evaluacion-${titulo}.pdf`)
  } catch (e) {
    console.error('Error generando informe:', e)
  } finally {
    generandoPdf.value = false
  }
}

// ── Ciclo de vida ──────────────────────────────────────
onMounted(loadOfertas)
</script>
