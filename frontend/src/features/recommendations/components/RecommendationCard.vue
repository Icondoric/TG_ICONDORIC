<template>
  <Card :hoverable="true" class="overflow-visible">
    <!-- Main Card Content -->
    <div class="flex items-start justify-between">
      <div class="flex-1">
        <!-- Badges Row -->
        <div class="flex items-center gap-2 mb-3">
          <Badge
            :variant="rec.clasificacion === 'APTO' ? 'gold' : rec.clasificacion === 'CONSIDERADO' ? 'navy' : 'danger'"
          >
            {{ rec.clasificacion }}
          </Badge>
          <Badge v-if="!rec.fue_vista" variant="navy" size="sm">
            Nueva
          </Badge>
        </div>

        <!-- Title -->
        <h3 class="text-lg font-semibold text-gray-900">{{ rec.oferta?.titulo }}</h3>

        <!-- Meta Info -->
        <div class="flex flex-wrap items-center gap-4 mt-2 text-sm text-gray-600">
          <span v-if="rec.oferta?.institution_name" class="flex items-center gap-1">
            <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            {{ rec.oferta.institution_name }}
          </span>
          <span v-if="rec.oferta?.sector" class="text-gray-400">
            {{ rec.oferta.sector }}
          </span>
          <span v-if="rec.oferta?.modalidad" class="flex items-center gap-1">
            <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            </svg>
            {{ rec.oferta.modalidad }}
          </span>
        </div>
      </div>

      <!-- Match Score Circle -->
      <div class="ml-4 flex-shrink-0">
        <div
          :class="[
            'w-16 h-16 rounded-full flex items-center justify-center text-xl font-bold border-4',
            rec.match_score >= 0.7
              ? 'bg-emi-gold-50 text-emi-gold-600 border-emi-gold-200'
              : rec.match_score >= 0.5
                ? 'bg-emi-navy-50 text-emi-navy-600 border-emi-navy-200'
                : 'bg-red-50 text-red-600 border-red-200'
          ]"
        >
          {{ Math.round(rec.match_score * 100) }}%
        </div>
        <p class="text-xs text-gray-500 text-center mt-1">Match</p>
      </div>
    </div>

    <!-- Description -->
    <p v-if="rec.oferta?.descripcion" class="mt-4 text-gray-600 text-sm line-clamp-2">
      {{ rec.oferta.descripcion }}
    </p>

    <!-- Strengths & Weaknesses -->
    <div class="mt-4 flex flex-wrap gap-4">
      <div v-if="rec.fortalezas?.length > 0">
        <span class="text-xs text-gray-500">Fortalezas:</span>
        <div class="flex flex-wrap gap-1 mt-1">
          <Badge v-for="f in rec.fortalezas.slice(0, 2)" :key="f" variant="gold" size="sm">
            {{ f }}
          </Badge>
        </div>
      </div>
      <div v-if="rec.debilidades?.length > 0">
        <span class="text-xs text-gray-500">Areas de mejora:</span>
        <div class="flex flex-wrap gap-1 mt-1">
          <Badge v-for="d in rec.debilidades.slice(0, 2)" :key="d" variant="neutral" size="sm">
            {{ d }}
          </Badge>
        </div>
      </div>
    </div>

    <!-- Expand Button -->
    <button
      @click="$emit('toggle', rec.id)"
      class="mt-4 text-emi-navy-500 hover:text-emi-gold-500 text-sm font-medium flex items-center transition-colors"
    >
      {{ expanded ? 'Ver menos' : 'Ver detalles' }}
      <svg :class="['h-4 w-4 ml-1 transition-transform', expanded ? 'rotate-180' : '']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- Expanded Details -->
    <div v-if="expanded" class="mt-4 pt-4 border-t border-gray-100">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Left: Scores -->
        <div>
          <h4 class="font-semibold text-gray-900 mb-3">Detalle de Scores</h4>
          <div class="space-y-3">
            <div v-for="(value, key) in rec.scores_detalle" :key="key">
              <ProgressBar
                :value="value * 100"
                :label="formatScoreLabel(key)"
              />
            </div>
          </div>
        </div>

        <!-- Right: Oferta Details -->
        <div>
          <h4 class="font-semibold text-gray-900 mb-3">Detalles de la Oferta</h4>
          <dl class="space-y-2 text-sm">
            <div v-if="rec.oferta?.tipo" class="flex">
              <dt class="text-gray-500 w-24">Tipo:</dt>
              <dd class="text-gray-900 capitalize">{{ rec.oferta.tipo }}</dd>
            </div>
            <div v-if="rec.oferta?.ubicacion" class="flex">
              <dt class="text-gray-500 w-24">Ubicacion:</dt>
              <dd class="text-gray-900">{{ rec.oferta.ubicacion }}</dd>
            </div>
            <div v-if="rec.oferta?.cupos_disponibles" class="flex">
              <dt class="text-gray-500 w-24">Cupos:</dt>
              <dd class="text-gray-900">{{ rec.oferta.cupos_disponibles }}</dd>
            </div>
            <div v-if="rec.oferta?.fecha_cierre" class="flex">
              <dt class="text-gray-500 w-24">Cierre:</dt>
              <dd class="text-gray-900">{{ formatDate(rec.oferta.fecha_cierre) }}</dd>
            </div>
          </dl>
        </div>
      </div>

      <!-- Action Note -->
      <div class="mt-6 p-4 bg-emi-navy-50 rounded-xl">
        <p class="text-sm text-emi-navy-700">
          <strong>Nota:</strong> Para postular a esta oferta, contacta a la Unidad de Vinculacion de la EMI.
          Este sistema solo genera recomendaciones de correspondencia.
        </p>
      </div>
    </div>
  </Card>
</template>

<script setup>
import Card from '@/shared/components/ui/Card.vue'
import Badge from '@/shared/components/ui/Badge.vue'
import ProgressBar from '@/shared/components/ui/ProgressBar.vue'

defineProps({
  rec: { type: Object, required: true },
  expanded: { type: Boolean, default: false },
  formatScoreLabel: { type: Function, required: true },
  formatDate: { type: Function, required: true }
})

defineEmits(['toggle'])
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
