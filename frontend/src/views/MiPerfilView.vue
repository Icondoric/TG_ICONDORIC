<template>
  <StudentLayout>
    <div class="flex">
      <!-- Secondary Sidebar -->
      <CollapsibleSidebar 
        v-model:isOpen="isSecondarySidebarOpen" 
        width="280px" 
        collapsedWidth="60px" 
        persistenceKey="studentProfileSidebar"
        :leftOffset="uiStore.isSidebarOpen ? '256px' : '80px'"
      >
        <!-- Expanded Content -->
        <div class="p-4 space-y-6">

          <!-- Gauge Chart -->
          <div class="text-center">
            <GaugeChart
              :value="Math.round(profile.completeness_score * 100)"
              size="md"
              label="Completitud"
            />
            <div class="mt-2">
              <Badge :variant="profile.is_complete ? 'gold' : 'danger'" size="sm">
                {{ profile.is_complete ? 'Completo' : 'Incompleto' }}
              </Badge>
            </div>
          </div>

          <!-- Stats Grid -->
          <div class="grid grid-cols-2 gap-2">
            <div class="p-2 bg-emi-navy-50 rounded-lg text-center">
              <span class="block text-lg font-bold text-emi-navy-600">{{ profile.hard_skills.length }}</span>
              <span class="text-xs text-gray-500">Skills</span>
            </div>
            <div class="p-2 bg-emi-gold-50 rounded-lg text-center">
              <span class="block text-lg font-bold text-emi-gold-600">{{ profile.soft_skills.length }}</span>
              <span class="text-xs text-gray-500">Soft</span>
            </div>
            <div class="p-2 bg-purple-50 rounded-lg text-center">
              <span class="block text-lg font-bold text-purple-600">{{ profile.languages.length }}</span>
              <span class="text-xs text-gray-500">Idiomas</span>
            </div>
             <div class="p-2 bg-green-50 rounded-lg text-center">
              <span class="block text-lg font-bold text-green-600">{{ profile.experience_years }}</span>
              <span class="text-xs text-gray-500">Años</span>
            </div>
          </div>

          <!-- Actions -->
           <div class="space-y-2 pt-4 border-t border-gray-100">
             <button 
                @click="loadProfile" 
                class="w-full flex items-center justify-center gap-2 px-3 py-2 text-sm text-emi-navy-600 bg-emi-navy-50 hover:bg-emi-navy-100 rounded-lg transition-colors"
                title="Actualizar datos"
             >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                   <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Actualizar
             </button>
             <router-link 
                to="/mis-recomendaciones"
                class="w-full flex items-center justify-center gap-2 px-3 py-2 text-sm text-white bg-emi-navy-500 hover:bg-emi-navy-600 rounded-lg transition-colors shadow-sm"
             >
                 Ver Recomendaciones
             </router-link>
           </div>
        </div>

        <!-- Collapsed Icons -->
        <template #collapsed>
            <div class="space-y-6 flex flex-col items-center w-full px-2">
                <div class="w-10 h-10 bg-emi-navy-100 rounded-full flex items-center justify-center text-lg font-bold text-emi-navy-600" title="Perfil">
                    {{ profile.names ? profile.names.charAt(0) : 'U' }}
                </div>
                
                <div class="text-center" :title="`Completitud: ${Math.round(profile.completeness_score * 100)}%`">
                     <div class="relative w-10 h-10 flex items-center justify-center">
                         <svg class="w-full h-full transform -rotate-90">
                             <circle cx="20" cy="20" r="16" fill="transparent" stroke="#e2e8f0" stroke-width="4"></circle>
                             <circle cx="20" cy="20" r="16" fill="transparent" :stroke="profile.is_complete ? '#10b981' : '#f59e0b'" stroke-width="4" 
                                :stroke-dasharray="100" :stroke-dashoffset="100 - (profile.completeness_score * 100)"></circle>
                         </svg>
                         <span class="absolute text-[10px] font-bold">{{ Math.round(profile.completeness_score * 100) }}</span>
                     </div>
                </div>

                <div class="flex flex-col gap-3 w-full border-t border-gray-100 pt-4">
                     <div class="flex flex-col items-center" title="Skills Técnicas">
                        <span class="text-xs font-bold text-emi-navy-600">{{ profile.hard_skills.length }}</span>
                        <div class="w-1 h-1 rounded-full bg-emi-navy-500 mt-0.5"></div>
                     </div>
                     <div class="flex flex-col items-center" title="Skills Blandas">
                        <span class="text-xs font-bold text-emi-gold-600">{{ profile.soft_skills.length }}</span>
                        <div class="w-1 h-1 rounded-full bg-emi-gold-500 mt-0.5"></div>
                     </div>
                </div>
            </div>
        </template>
      </CollapsibleSidebar>

      <!-- Main Content Container with Dynamic Margin -->
      <div 
        class="flex-1 transition-[margin] duration-300 ease-in-out min-h-screen"
        :style="{ marginLeft: isSecondarySidebarOpen ? '280px' : '60px' }"
      >
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <!-- Header -->
          <div class="mb-8">
            <h1 class="text-3xl font-bold text-emi-navy-500">Digitalización de Perfiles</h1>
            <p class="mt-2 text-gray-600">
              Sube tu CV para extraer automáticamente tus competencias y experiencia profesional
            </p>
          </div>

          <!-- CV Upload/Update Section -->
          <Card class="mb-6 border-2 border-emi-gold-200 bg-gradient-to-br from-emi-gold-50 to-white">
            <div class="flex items-start gap-4">
              <div class="p-3 bg-emi-gold-500 rounded-xl shadow-md">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div class="flex-1">
                <h2 class="text-xl font-bold text-gray-900 mb-2">
                  {{ profile.cv_filename ? 'CV Cargado' : 'Sube tu Curriculum Vitae' }}
                </h2>
                
                <!-- CV Info if exists -->
                <div v-if="profile.cv_filename" class="mb-4 p-4 bg-white rounded-lg border border-emi-gold-200">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                      <div class="p-2 bg-emi-navy-100 rounded-lg">
                        <svg class="h-6 w-6 text-emi-navy-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                      <div>
                        <p class="font-semibold text-gray-900">{{ profile.cv_filename }}</p>
                        <p class="text-sm text-gray-500">Subido {{ formatDate(profile.cv_uploaded_at) }}</p>
                      </div>
                    </div>
                    <Badge variant="gold">
                      <svg class="w-4 h-4 mr-1 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                      </svg>
                      Procesado
                    </Badge>
                  </div>
                </div>

                <!-- Upload Instructions -->
                <p class="text-gray-600 mb-4">
                  {{ profile.cv_filename 
                    ? 'Actualiza tu CV para refrescar la información extraída de tu perfil profesional.' 
                    : 'Nuestro sistema de IA extraerá automáticamente tus competencias, formación y experiencia laboral.' 
                  }}
                </p>

                <!-- Action Buttons -->
                <div class="flex flex-wrap gap-3">
                  <button
                    @click="showUploadModal = true"
                    class="inline-flex items-center gap-2 px-6 py-3 bg-emi-gold-500 text-emi-navy-800 rounded-lg font-semibold hover:bg-emi-gold-400 transition-all hover:shadow-lg hover:-translate-y-0.5"
                  >
                    <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                    </svg>
                    {{ profile.cv_filename ? 'Actualizar CV' : 'Subir CV (PDF)' }}
                  </button>
                  
                  <button
                    v-if="profile.cv_filename"
                    @click="showDeleteConfirm = true"
                    class="inline-flex items-center gap-2 px-6 py-3 border-2 border-red-300 text-red-700 rounded-lg font-semibold hover:bg-red-50 transition-colors"
                  >
                    <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    Limpiar Perfil
                  </button>
                </div>
              </div>
            </div>
          </Card>

          <!-- Loading -->
          <div v-if="loading" class="flex justify-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emi-navy-500"></div>
          </div>

          <!-- Error -->
          <Card v-else-if="error" class="border-red-200 bg-red-50">
            <p class="text-red-700">{{ error }}</p>
            <button @click="loadProfile" class="mt-2 text-red-600 hover:text-red-800 underline">
              Reintentar
            </button>
          </Card>

          <!-- Content -->
          <div v-else class="space-y-6">
            <!-- Mobile Score Card (visible only on mobile) -->
            <Card class="lg:hidden">
              <div class="flex items-center justify-between">
                <div>
                  <h2 class="text-lg font-semibold text-gray-900">Estado del Perfil</h2>
                  <Badge :variant="profile.is_complete ? 'gold' : 'danger'" class="mt-2">
                    {{ profile.is_complete ? 'Completo' : 'Incompleto' }}
                  </Badge>
                </div>
                <GaugeChart
                  :value="Math.round(profile.completeness_score * 100)"
                  size="sm"
                />
              </div>

              <!-- Progress Bar for mobile -->
              <div class="mt-4">
                <ProgressBar
                  :value="profile.completeness_score * 100"
                  label="Completitud del perfil"
                />
              </div>

              <!-- Mobile Upload Button -->
              <button
                @click="showUploadModal = true"
                class="mt-4 w-full flex items-center justify-center gap-2 btn-emi-primary"
              >
                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
                {{ profile.cv_filename ? 'Actualizar CV' : 'Subir CV' }}
              </button>
            </Card>

            <!-- Missing Fields -->
            <Card v-if="completeness && completeness.missing_fields.length > 0" class="border-emi-gold-200 bg-emi-gold-50">
              <div class="flex items-start gap-3">
                <div class="p-2 bg-emi-gold-100 rounded-full">
                  <svg class="w-5 h-5 text-emi-gold-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h3 class="font-semibold text-emi-gold-800">Para mejorar tu perfil:</h3>
                  <ul class="mt-2 list-disc list-inside text-sm text-emi-gold-700 space-y-1">
                    <li v-for="rec in completeness.recommendations" :key="rec">{{ rec }}</li>
                  </ul>
                </div>
              </div>
            </Card>

            <!-- CV Info Card -->
            <Card v-if="profile.cv_filename" title="Documento CV">
              <div class="flex items-center text-gray-600">
                <div class="p-2 bg-emi-navy-100 rounded-lg mr-3">
                  <svg class="h-6 w-6 text-emi-navy-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div>
                  <p class="font-medium text-gray-900">{{ profile.cv_filename }}</p>
                  <p class="text-sm text-gray-500">
                    Subido {{ formatDate(profile.cv_uploaded_at) }}
                  </p>
                </div>
              </div>
            </Card>

            <!-- Digitalization Summary Card -->
            <Card v-if="hasGeminiData" title="Datos Extraidos del CV (Digitalizacion)">
              <div class="space-y-4">
                <!-- Personal Info / Summary -->
                <div v-if="geminiPersonalInfo?.summary">
                  <h4 class="text-sm font-semibold text-gray-700 mb-2">Resumen Profesional</h4>
                  <p class="text-sm text-gray-600 bg-gray-50 p-3 rounded-lg">{{ geminiPersonalInfo.summary }}</p>
                </div>

                <!-- Detected Names -->
                <div v-if="geminiPersonalInfo?.detected_names?.length > 0">
                  <h4 class="text-sm font-semibold text-gray-700 mb-2">Nombres Detectados</h4>
                  <div class="flex flex-wrap gap-2">
                    <Badge v-for="name in geminiPersonalInfo.detected_names" :key="name" variant="neutral">
                      {{ name }}
                    </Badge>
                  </div>
                </div>

                <!-- Contact Info -->
                <div v-if="geminiPersonalInfo?.email || geminiPersonalInfo?.phone" class="grid grid-cols-2 gap-4">
                  <div v-if="geminiPersonalInfo?.email">
                    <h4 class="text-sm font-semibold text-gray-700 mb-1">Email Detectado</h4>
                    <p class="text-sm text-gray-600">{{ geminiPersonalInfo.email }}</p>
                  </div>
                  <div v-if="geminiPersonalInfo?.phone">
                    <h4 class="text-sm font-semibold text-gray-700 mb-1">Telefono Detectado</h4>
                    <p class="text-sm text-gray-600">{{ geminiPersonalInfo.phone }}</p>
                  </div>
                </div>

                <!-- Extraction Stats -->
                <div class="grid grid-cols-2 md:grid-cols-4 gap-3 pt-3 border-t border-gray-100">
                  <div class="text-center p-2 bg-emi-navy-50 rounded-lg">
                    <p class="text-xl font-bold text-emi-navy-600">{{ profile.hard_skills?.length || 0 }}</p>
                    <p class="text-xs text-gray-500">Skills Tecnicos</p>
                  </div>
                  <div class="text-center p-2 bg-emi-gold-50 rounded-lg">
                    <p class="text-xl font-bold text-emi-gold-600">{{ profile.soft_skills?.length || 0 }}</p>
                    <p class="text-xs text-gray-500">Skills Blandos</p>
                  </div>
                  <div class="text-center p-2 bg-green-50 rounded-lg">
                    <p class="text-xl font-bold text-green-600">{{ geminiEducation?.length || 0 }}</p>
                    <p class="text-xs text-gray-500">Formacion</p>
                  </div>
                  <div class="text-center p-2 bg-purple-50 rounded-lg">
                    <p class="text-xl font-bold text-purple-600">{{ geminiExperience?.length || 0 }}</p>
                    <p class="text-xs text-gray-500">Experiencias</p>
                  </div>
                </div>
              </div>
            </Card>

            <!-- No CV Message -->
            <Card v-if="!profile.cv_filename" class="border-emi-gold-200 bg-emi-gold-50">
              <div class="flex items-start gap-4">
                <div class="p-3 bg-emi-gold-100 rounded-full">
                  <svg class="h-6 w-6 text-emi-gold-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div class="flex-1">
                  <h3 class="text-lg font-semibold text-emi-gold-800">Sube tu CV para comenzar</h3>
                  <p class="mt-1 text-emi-gold-700">
                    Nuestro sistema extraera automaticamente tus competencias, formacion y experiencia.
                  </p>
                  <button
                    @click="showUploadModal = true"
                    class="mt-4 btn-emi-primary"
                  >
                    Subir CV ahora
                  </button>
                </div>
              </div>
            </Card>

            <!-- Competencias Section -->
            <Card id="competencias">
              <div class="flex items-center justify-between mb-4">
                <h2 class="text-lg font-semibold text-gray-900">Competencias</h2>
                <button
                  @click="openEditModal('skills')"
                  class="flex items-center gap-1 text-sm text-emi-navy-500 hover:text-emi-gold-500 transition-colors"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                  Editar
                </button>
              </div>

              <!-- Hard Skills -->
              <div class="mb-6">
                <h3 class="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                  <span class="w-2 h-2 bg-emi-navy-500 rounded-full"></span>
                  Habilidades Tecnicas
                </h3>
                <div class="flex flex-wrap gap-2">
                  <Badge
                    v-for="skill in profile.hard_skills"
                    :key="skill"
                    variant="navy"
                  >
                    {{ skill }}
                  </Badge>
                  <span v-if="profile.hard_skills.length === 0" class="text-gray-400 text-sm">
                    No hay habilidades registradas -
                    <button @click="openEditModal('skills')" class="text-emi-navy-500 hover:underline">Agregar</button>
                  </span>
                </div>
              </div>

              <!-- Soft Skills -->
              <div class="mb-6">
                <h3 class="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                  <span class="w-2 h-2 bg-emi-gold-500 rounded-full"></span>
                  Habilidades Blandas
                </h3>
                <div class="flex flex-wrap gap-2">
                  <Badge
                    v-for="skill in profile.soft_skills"
                    :key="skill"
                    variant="gold"
                  >
                    {{ skill }}
                  </Badge>
                  <span v-if="profile.soft_skills.length === 0" class="text-gray-400 text-sm">
                    No hay habilidades registradas -
                    <button @click="openEditModal('skills')" class="text-emi-navy-500 hover:underline">Agregar</button>
                  </span>
                </div>
              </div>

              <!-- Languages -->
              <div>
                <h3 class="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                  <span class="w-2 h-2 bg-gray-400 rounded-full"></span>
                  Idiomas
                </h3>
                <div class="flex flex-wrap gap-2">
                  <Badge
                    v-for="lang in profile.languages"
                    :key="lang"
                    variant="neutral"
                  >
                    {{ lang }}
                  </Badge>
                  <span v-if="profile.languages.length === 0" class="text-gray-400 text-sm">
                    No hay idiomas registrados -
                    <button @click="openEditModal('skills')" class="text-emi-navy-500 hover:underline">Agregar</button>
                  </span>
                </div>
              </div>
            </Card>

            <!-- Education & Experience Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Education -->
              <Card id="formacion">
                <div class="flex items-center justify-between mb-4">
                  <h2 class="text-lg font-semibold text-gray-900">Formacion Academica</h2>
                  <button
                    @click="openEditModal('education')"
                    class="flex items-center gap-1 text-sm text-emi-navy-500 hover:text-emi-gold-500 transition-colors"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                    Editar
                  </button>
                </div>

                <div v-if="profile.education_level" class="flex items-center mb-4">
                  <div class="p-3 bg-emi-navy-100 rounded-xl mr-4">
                    <svg class="h-8 w-8 text-emi-navy-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path d="M12 14l9-5-9-5-9 5 9 5z" />
                      <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                    </svg>
                  </div>
                  <div>
                    <p class="font-semibold text-gray-900">{{ profile.education_level }}</p>
                    <p class="text-sm text-gray-500">Nivel educativo mas alto</p>
                  </div>
                </div>
                <p v-else class="text-gray-400 text-sm">
                  No hay formacion registrada -
                  <button @click="openEditModal('education')" class="text-emi-navy-500 hover:underline">Agregar</button>
                </p>

                <!-- Education Details from Gemini -->
                <div v-if="geminiEducation.length > 0" class="mt-4 pt-4 border-t border-gray-100 space-y-3">
                  <div v-for="(edu, index) in geminiEducation" :key="index" class="p-3 bg-gray-50 rounded-lg">
                    <p class="font-medium text-gray-800">{{ edu.degree }}</p>
                    <p class="text-sm text-gray-600">{{ edu.institution }}</p>
                    <p v-if="edu.year" class="text-xs text-gray-400 mt-1">{{ edu.year }}</p>
                  </div>
                </div>
              </Card>

              <!-- Experience -->
              <Card id="experiencia">
                <div class="flex items-center justify-between mb-4">
                  <h2 class="text-lg font-semibold text-gray-900">Experiencia Laboral</h2>
                  <button
                    @click="openEditModal('experience')"
                    class="flex items-center gap-1 text-sm text-emi-navy-500 hover:text-emi-gold-500 transition-colors"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                    Editar
                  </button>
                </div>

                <div class="flex items-center mb-4">
                  <div class="p-3 bg-emi-gold-100 rounded-xl mr-4">
                    <svg class="h-8 w-8 text-emi-gold-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <p class="font-semibold text-gray-900">{{ profile.experience_years }} anos</p>
                    <p class="text-sm text-gray-500">Experiencia total</p>
                  </div>
                </div>

                <!-- Experience Details from Gemini -->
                <div v-if="geminiExperience.length > 0" class="mt-4 pt-4 border-t border-gray-100 space-y-3">
                  <div v-for="(exp, index) in geminiExperience" :key="index" class="p-3 bg-gray-50 rounded-lg">
                    <p class="font-medium text-gray-800">{{ exp.role }}</p>
                    <p class="text-sm text-gray-600">{{ exp.company }}</p>
                    <p v-if="exp.duration" class="text-xs text-gray-400 mt-1">{{ exp.duration }}</p>
                  </div>
                </div>
                <p v-else-if="geminiExperience.length === 0 && profile.experience_years === 0" class="text-gray-400 text-sm">
                  No hay experiencia registrada -
                  <button @click="openEditModal('experience')" class="text-emi-navy-500 hover:underline">Agregar</button>
                </p>
              </Card>
            </div>

            <!-- Actions Card -->
            <Card title="Acciones">
              <div class="flex flex-wrap gap-4">
                <router-link
                  to="/mis-recomendaciones"
                  class="inline-flex items-center gap-2 btn-emi-secondary"
                  :class="{ 'opacity-50 cursor-not-allowed': !profile.is_complete }"
                >
                  <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                  </svg>
                  Ver Recomendaciones
                </router-link>

                <button
                  @click="showDeleteConfirm = true"
                  class="inline-flex items-center gap-2 px-4 py-2 border border-red-300 rounded-lg text-red-700 bg-white hover:bg-red-50 transition-colors"
                >
                  <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  Limpiar Perfil
                </button>
              </div>
            </Card>
          </div>
        </div>

    <!-- Upload CV Modal -->
    <div v-if="showUploadModal" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50 p-4">
      <Card class="w-full max-w-lg" :hoverable="false">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Subir CV</h3>
          <button @click="showUploadModal = false; uploadFile = null" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleDrop"
          :class="[
            'border-2 border-dashed rounded-lg p-8 text-center transition-colors cursor-pointer',
            isDragging ? 'border-emi-gold-500 bg-emi-gold-50' : 'border-gray-300 hover:border-emi-navy-400'
          ]"
          @click="$refs.fileInput.click()"
        >
          <template v-if="!uploadFile">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p class="mt-2 text-gray-600">Arrastra tu CV aqui o <span class="text-emi-navy-500 font-medium">selecciona un archivo</span></p>
            <p class="mt-1 text-sm text-gray-500">Solo archivos PDF (max. 10MB)</p>
          </template>
          <template v-else>
            <svg class="mx-auto h-12 w-12 text-emi-gold-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="mt-2 font-medium text-gray-900">{{ uploadFile.name }}</p>
            <p class="mt-1 text-sm text-gray-500">{{ formatFileSize(uploadFile.size) }}</p>
          </template>
        </div>
        <input ref="fileInput" type="file" accept=".pdf" @change="handleFileSelect" class="hidden" />

        <div class="mt-4 flex justify-end gap-3">
          <button
            @click="showUploadModal = false; uploadFile = null"
            class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
          >
            Cancelar
          </button>
          <button
            @click="processCV"
            :disabled="!uploadFile || uploading"
            class="btn-emi-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ uploading ? 'Procesando...' : 'Procesar CV' }}
          </button>
        </div>
      </Card>
    </div>

    <!-- Edit Modal -->
    <div v-if="editModal.show" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50 p-4">
      <Card class="w-full max-w-2xl max-h-[90vh] overflow-y-auto" :hoverable="false">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">{{ editModal.title }}</h3>
          <button @click="closeEditModal" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Skills Edit -->
        <div v-if="editModal.type === 'skills'" class="space-y-6">
          <!-- Hard Skills -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Habilidades Tecnicas</label>
            <div class="flex flex-wrap gap-2 mb-2">
              <Badge v-for="(skill, index) in editForm.hard_skills" :key="skill" variant="navy">
                {{ skill }}
                <button @click="removeSkill('hard_skills', index)" class="ml-1 hover:text-red-500">&times;</button>
              </Badge>
            </div>
            <div class="flex gap-2">
              <input
                v-model="newHardSkill"
                @keyup.enter="addSkill('hard_skills', newHardSkill); newHardSkill = ''"
                type="text"
                placeholder="Agregar habilidad tecnica..."
                class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
              />
              <button
                @click="addSkill('hard_skills', newHardSkill); newHardSkill = ''"
                class="px-4 py-2 bg-emi-navy-500 text-white rounded-lg hover:bg-emi-navy-600 transition-colors"
              >
                Agregar
              </button>
            </div>
          </div>

          <!-- Soft Skills -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Habilidades Blandas</label>
            <div class="flex flex-wrap gap-2 mb-2">
              <Badge v-for="(skill, index) in editForm.soft_skills" :key="skill" variant="gold">
                {{ skill }}
                <button @click="removeSkill('soft_skills', index)" class="ml-1 hover:text-red-500">&times;</button>
              </Badge>
            </div>
            <div class="flex gap-2">
              <input
                v-model="newSoftSkill"
                @keyup.enter="addSkill('soft_skills', newSoftSkill); newSoftSkill = ''"
                type="text"
                placeholder="Agregar habilidad blanda..."
                class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-gold-500 focus:border-transparent"
              />
              <button
                @click="addSkill('soft_skills', newSoftSkill); newSoftSkill = ''"
                class="px-4 py-2 bg-emi-gold-500 text-emi-navy-800 rounded-lg hover:bg-emi-gold-400 transition-colors"
              >
                Agregar
              </button>
            </div>
          </div>

          <!-- Languages -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Idiomas</label>
            <div class="flex flex-wrap gap-2 mb-2">
              <Badge v-for="(lang, index) in editForm.languages" :key="lang" variant="neutral">
                {{ lang }}
                <button @click="removeSkill('languages', index)" class="ml-1 hover:text-red-500">&times;</button>
              </Badge>
            </div>
            <div class="flex gap-2">
              <input
                v-model="newLanguage"
                @keyup.enter="addSkill('languages', newLanguage); newLanguage = ''"
                type="text"
                placeholder="Agregar idioma..."
                class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-transparent"
              />
              <button
                @click="addSkill('languages', newLanguage); newLanguage = ''"
                class="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
              >
                Agregar
              </button>
            </div>
          </div>
        </div>

        <!-- Education Edit -->
        <div v-if="editModal.type === 'education'" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Nivel Educativo</label>
            <select
              v-model="editForm.education_level"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
            >
              <option value="">Seleccionar nivel...</option>
              <option value="Bachiller">Bachiller</option>
              <option value="Tecnico Superior">Tecnico Superior</option>
              <option value="Licenciatura">Licenciatura</option>
              <option value="Ingenieria">Ingenieria</option>
              <option value="Especialidad">Especialidad</option>
              <option value="Maestria">Maestria</option>
              <option value="Doctorado">Doctorado</option>
            </select>
          </div>
        </div>

        <!-- Experience Edit -->
        <div v-if="editModal.type === 'experience'" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Anos de Experiencia</label>
            <input
              v-model.number="editForm.experience_years"
              type="number"
              min="0"
              max="50"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emi-navy-500 focus:border-transparent"
            />
          </div>
        </div>

        <div class="mt-6 flex justify-end gap-3">
          <button
            @click="closeEditModal"
            class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
          >
            Cancelar
          </button>
          <button
            @click="saveChanges"
            :disabled="saving"
            class="btn-emi-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ saving ? 'Guardando...' : 'Guardar Cambios' }}
          </button>
        </div>
      </Card>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50">
      <Card class="max-w-md mx-4" :hoverable="false">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Confirmar limpieza de perfil</h3>
        <p class="text-gray-600 mb-6">
          Esto eliminara todos los datos de tu CV y competencias. Tendras que subir tu CV nuevamente.
          Esta accion no se puede deshacer.
        </p>
        <div class="flex justify-end gap-3">
          <button
            @click="showDeleteConfirm = false"
            class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
          >
            Cancelar
          </button>
          <button
            @click="deleteProfile"
            :disabled="deleting"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 transition-colors"
          >
            {{ deleting ? 'Eliminando...' : 'Eliminar' }}
          </button>
        </div>
      </Card>
      </div>
    </div>
  </div>
  </StudentLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getMyProfile, getProfileCompleteness, deleteMyProfile, updateMyProfile, uploadCV } from '../services/api'
