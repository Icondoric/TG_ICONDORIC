<template>
  <AppLayout>
    <div class="max-w-4xl mx-auto px-6 py-8 space-y-6">

      <!-- ═══ ENCABEZADO ESTÁNDAR ═══ -->
      <div class="flex items-start justify-between gap-6">
        <div>
          <!-- Breadcrumb -->
          <router-link
            to="/admin/ranking-candidatos"
            class="inline-flex items-center gap-1.5 text-xs text-emi-navy-400 hover:text-emi-navy-600 font-medium transition-colors mb-2"
          >
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
            Volver a Evaluación de Candidatos
          </router-link>
          <h1 class="text-3xl font-bold text-emi-navy-500">Evaluación de Postulantes</h1>
          <p class="mt-1 text-gray-600">
            Candidatos evaluados y ordenados por compatibilidad con la oferta seleccionada.
          </p>
        </div>

        <div class="flex items-center gap-2 flex-shrink-0">
          <!-- Botón Actualizar -->
          <button
            @click="loadOferta"
            :disabled="loadingOferta || loadingRanking"
            class="inline-flex items-center gap-2 px-4 py-2 bg-white border border-emi-navy-200 hover:border-emi-navy-400 text-emi-navy-600 text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
          >
            <svg :class="['h-4 w-4', (loadingOferta || loadingRanking) && 'animate-spin']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            Actualizar
          </button>

          <!-- Botón Generar Informe -->
          <button
            v-if="rankingData?.candidatos?.length > 0"
            @click="handleGenerarInforme"
            :disabled="generandoPdf"
            class="btn-emi-primary inline-flex items-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed"
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
      </div>

      <!-- Loading inicial -->
      <div v-if="loadingOferta" class="flex justify-center py-20">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-emi-navy-500"></div>
      </div>

      <!-- Error cargando oferta -->
      <div v-else-if="errorOferta" class="card-emi text-center py-12">
        <div class="w-12 h-12 bg-danger-50 rounded-full flex items-center justify-center mx-auto mb-3">
          <svg class="h-6 w-6 text-danger-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <p class="text-danger-600 font-semibold">No se pudo cargar la oferta</p>
        <p class="text-sm text-gray-400 mt-1">{{ errorOferta }}</p>
        <router-link to="/admin/ranking-candidatos" class="btn-emi-primary inline-flex items-center gap-2 mt-4">
          Volver al listado
        </router-link>
      </div>

      <template v-else-if="oferta">

        <!-- ═══════════════════════════════════════════════════════
             SECCIÓN 1: Tarjeta de la oferta
             ═══════════════════════════════════════════════════════ -->
        <div class="card-emi !p-0 overflow-hidden">

          <!-- Header con gradiente -->
          <div class="bg-gradient-to-r from-emi-navy-600 to-emi-navy-800 px-6 py-5">
            <div class="flex items-start justify-between gap-4">
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <span :class="[
                    'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold',
                    oferta.tipo === 'pasantia' ? 'bg-info-100 text-info-700' : 'bg-emi-gold-200 text-emi-gold-800'
                  ]">
                    {{ oferta.tipo === 'pasantia' ? 'Pasantía' : 'Empleo' }}
                  </span>
                  <span v-if="!oferta.is_active"
                    class="inline-flex items-center px-2 py-0.5 rounded-full text-xs bg-white/20 text-white">
                    Convocatoria cerrada
                  </span>
                </div>
                <h2 class="text-xl font-bold text-white">{{ oferta.titulo }}</h2>
                <p v-if="oferta.institution_name" class="text-emi-navy-200 text-sm mt-0.5">
                  {{ oferta.institution_name }}
                  <span v-if="oferta.sector" class="opacity-70"> · {{ oferta.sector }}</span>
                </p>
              </div>
              <div class="text-right text-white flex-shrink-0">
                <div class="text-2xl font-bold">{{ rankingData?.total_postulantes ?? 0 }}</div>
                <div class="text-xs text-emi-navy-200">postulante{{ rankingData?.total_postulantes !== 1 ? 's' : '' }}</div>
              </div>
            </div>
          </div>

          <!-- Detalles -->
          <div class="px-6 py-5">
            <p v-if="oferta.descripcion" class="text-sm text-gray-700 leading-relaxed mb-4">
              {{ oferta.descripcion }}
            </p>

            <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
              <div v-if="oferta.cupos_disponibles" class="bg-emi-navy-50 rounded-lg p-3">
                <dt class="text-xs text-emi-navy-400 mb-0.5">Cupos disponibles</dt>
                <dd class="text-sm font-semibold text-emi-navy-800">{{ oferta.cupos_disponibles }}</dd>
              </div>
              <div v-if="oferta.modalidad" class="bg-emi-navy-50 rounded-lg p-3">
                <dt class="text-xs text-emi-navy-400 mb-0.5">Modalidad</dt>
                <dd class="text-sm font-semibold text-emi-navy-800 capitalize">{{ oferta.modalidad }}</dd>
              </div>
              <div v-if="oferta.ubicacion" class="bg-emi-navy-50 rounded-lg p-3">
                <dt class="text-xs text-emi-navy-400 mb-0.5">Ubicación</dt>
                <dd class="text-sm font-semibold text-emi-navy-800">{{ oferta.ubicacion }}</dd>
              </div>
              <div v-if="oferta.area" class="bg-emi-navy-50 rounded-lg p-3">
                <dt class="text-xs text-emi-navy-400 mb-0.5">Área</dt>
                <dd class="text-sm font-semibold text-emi-navy-800">{{ oferta.area }}</dd>
              </div>
              <div v-if="oferta.fecha_inicio" class="bg-emi-navy-50 rounded-lg p-3">
                <dt class="text-xs text-emi-navy-400 mb-0.5">Fecha inicio</dt>
                <dd class="text-sm font-semibold text-emi-navy-800">{{ formatDate(oferta.fecha_inicio) }}</dd>
              </div>
              <div v-if="oferta.fecha_cierre" class="bg-emi-navy-50 rounded-lg p-3">
                <dt class="text-xs text-emi-navy-400 mb-0.5">Fecha cierre</dt>
                <dd class="text-sm font-semibold text-emi-navy-800">{{ formatDate(oferta.fecha_cierre) }}</dd>
              </div>
            </div>

            <!-- Contacto -->
            <div v-if="oferta.contact_email || oferta.contact_phone" class="mt-4 flex flex-wrap gap-4">
              <a v-if="oferta.contact_email"
                :href="'mailto:' + oferta.contact_email"
                class="inline-flex items-center gap-1.5 text-xs text-emi-navy-600 hover:underline">
                <svg class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                </svg>
                {{ oferta.contact_email }}
              </a>
              <span v-if="oferta.contact_phone" class="inline-flex items-center gap-1.5 text-xs text-gray-600">
                <svg class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                </svg>
                {{ oferta.contact_phone }}
              </span>
            </div>

            <!-- Requisitos -->
            <div v-if="oferta.requirements && hasRequisitos(oferta.requirements)"
              class="mt-4 pt-4 border-t border-emi-navy-100">
              <h4 class="text-xs font-semibold text-emi-navy-400 uppercase tracking-wider mb-3">Requisitos de la convocatoria</h4>
              <div class="space-y-2">
                <div v-if="oferta.requirements.required_education_level" class="flex gap-3">
                  <dt class="text-xs text-emi-navy-400 w-36 flex-shrink-0">Nivel educativo mín.</dt>
                  <dd class="text-xs font-medium text-emi-navy-800">{{ oferta.requirements.required_education_level }}</dd>
                </div>
                <div v-if="oferta.requirements.min_experience_years > 0" class="flex gap-3">
                  <dt class="text-xs text-emi-navy-400 w-36 flex-shrink-0">Experiencia mín.</dt>
                  <dd class="text-xs font-medium text-emi-navy-800">{{ oferta.requirements.min_experience_years }} año(s)</dd>
                </div>
                <div v-if="oferta.requirements.required_skills?.length > 0">
                  <dt class="text-xs text-emi-navy-400 mb-1.5">Habilidades requeridas</dt>
                  <div class="flex flex-wrap gap-1.5">
                    <span v-for="s in oferta.requirements.required_skills" :key="s"
                      class="px-2 py-0.5 bg-emi-navy-50 text-emi-navy-700 border border-emi-navy-200 rounded-full text-xs">
                      {{ s }}
                    </span>
                  </div>
                </div>
                <div v-if="oferta.requirements.preferred_skills?.length > 0">
                  <dt class="text-xs text-emi-navy-400 mb-1.5">Habilidades deseables</dt>
                  <div class="flex flex-wrap gap-1.5">
                    <span v-for="s in oferta.requirements.preferred_skills" :key="s"
                      class="px-2 py-0.5 bg-gray-100 text-gray-600 border border-gray-200 rounded-full text-xs">
                      {{ s }}
                    </span>
                  </div>
                </div>
                <div v-if="oferta.requirements.required_languages?.length > 0" class="flex gap-3">
                  <dt class="text-xs text-emi-navy-400 w-36 flex-shrink-0">Idiomas</dt>
                  <dd class="text-xs font-medium text-emi-navy-800">{{ oferta.requirements.required_languages.join(', ') }}</dd>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ═══════════════════════════════════════════════════════
             SECCIÓN 2: Control de top N + distribución
             ═══════════════════════════════════════════════════════ -->
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h2 class="text-lg font-bold text-emi-navy-500">Candidatos Evaluados</h2>
            <p class="text-sm text-gray-500 mt-0.5">
              Los {{ topN }} mejores candidatos ordenados por compatibilidad.
              Expande cada tarjeta para ver el desglose completo.
            </p>
          </div>

          <!-- Top N selector -->
          <div class="flex items-center gap-2">
            <span class="text-xs text-gray-500 whitespace-nowrap">Mostrar top:</span>
            <div class="flex gap-1">
              <button
                v-for="n in [3, 5, 10]"
                :key="n"
                @click="topN = n; loadRanking()"
                :class="[
                  'px-3 py-1.5 text-xs rounded-lg font-medium transition-colors',
                  topN === n
                    ? 'bg-emi-gold-500 text-white'
                    : 'bg-white text-gray-500 border border-emi-navy-200 hover:border-emi-gold-400'
                ]"
              >{{ n }}</button>
            </div>
          </div>
        </div>

        <!-- Distribución de candidatos -->
        <div v-if="rankingData?.total_postulantes > 0" class="grid grid-cols-3 gap-3">
          <div class="card-emi text-center py-3 bg-emi-gold-50 border-emi-gold-200">
            <span class="block text-2xl font-black text-emi-gold-600">{{ statsApto }}</span>
            <span class="text-xs font-semibold text-emi-gold-700 uppercase tracking-wide">APTO</span>
            <span class="block text-xs text-gray-400 mt-0.5">Candidatos</span>
          </div>
          <div class="card-emi text-center py-3 bg-emi-navy-50 border-emi-navy-200">
            <span class="block text-2xl font-black text-emi-navy-600">{{ statsConsiderado }}</span>
            <span class="text-xs font-semibold text-emi-navy-700 uppercase tracking-wide">CONSIDERADO</span>
            <span class="block text-xs text-gray-400 mt-0.5">Candidatos</span>
          </div>
          <div class="card-emi text-center py-3 bg-danger-50 border-danger-100">
            <span class="block text-2xl font-black text-danger-500">{{ statsNoApto }}</span>
            <span class="text-xs font-semibold text-danger-600 uppercase tracking-wide">NO APTO</span>
            <span class="block text-xs text-gray-400 mt-0.5">Candidatos</span>
          </div>
        </div>

        <!-- ═══════════════════════════════════════════════════════
             SECCIÓN 3: Cards de candidatos
             ═══════════════════════════════════════════════════════ -->

        <!-- Loading ranking -->
        <div v-if="loadingRanking" class="flex justify-center py-12">
          <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-emi-navy-500"></div>
        </div>

        <!-- Sin postulaciones -->
        <div v-else-if="!rankingData || rankingData.candidatos.length === 0"
          class="card-emi text-center py-12">
          <div class="w-12 h-12 bg-emi-navy-50 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg class="h-6 w-6 text-emi-navy-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
          </div>
          <p class="text-emi-navy-500 font-semibold">Sin postulaciones aún</p>
          <p class="text-xs text-gray-400 mt-1">Nadie se ha postulado a esta oferta todavía</p>
        </div>

        <!-- Cards de candidatos -->
        <div v-else class="space-y-4">
          <div
            v-for="candidato in rankingData.candidatos"
            :key="candidato.usuario_id"
            class="card-emi !p-0 overflow-hidden"
          >
            <!-- Header del candidato -->
            <div class="px-5 py-4">
              <div class="flex items-start gap-4">

                <!-- Rank badge -->
                <div :class="[
                  'flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center text-sm font-black shadow-sm',
                  candidato.rank === 1 ? 'bg-emi-gold-400 text-white' :
                  candidato.rank === 2 ? 'bg-emi-navy-200 text-emi-navy-700' :
                  candidato.rank === 3 ? 'bg-warning-500 text-white' :
                  'bg-emi-navy-100 text-emi-navy-700'
                ]">
                  #{{ candidato.rank }}
                </div>

                <!-- Info candidato -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 flex-wrap">
                    <h3 class="text-base font-bold text-emi-navy-800">
                      {{ candidato.perfil.nombre_completo }}
                    </h3>
                    <Badge
                      :variant="candidato.clasificacion === 'APTO' ? 'gold'
                        : candidato.clasificacion === 'CONSIDERADO' ? 'navy' : 'danger'"
                    >
                      {{ candidato.clasificacion }}
                    </Badge>
                    <span v-if="candidato.perfil.rol"
                      class="text-xs px-2 py-0.5 bg-emi-navy-100 text-emi-navy-600 rounded-full capitalize">
                      {{ candidato.perfil.rol }}
                    </span>
                  </div>
                  <div class="flex flex-wrap gap-3 mt-1 text-xs text-gray-400">
                    <span v-if="candidato.perfil.email">{{ candidato.perfil.email }}</span>
                    <span v-if="candidato.perfil.telefono">{{ candidato.perfil.telefono }}</span>
                    <span v-if="candidato.perfil.education_level">{{ candidato.perfil.education_level }}</span>
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
                    candidato.clasificacion === 'CONSIDERADO' ? 'text-emi-navy-600' : 'text-danger-500'
                  ]">
                    {{ Math.round(candidato.match_score * 100) }}%
                  </div>
                  <div class="text-xs text-gray-400 mt-0.5">compatibilidad</div>
                </div>
              </div>

              <!-- Barra de score -->
              <div class="mt-3">
                <ProgressBar :value="candidato.match_score * 100" :showLabel="false" size="sm" />
              </div>

              <!-- Tags fortalezas / debilidades -->
              <div v-if="candidato.fortalezas?.length || candidato.debilidades?.length"
                class="mt-3 flex flex-wrap gap-2">
                <span
                  v-for="f in candidato.fortalezas"
                  :key="f"
                  class="inline-flex items-center gap-1 px-2 py-0.5 bg-success-50 text-success-700 border border-success-100 rounded-full text-xs"
                >
                  <svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  {{ f }}
                </span>
                <span
                  v-for="d in candidato.debilidades"
                  :key="d"
                  class="inline-flex items-center gap-1 px-2 py-0.5 bg-danger-50 text-danger-600 border border-danger-100 rounded-full text-xs"
                >
                  <svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  {{ d }}
                </span>
              </div>
            </div>

            <!-- Footer con acciones -->
            <div class="px-5 py-2.5 bg-emi-navy-50 border-t border-emi-navy-100 flex items-center justify-between">
              <button
                @click="toggleExpand(candidato.usuario_id)"
                class="inline-flex items-center gap-1.5 text-sm text-emi-navy-600 hover:text-emi-navy-800 font-medium transition-colors"
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
                class="inline-flex items-center gap-1.5 text-xs text-emi-navy-500 hover:text-emi-navy-700 font-medium transition-colors"
              >
                <svg class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2"/>
                </svg>
                Ver perfil completo
              </router-link>
            </div>

            <!-- Panel expandible -->
            <div v-if="expandedId === candidato.usuario_id" class="px-5 py-4 border-t border-emi-navy-100 space-y-5">

              <!-- Perfil -->
              <div>
                <h4 class="text-xs font-semibold text-emi-navy-400 uppercase tracking-wider mb-1">Resumen del Perfil</h4>
                <p class="text-xs text-gray-400 mb-3">Datos de contacto y habilidades declaradas en el perfil del candidato.</p>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div v-if="candidato.perfil.hard_skills?.length > 0">
                    <p class="text-xs text-emi-navy-400 mb-1.5">Habilidades técnicas</p>
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
                    <p class="text-xs text-emi-navy-400 mb-1.5">Habilidades blandas</p>
                    <div class="flex flex-wrap gap-1.5">
                      <span v-for="s in candidato.perfil.soft_skills.slice(0, 6)" :key="s"
                        class="px-2 py-0.5 bg-gray-100 text-gray-600 border border-gray-200 rounded-full text-xs">
                        {{ s }}
                      </span>
                    </div>
                  </div>
                  <div v-if="candidato.perfil.languages?.length > 0">
                    <p class="text-xs text-emi-navy-400 mb-1">Idiomas</p>
                    <p class="text-xs text-emi-navy-800">{{ candidato.perfil.languages.join(', ') }}</p>
                  </div>
                  <div v-if="candidato.postulado_en">
                    <p class="text-xs text-emi-navy-400 mb-1">Fecha de postulación</p>
                    <p class="text-xs text-emi-navy-800">{{ formatDate(candidato.postulado_en) }}</p>
                  </div>
                </div>
              </div>

              <!-- Scores por dimensión -->
              <div v-if="candidato.scores_detalle && Object.keys(candidato.scores_detalle).length > 0">
                <h4 class="text-xs font-semibold text-emi-navy-400 uppercase tracking-wider mb-1">
                  Justificación del Score — Detalle por Dimensión
                </h4>
                <p class="text-xs text-gray-400 mb-3">
                  Puntaje obtenido en cada dimensión. El global es la suma ponderada de estas dimensiones.
                </p>
                <div class="space-y-2.5">
                  <div v-for="(value, key) in candidato.scores_detalle" :key="key">
                    <ProgressBar :value="value * 100" :label="formatScoreLabel(key)" size="md" />
                  </div>
                </div>
              </div>

              <!-- Match detail -->
              <MatchDetailSection
                v-if="candidato.match_details"
                :matchDetails="candidato.match_details"
                :clasificacion="candidato.clasificacion"
              />
            </div>
          </div>
        </div>

      </template>

    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '@/shared/components/AppLayout.vue'
