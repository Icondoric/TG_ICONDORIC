<template>
  <AppLayout :menuItems="studentMenuItems" variant="light">
    <div class="flex">
      <!-- Secondary Sidebar -->
      <RecommendationsSidebar
        v-model:isOpen="isSecondarySidebarOpen"
        :bestMatch="bestMatch"
        :perfilSummary="perfilSummary"
        :totalCount="recommendations.length"
        :newCount="newCount"
        :aptoCount="aptoCount"
        :consideradoCount="consideradoCount"
        :refreshing="refreshing"
        @refresh="loadRecommendations(true)"
      />

      <!-- Main Content -->
      <div
        class="flex-1 transition-[margin] duration-300 ease-in-out min-h-screen"
        :style="{ marginLeft: isSecondarySidebarOpen ? '280px' : '60px' }"
      >
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <!-- Header -->
          <div class="mb-8">
            <h1 class="text-3xl font-bold text-emi-navy-500">Mis Recomendaciones</h1>
            <p class="mt-2 text-gray-600">
              {{ userRole === 'estudiante' ? 'Pasantias recomendadas' : 'Empleos recomendados' }} basados en tu perfil
            </p>
          </div>

          <!-- Loading -->
          <div v-if="loading" class="flex justify-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emi-navy-500"></div>
          </div>

          <!-- Not Eligible -->
          <EligibilityWarning
            v-else-if="!isEligible"
            :reason="eligibilityReason"
            :action="eligibilityAction"
            :missingFields="missingFields"
          />

          <!-- Error -->
          <Card v-else-if="error" class="border-red-200 bg-red-50">
            <p class="text-red-700">{{ error }}</p>
            <button @click="loadRecommendations" class="mt-2 text-red-600 hover:text-red-800 underline">
              Reintentar
            </button>
          </Card>

          <!-- Results -->
          <div v-else>
            <!-- Mobile Stats Bar -->
            <Card class="lg:hidden mb-6">
              <div class="flex items-center justify-between">
                <div>
                  <span class="text-2xl font-bold text-emi-navy-500">{{ recommendations.length }}</span>
                  <span class="text-gray-500 ml-1">recomendaciones</span>
                </div>
                <div v-if="newCount > 0">
                  <Badge variant="gold">{{ newCount }} nuevas</Badge>
                </div>
              </div>
              <div class="mt-4 flex gap-2">
                <button
                  @click="loadRecommendations(true)"
                  :disabled="refreshing"
                  class="flex-1 flex items-center justify-center gap-2 btn-emi-primary text-sm"
                >
                  <svg :class="['h-4 w-4', refreshing ? 'animate-spin' : '']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  {{ refreshing ? 'Actualizando...' : 'Actualizar' }}
                </button>
              </div>
            </Card>

            <!-- No Recommendations -->
            <Card v-if="recommendations.length === 0" class="text-center py-12">
              <svg class="mx-auto h-16 w-16 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <h3 class="mt-4 text-lg font-semibold text-gray-900">No hay recomendaciones disponibles</h3>
              <p class="mt-2 text-gray-500">
                No hay {{ userRole === 'estudiante' ? 'pasantias' : 'empleos' }} activos en este momento.
              </p>
              <div class="mt-4 space-y-2">
                <p class="text-sm text-gray-400">Posibles razones:</p>
                <ul class="text-sm text-gray-400 list-disc list-inside">
                  <li>No hay ofertas publicadas para tu perfil</li>
                  <li>Tu perfil necesita mas informacion</li>
                  <li>El sistema esta procesando las ofertas</li>
                </ul>
              </div>
              <div class="mt-6 flex justify-center gap-4">
                <router-link
                  to="/mi-perfil"
                  class="inline-flex items-center gap-2 px-4 py-2 border border-emi-navy-300 text-emi-navy-600 rounded-lg hover:bg-emi-navy-50 transition-colors"
                >
                  Revisar Mi Perfil
                </router-link>
                <button @click="loadRecommendations(true)" class="btn-emi-primary">
                  Reintentar
                </button>
              </div>
            </Card>

            <!-- Recommendations List -->
            <div v-else class="space-y-4">
              <RecommendationCard
                v-for="rec in recommendations"
                :key="rec.id"
                :rec="rec"
                :expanded="expandedId === rec.id"
                :formatScoreLabel="formatScoreLabel"
                :formatDate="formatDate"
                @toggle="toggleExpand"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref } from 'vue'
import { studentMenuItems } from '@/shared/constants/navigation'
import AppLayout from '@/shared/components/AppLayout.vue'
import Card from '@/shared/components/ui/Card.vue'
import Badge from '@/shared/components/ui/Badge.vue'
import RecommendationsSidebar from '../components/RecommendationsSidebar.vue'
import RecommendationCard from '../components/RecommendationCard.vue'
import EligibilityWarning from '../components/EligibilityWarning.vue'
import { useRecommendations } from '../composables/useRecommendations'

const isSecondarySidebarOpen = ref(true)

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
  expandedId,
  userRole,
  newCount,
  aptoCount,
  consideradoCount,
  bestMatch,
  formatScoreLabel,
  formatDate,
  toggleExpand,
  loadRecommendations
} = useRecommendations()
</script>