import { useUiStore } from '../stores/ui'
import StudentLayout from '../components/student/StudentLayout.vue'
import CollapsibleSidebar from '../components/ui/CollapsibleSidebar.vue'
import Card from '../components/ui/Card.vue'
import Badge from '../components/ui/Badge.vue'
import GaugeChart from '../components/ui/GaugeChart.vue'

const uiStore = useUiStore()
const showProfileSummary = ref(true) // Keep for backward compatibility if needed, though replaced by sidebar
const isSecondarySidebarOpen = ref(true)

const profile = ref({
  hard_skills: [],
  soft_skills: [],
  languages: [],
  education_level: null,
  experience_years: 0,
  is_complete: false,
  completeness_score: 0,
  cv_filename: null,
  cv_uploaded_at: null,
  gemini_extraction: {}
})
const completeness = ref(null)
const loading = ref(true)
const error = ref(null)
const showDeleteConfirm = ref(false)
const deleting = ref(false)
const isMobileSidebarOpen = ref(false)

// Upload CV
const showUploadModal = ref(false)
const uploadFile = ref(null)
const uploading = ref(false)
const isDragging = ref(false)

// Edit Modal
const editModal = ref({ show: false, type: '', title: '' })
const editForm = ref({
  hard_skills: [],
  soft_skills: [],
  languages: [],
  education_level: '',
  experience_years: 0
})
const saving = ref(false)
const newHardSkill = ref('')
const newSoftSkill = ref('')
const newLanguage = ref('')