import Badge from '@/shared/components/ui/Badge.vue'
import ProgressBar from '@/shared/components/ui/ProgressBar.vue'
import MatchDetailSection from '@/features/recommendations/components/MatchDetailSection.vue'
import { getOfertasConStats, getRankingCandidatos, generarInforme } from '../api/ranking.api'

const route = useRoute()
const router = useRouter()

const ofertaId = computed(() => route.params.id)

// ── Estado ─────────────────────────────────────────────
const oferta = ref(null)
const rankingData = ref(null)
const loadingOferta = ref(true)
const loadingRanking = ref(false)
const errorOferta = ref(null)
const expandedId = ref(null)
const generandoPdf = ref(false)
const topN = ref(5)

// ── Computed stats ─────────────────────────────────────
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

// ── Carga de datos ─────────────────────────────────────
const loadOferta = async () => {
  loadingOferta.value = true
  errorOferta.value = null
  try {
    // Obtenemos la lista completa y filtramos por ID
    const data = await getOfertasConStats({ include_expired: true })
    oferta.value = (data.ofertas || []).find(o => o.id === ofertaId.value) ?? null
    if (!oferta.value) {
      errorOferta.value = 'La oferta no fue encontrada.'
      return
    }
    await loadRanking()
  } catch (e) {
    console.error('Error cargando oferta:', e)
    errorOferta.value = 'No se pudo cargar la información de la oferta.'
  } finally {
    loadingOferta.value = false
  }
}

const loadRanking = async () => {
  loadingRanking.value = true
  try {
    rankingData.value = await getRankingCandidatos(ofertaId.value, topN.value)
  } catch (e) {
    console.error('Error cargando evaluacion:', e)
  } finally {
    loadingRanking.value = false
  }
}

const handleGenerarInforme = async () => {
  if (generandoPdf.value) return
  generandoPdf.value = true
  try {
    const titulo = (oferta.value?.titulo || 'informe').slice(0, 30).replace(/\s+/g, '-').toLowerCase()
    await generarInforme(ofertaId.value, topN.value, `informe-evaluacion-${titulo}.pdf`)
  } catch (e) {
    console.error('Error generando informe:', e)
  } finally {
    generandoPdf.value = false
  }
}

onMounted(loadOferta)
</script>