const geminiEducation = computed(() => {
  return profile.value.gemini_extraction?.education || []
})

const geminiExperience = computed(() => {
  return profile.value.gemini_extraction?.experience || []
})

const geminiPersonalInfo = computed(() => {
  return profile.value.gemini_extraction?.personal_info || {}
})

const hasGeminiData = computed(() => {
  const extraction = profile.value.gemini_extraction
  if (!extraction) return false
  return (
    (extraction.education && extraction.education.length > 0) ||
    (extraction.experience && extraction.experience.length > 0) ||
    (extraction.hard_skills && extraction.hard_skills.length > 0) ||
    (extraction.soft_skills && extraction.soft_skills.length > 0) ||
    (extraction.personal_info && Object.keys(extraction.personal_info).length > 0)
  )
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const loadProfile = async () => {
  loading.value = true
  error.value = null

  try {
    const [profileData, completenessData] = await Promise.all([
      getMyProfile(),
      getProfileCompleteness()
    ])

    profile.value = profileData
    completeness.value = completenessData
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error cargando el perfil'
  } finally {
    loading.value = false
  }
}

const deleteProfileAction = async () => {
  deleting.value = true

  try {
    await deleteMyProfile()
    showDeleteConfirm.value = false
    await loadProfile()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error eliminando el perfil'
  } finally {
    deleting.value = false
  }
}

// Alias for template
const deleteProfile = deleteProfileAction

// Upload CV handlers
const handleFileSelect = (event) => {
  const file = event.target.files[0]
  validateAndSetFile(file)
}

const handleDrop = (event) => {
  isDragging.value = false
  const file = event.dataTransfer.files[0]
  validateAndSetFile(file)
}

const validateAndSetFile = (file) => {
  if (!file) return

  if (!file.name.toLowerCase().endsWith('.pdf')) {
    alert('Solo se permiten archivos PDF')
    return
  }

  if (file.size > 10 * 1024 * 1024) {
    alert('El archivo excede el tamano maximo de 10MB')
    return
  }

  uploadFile.value = file
}

const processCV = async () => {
  if (!uploadFile.value) return

  uploading.value = true

  try {
    await uploadCV(uploadFile.value)
    showUploadModal.value = false
    uploadFile.value = null
    await loadProfile()
  } catch (e) {
    alert(e.response?.data?.detail || 'Error procesando el CV')
  } finally {
    uploading.value = false
  }
}

// Edit Modal handlers
const openEditModal = (type) => {
  editModal.value.type = type
  editModal.value.show = true

  switch (type) {
    case 'skills':
      editModal.value.title = 'Editar Competencias'
      editForm.value.hard_skills = [...profile.value.hard_skills]
      editForm.value.soft_skills = [...profile.value.soft_skills]
      editForm.value.languages = [...profile.value.languages]
      break
    case 'education':
      editModal.value.title = 'Editar Formacion'
      editForm.value.education_level = profile.value.education_level || ''
      break
    case 'experience':
      editModal.value.title = 'Editar Experiencia'
      editForm.value.experience_years = profile.value.experience_years || 0
      break
  }
}

const closeEditModal = () => {
  editModal.value.show = false
  editModal.value.type = ''
  editModal.value.title = ''
  newHardSkill.value = ''
  newSoftSkill.value = ''
  newLanguage.value = ''
}

const addSkill = (field, value) => {
  if (!value || !value.trim()) return
  const trimmed = value.trim()
  if (!editForm.value[field].includes(trimmed)) {
    editForm.value[field].push(trimmed)
  }
}

const removeSkill = (field, index) => {
  editForm.value[field].splice(index, 1)
}

const saveChanges = async () => {
  saving.value = true

  try {
    const updates = {}

    switch (editModal.value.type) {
      case 'skills':
        updates.hard_skills = editForm.value.hard_skills
        updates.soft_skills = editForm.value.soft_skills
        updates.languages = editForm.value.languages
        break
      case 'education':
        updates.education_level = editForm.value.education_level
        break
      case 'experience':
        updates.experience_years = editForm.value.experience_years
        break
    }

    await updateMyProfile(updates)
    closeEditModal()
    await loadProfile()
  } catch (e) {
    alert(e.response?.data?.detail || 'Error guardando los cambios')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadProfile()
})
</script>
