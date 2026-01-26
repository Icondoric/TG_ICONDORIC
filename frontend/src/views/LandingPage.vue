<template>
  <div class="landing-page">
    <!-- Navbar Component -->
    <NavBar />

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-container">
        <div class="hero-content">
          <h1>Sistema de Evaluación de Perfiles Profesionales con IA</h1>
          <p>Plataforma inteligente que aplica Procesamiento de Lenguaje Natural y Machine Learning para recomendar oportunidades laborales y de pasantía según tu perfil académico</p>
          <div class="hero-stats">
            <div class="stat">
              <span class="stat-number">92%</span>
              <span class="stat-label">Precisión en evaluación</span>
            </div>
            <div class="stat">
              <span class="stat-number">&lt; 30s</span>
              <span class="stat-label">Procesamiento NLP</span>
            </div>
            <div class="stat">
              <span class="stat-number">100+</span>
              <span class="stat-label">Convenios activos</span>
            </div>
          </div>
        </div>

        <div class="upload-card">
          <h3>Digitaliza tu Perfil</h3>
          <p>Carga tu CV y recibe recomendaciones personalizadas de la EMI</p>
          <div 
            class="dropzone" 
            @click="triggerFileInput"
            @dragover.prevent="handleDragOver"
            @dragleave="handleDragLeave"
            @drop.prevent="handleDrop"
            :class="{ 'border-primary': isDragging }"
          >
            <div class="dropzone-content" v-if="!isProcessing">
                <div class="dropzone-icon">📄</div>
                <div style="color: var(--text-dark); font-weight: 500; margin-bottom: 0.5rem;">Arrastra tu CV aquí</div>
                <div style="color: var(--text-light); font-size: 0.9rem;">o haz clic para seleccionar (PDF, máx. 2MB)</div>
            </div>
            <div class="dropzone-content" v-else>
                 <div style="font-size: 4rem; margin-bottom: 1rem;">⏳</div>
                <div style="color: var(--text-dark); font-weight: 500;">Procesando con NLP...</div>
                <div style="color: var(--text-light); font-size: 0.9rem; margin-top: 0.5rem;">{{ processingFileName }}</div>
            </div>
          </div>
          <input 
            type="file" 
            ref="fileInputRef" 
            accept=".pdf" 
            style="display: none;" 
            @change="handleFileChange"
          >
          <button class="btn-upload" @click="triggerFileInput">Comenzar Evaluación</button>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features" id="features">
      <div class="features-container">
        <h2 class="section-title">Un Sistema de Apoyo a la Decisión</h2>
        <p class="section-subtitle">Tecnología de vanguardia para conectar estudiantes y titulados de la EMI con oportunidades institucionales</p>
        
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>Extracción Automática con NLP</h3>
            <p>Procesamiento híbrido que combina expresiones regulares (Regex) para datos de contacto y spaCy para identificar competencias técnicas y blandas en español</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3>Evaluación Inteligente</h3>
            <p>Modelo de Machine Learning (TF-IDF + Similitud Coseno) que calcula la correspondencia entre tu perfil y los perfiles laborales de referencia basados en convenios institucionales</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3>Validación Humana</h3>
            <p>El sistema pre-llena tu información pero TÚ tienes la última palabra. Valida y corrige los datos extraídos antes de confirmar tu perfil</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h3>Explicabilidad Total</h3>
            <p>No solo recibes un porcentaje de compatibilidad. El sistema te muestra EXACTAMENTE qué competencias coinciden y cuáles te faltan para cada oferta</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Recomendaciones, No Postulaciones</h3>
            <p>El sistema genera sugerencias basadas en tu perfil. Para postular, debes seguir el conducto regular de la Unidad de Vinculación de la EMI</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <h3>Seguridad JWT + bcrypt</h3>
            <p>Autenticación stateless con tokens firmados y hashing irreversible de contraseñas. Tus datos están protegidos con estándares de la industria</p>
          </div>
        </div>
      </div>
    </section>

    <!-- How it Works -->
    <section class="how-it-works" id="how-it-works">
      <div class="features-container">
        <h2 class="section-title">¿Cómo Funciona el Sistema?</h2>
        <p class="section-subtitle">Proceso validado mediante metodología CRISP-DM y desarrollo incremental con SCRUM</p>

        <div class="steps">
          <div class="step">
            <div class="step-number">1</div>
            <h3>Digitalización del CV</h3>
            <p>Sube tu currículum en PDF. El módulo de NLP extrae datos de contacto (Regex), limpia el texto y detecta competencias usando diccionarios validados (spaCy es_core_news_md)</p>
          </div>

          <div class="step">
            <div class="step-number">2</div>
            <h3>Validación Manual</h3>
            <p>Revisas un formulario pre-llenado con la información extraída. Corriges errores de lectura y confirmas tu perfil antes de guardarlo en la base de datos híbrida (SQL + NoSQL)</p>
          </div>

          <div class="step">
            <div class="step-number">3</div>
            <h3>Evaluación de Correspondencia</h3>
            <p>El modelo de ML compara tu texto normalizado con las convocatorias mediante vectorización TF-IDF y similitud coseno, generando un porcentaje de afinidad</p>
          </div>

          <div class="step">
            <div class="step-number">4</div>
            <h3>Recomendaciones Personalizadas</h3>
            <p>Recibes un ranking de oportunidades (Pasantías/Trabajos Dirigidos/Empleos) ordenadas por compatibilidad, con detalles sobre qué competencias posees y cuáles necesitas desarrollar</p>
          </div>
        </div>
      </div>
    </section>

    <!-- About Section -->
    <section class="about-section" id="about">
      <!-- Header -->
      <div class="section-header">
        <h1 class="section-title">Acerca del Sistema</h1>
        <p class="section-subtitle">
            Sistema de Evaluación de Perfiles Profesionales aplicando Procesamiento de Lenguaje Natural y Machine Learning para la Escuela Militar de Ingeniería
        </p>
      </div>

      <!-- Main Description -->
      <div class="main-description">
        <h3>🎯 ¿Qué es este Sistema?</h3>
        <p>
            Este proyecto constituye un <strong>Trabajo de Grado</strong> desarrollado para el Vicerrectorado de Grado de la Escuela Militar de Ingeniería, que tiene como propósito central crear una plataforma web inteligente de intermediación entre estudiantes/titulados y las oportunidades laborales y de pasantía ofrecidas por instituciones y empresas con convenio vigente.
        </p>
        <p>
            A diferencia de los sistemas tradicionales que funcionan como simples repositorios de archivos, esta plataforma es un <strong>sistema activo de apoyo a la toma de decisiones</strong> capaz de "leer", "entender" y "conectar" información académica con demandas reales del mercado laboral mediante técnicas avanzadas de Inteligencia Artificial.
        </p>

        <div class="highlight-box">
            <strong>Alcance Explícito:</strong> El sistema se limita a la generación de recomendaciones de correspondencia entre perfiles y ofertas. <strong>NO gestiona postulaciones, selección final, entrevistas ni procesos de contratación</strong>, los cuales dependen exclusivamente de las empresas e instituciones y de los procedimientos establecidos por la Unidad de Vinculación de la EMI.
        </div>

        <p>
            El sistema integra dos pilares tecnológicos fundamentales: el <strong>Procesamiento de Lenguaje Natural (PLN)</strong> para extraer y estructurar automáticamente la información contenida en los currículums, y el <strong>Machine Learning</strong> para evaluar matemáticamente el grado de correspondencia entre el perfil del candidato y los requisitos de cada convocatoria.
        </p>
      </div>

      <!-- Problem-Solution -->
      <div class="problem-solution">
        <div class="ps-card problem">
            <h4>❌ Problemática Identificada</h4>
            <ul class="ps-list">
                <li>Información dispersa en múltiples canales (Facebook, correos, tableros físicos)</li>
                <li>CVs en formatos no estandarizados dificultan la comparación</li>
                <li>Búsqueda manual consume tiempo valioso del estudiante</li>
                <li>Ausencia de criterios objetivos para identificar oportunidades afines</li>
                <li>Descentralización impide seguimiento institucional</li>
                <li>Bolivia: 80.8% de informalidad laboral (OIT, 2024)</li>
            </ul>
        </div>

        <div class="ps-card solution">
            <h4>✅ Solución Propuesta</h4>
            <ul class="ps-list">
                <li>Centralización de información en plataforma única</li>
                <li>Extracción automática de datos con NLP híbrido (Regex + spaCy)</li>
                <li>Recomendaciones personalizadas en segundos</li>
                <li>Evaluación objetiva mediante similitud coseno (0-100%)</li>
                <li>Dashboard de métricas para gestión institucional</li>
                <li>Explicabilidad total del porcentaje de match</li>
            </ul>
        </div>
      </div>

      <!-- Objectives -->
      <div class="objectives">
        <h3>🎓 Objetivos del Proyecto</h3>

        <div class="objective-item">
            <div class="objective-number">G</div>
            <div class="objective-content">
                <h4>Objetivo General</h4>
                <p>Desarrollar un sistema de evaluación de perfiles profesionales aplicando procesamiento de lenguaje natural y machine learning, para centralizar la información de estudiantes y titulados con el propósito de apoyar la toma de decisiones en la identificación de correspondencia entre aptitudes y demandas, a fin de generar recomendaciones laborales y de pasantía en empresas e instituciones con convenio vigente en la EMI.</p>
            </div>
        </div>

        <div class="objective-item">
            <div class="objective-number">1</div>
            <div class="objective-content">
                <h4>Recopilación de Información</h4>
                <p>Recopilar información de convenios gestionados a través de la EMI para determinar los requerimientos funcionales y técnicos del sistema de evaluación de perfiles profesionales.</p>
            </div>
        </div>

        <div class="objective-item">
            <div class="objective-number">2</div>
            <div class="objective-content">
                <h4>Diseño de Arquitectura</h4>
                <p>Diseñar la arquitectura que permita la gestión de información de perfiles, considerando un módulo de procesamiento de lenguaje natural para la extracción y estructuración de información relevante contenida en los currículums.</p>
            </div>
        </div>

        <div class="objective-item">
            <div class="objective-number">3</div>
            <div class="objective-content">
                <h4>Integración del Modelo ML</h4>
                <p>Integrar un modelo de machine learning que permita evaluar los perfiles profesionales con los perfiles laborales de referencia, determinando el nivel de correspondencia entre ambos.</p>
            </div>
        </div>

        <div class="objective-item">
            <div class="objective-number">4</div>
            <div class="objective-content">
                <h4>Validación Integral</h4>
                <p>Realizar la validación integral del sistema mediante pruebas unitarias, de integración, funcionales, de rendimiento y de usabilidad, verificando el correcto desempeño de los módulos de procesamiento de lenguaje natural y machine learning.</p>
            </div>
        </div>
      </div>

      <!-- Methodologies -->
      <h3 style="text-align: center; color: var(--primary); font-size: 1.8rem; margin: 3rem 0 2rem;">📐 Metodologías Aplicadas</h3>
      
      <div class="methodologies">
        <div class="methodology-card">
            <div class="methodology-icon">🔄</div>
            <h4>SCRUM</h4>
            <p>Marco ágil para el desarrollo incremental del software en sprints de 2 semanas</p>
            <div class="methodology-phases">
                <span class="phase-tag">Sprint Planning</span>
                <span class="phase-tag">Daily Scrum</span>
                <span class="phase-tag">Sprint Review</span>
                <span class="phase-tag">Retrospectiva</span>
            </div>
        </div>

        <div class="methodology-card">
            <div class="methodology-icon">📊</div>
            <h4>CRISP-DM</h4>
            <p>Estándar internacional para el desarrollo del modelo de Machine Learning</p>
            <div class="methodology-phases">
                <span class="phase-tag">Comprensión del Negocio</span>
                <span class="phase-tag">Comprensión de Datos</span>
                <span class="phase-tag">Preparación</span>
                <span class="phase-tag">Modelado</span>
                <span class="phase-tag">Evaluación</span>
                <span class="phase-tag">Despliegue</span>
            </div>
        </div>

        <div class="methodology-card">
            <div class="methodology-icon">📐</div>
            <h4>UML 2.5.1</h4>
            <p>Lenguaje de modelado unificado para el diseño arquitectónico del sistema</p>
            <div class="methodology-phases">
                <span class="phase-tag">Casos de Uso</span>
                <span class="phase-tag">Clases</span>
                <span class="phase-tag">Secuencia</span>
                <span class="phase-tag">Componentes</span>
                <span class="phase-tag">Despliegue</span>
            </div>
        </div>
      </div>

      <!-- Team Section -->
      <div class="team-section">
        <h3>👥 Equipo del Proyecto</h3>
        <div class="team-grid">
            <div class="team-member">
                <div class="team-avatar">👨🎓</div>
                <div class="team-name">Ivan Condori Choquehuanca</div>
                <div class="team-role">Autor del Trabajo de Grado<br>Estudiante de Ingeniería de Sistemas</div>
            </div>

            <div class="team-member">
                <div class="team-avatar">👩🏫</div>
                <div class="team-name">Lic. Cynthia Rodriguez Canaviri</div>
                <div class="team-role">Tutora del Proyecto<br>Escuela Militar de Ingeniería</div>
            </div>

            <div class="team-member">
                <div class="team-avatar">🏛️</div>
                <div class="team-name">Vicerrectorado de Grado</div>
                <div class="team-role">Unidad Beneficiaria<br>Caso de Estudio: UALP</div>
            </div>
        </div>
      </div>

      <!-- Timeline -->
      <div class="timeline">
        <h3>📅 Línea de Tiempo del Desarrollo</h3>

        <div class="timeline-item">
            <div class="timeline-date">Fase 1</div>
            <div class="timeline-content">
                <h4>Recopilación y Análisis (Pre-Juego SCRUM)</h4>
                <p>Análisis de la situación actual, identificación de actores, historias de usuario y Product Backlog</p>
            </div>
        </div>

        <div class="timeline-item">
            <div class="timeline-date">Fase 2</div>
            <div class="timeline-content">
                <h4>Diseño de Arquitectura (Comprensión CRISP-DM)</h4>
                <p>Diseño del módulo NLP, arquitectura del sistema, base de datos híbrida y modelado UML</p>
            </div>
        </div>

        <div class="timeline-item">
            <div class="timeline-date">Fase 3</div>
            <div class="timeline-content">
                <h4>Integración del Modelo ML (Preparación y Modelado)</h4>
                <p>Preparación de datos, vectorización TF-IDF, entrenamiento del modelo de similitud</p>
            </div>
        </div>

        <div class="timeline-item">
            <div class="timeline-date">Fase 4</div>
            <div class="timeline-content">
                <h4>Desarrollo por Sprints (Juego SCRUM)</h4>
                <p>5 sprints de desarrollo incremental: Usuarios, Digitalización, Ofertas, Evaluación, Reportes</p>
            </div>
        </div>

        <div class="timeline-item">
            <div class="timeline-date">Fase 5</div>
            <div class="timeline-content">
                <h4>Validación Integral (Post-Juego + Evaluación)</h4>
                <p>Pruebas unitarias, de integración, funcionales, de rendimiento y usabilidad</p>
            </div>
        </div>
      </div>

      <!-- Stats -->
      <h3 style="text-align: center; color: var(--primary); font-size: 1.8rem; margin: 3rem 0 2rem;">📈 Datos del Contexto</h3>
      
      <div class="stats-grid">
        <div class="stat-card">
            <span class="stat-number">80.8%</span>
            <span class="stat-label">Informalidad laboral en Bolivia (OIT, 2024)</span>
        </div>

        <div class="stat-card">
            <span class="stat-number">100+</span>
            <span class="stat-label">Convenios institucionales vigentes (EMI UALP)</span>
        </div>

        <div class="stat-card">
            <span class="stat-number">50-100</span>
            <span class="stat-label">Perfiles piloto para validación del sistema</span>
        </div>

        <div class="stat-card">
            <span class="stat-number">6</span>
            <span class="stat-label">Carreras de ingeniería en la UALP</span>
        </div>

        <div class="stat-card">
            <span class="stat-number">92%</span>
            <span class="stat-label">Precisión esperada en evaluación de perfiles</span>
        </div>

        <div class="stat-card">
            <span class="stat-number">&lt; 30s</span>
            <span class="stat-label">Tiempo de procesamiento NLP por CV</span>
        </div>
      </div>

      <!-- Final Note -->
      <div class="main-description" style="margin-top: 3rem;">
        <h3>🔬 Fundamentación Académica</h3>
        <p>
            Este proyecto se sustenta en investigación académica y estándares internacionales reconocidos. El diseño del módulo de Procesamiento de Lenguaje Natural se basa en los trabajos de <strong>Manning, Raghavan & Schütze (2008)</strong> sobre recuperación de información, mientras que la arquitectura de Transformers sigue los lineamientos de <strong>Tunstall, von Werra & Wolf (2022)</strong>.
        </p>
        <p>
            El modelo de Machine Learning se fundamenta en los principios establecidos por <strong>Mitchell (1997)</strong> y las técnicas de vectorización documentadas en <strong>Goodfellow, Bengio & Courville (2016)</strong>. La metodología de desarrollo sigue los estándares del <strong>IEEE SWEBOK</strong> y las mejores prácticas de ingeniería de software propuestas por <strong>Pressman (2010)</strong> y <strong>Sommerville (2011)</strong>.
        </p>
        <p>
            El contexto sociolaboral se analizó utilizando datos de la <strong>Organización Internacional del Trabajo (OIT, 2024-2025)</strong> y estudios de habilidades de la <strong>OECD (2023)</strong>, que evidencian la problemática del desajuste de competencias en América Latina y el Caribe.
        </p>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta">
      <h2>¿Listo para Descubrir tus Oportunidades?</h2>
      <p>Sistema desarrollado para el Vicerrectorado de Grado de la Escuela Militar de Ingeniería</p>
      <button class="btn-cta" @click="scrollToTop">
        Comenzar Evaluación
      </button>
    </section>

    <!-- Footer -->
    <footer>
      <div class="footer-container">
        <div class="footer-section">
          <h4>Sobre el Sistema</h4>
          <p>Trabajo de Grado: "Sistema de Evaluación de Perfiles Profesionales Aplicando Procesamiento de Lenguaje Natural y Machine Learning"</p>
          <p style="margin-top: 1rem; font-size: 0.9rem;">Autor: Ivan Condori Choquehuanca<br>Tutora: Lic. Cynthia Rodriguez Canaviri</p>
        </div>

        <div class="footer-section">
          <h4>Alcance del Sistema</h4>
          <p>✓ Digitalización de CVs con NLP</p>
          <p>✓ Evaluación de correspondencia con ML</p>
          <p>✓ Generación de recomendaciones</p>
          <p>✗ NO gestiona postulaciones ni contratación</p>
        </div>

        <div class="footer-section">
          <h4>Metodologías Aplicadas</h4>
          <p>• CRISP-DM (Desarrollo del Modelo ML)</p>
          <p>• SCRUM (Desarrollo de Software)</p>
          <p>• UML 2.5.1 (Diseño Arquitectónico)</p>
        </div>

        <div class="footer-section">
          <h4>Contacto EMI</h4>
          <p>📧 vinculacion@emi.edu.bo</p>
          <p>📞 +591 (2) 2482121</p>
          <p>📍 Unidad Académica La Paz</p>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; 2025 Escuela Militar de Ingeniería "Mcal. Antonio José de Sucre" | Prestigio, Disciplina y Oportunidades</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import NavBar from '../components/NavBar.vue'

const router = useRouter()
const authStore = useAuthStore()
const fileInputRef = ref(null)
const isDragging = ref(false)
const isProcessing = ref(false)
const processingFileName = ref('')

const scrollToSection = (id) => {
  const element = document.getElementById(id)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
}

const triggerFileInput = () => {
  fileInputRef.value.click()
}

const handleDragOver = () => {
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

const handleDrop = (e) => {
  isDragging.value = false
  const file = e.dataTransfer.files[0]
  if (file) validateAndProcessFile(file)
}

const handleFileChange = (e) => {
  const file = e.target.files[0]
  if (file) validateAndProcessFile(file)
}

const validateAndProcessFile = (file) => {
  if (file.type !== 'application/pdf') {
    alert('Por favor sube un archivo PDF válido')
    return
  }
  
  if (file.size > 2 * 1024 * 1024) {
    alert('El archivo no debe superar 2MB')
    return
  }

  processFile(file)
}

const processFile = (file) => {
  isProcessing.value = true
  processingFileName.value = file.name
  
  // Simulation of processing
  setTimeout(() => {
    alert('En la versión completa, serías redirigido al formulario de validación con tus datos pre-llenados.')
    // Here we would navigate to the validation or register page with the file
    // router.push({ name: 'register', query: { from: 'upload' } }) 
    isProcessing.value = false
    processingFileName.value = ''
    router.push('/register') // Redirecting to register for now as per "Phase 1" flows likely needing auth or at least profile creation
  }, 2000)
}
</script>

<style scoped>
/* Scoped styles based on the provided CSS */
.landing-page {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #1f2937; /* var(--text-dark) */
  line-height: 1.6;
  overflow-x: hidden;
  --primary: #1e40af;
  --primary-dark: #1e3a8a;
  --secondary: #10b981;
  --accent: #f59e0b;
  --text-dark: #1f2937;
  --text-light: #6b7280;
  --bg-light: #f9fafb;
}

/* Navbar Styles Removed - Using Component */


/* Hero Section */
.hero {
  margin-top: 80px;
  min-height: 90vh;
  background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="2" fill="white" opacity="0.1"/></svg>');
  animation: float 20s linear infinite;
}

@keyframes float {
  to { transform: translateY(-100px); }
}

.hero-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 4rem 2rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  position: relative;
  z-index: 1;
}

.hero-content h1 {
  font-size: 3rem;
  color: white;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.hero-content p {
  font-size: 1.2rem;
  color: rgba(255,255,255,0.9);
  margin-bottom: 2rem;
}

.hero-stats {
  display: flex;
  gap: 3rem;
  margin-top: 2rem;
}

.stat {
  text-align: center;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: var(--accent);
  display: block;
}

.stat-label {
  color: rgba(255,255,255,0.8);
  font-size: 0.9rem;
}

/* Upload Card */
.upload-card {
  background: white;
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  text-align: center;
}

.upload-card h3 {
  color: var(--text-dark);
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

.upload-card p {
  color: var(--text-light);
  margin-bottom: 2rem;
}

.dropzone {
  border: 3px dashed #cbd5e1;
  border-radius: 12px;
  padding: 3rem 2rem;
  cursor: pointer;
  transition: all 0.3s;
  background: var(--bg-light);
}

.dropzone:hover, .dropzone.border-primary {
  border-color: var(--primary);
  background: rgba(30, 64, 175, 0.05);
  transform: scale(1.02);
}

.dropzone-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.btn-upload {
  width: 100%;
  background: var(--secondary);
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 1.5rem;
  transition: all 0.3s;
}

.btn-upload:hover {
  background: #059669;
  transform: translateY(-2px);
}

/* Features Section */
.features {
  padding: 6rem 2rem;
  background: white;
}

.features-container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  color: var(--text-dark);
  margin-bottom: 1rem;
}

.section-subtitle {
  text-align: center;
  color: var(--text-light);
  font-size: 1.2rem;
  margin-bottom: 4rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-card {
  padding: 2rem;
  border-radius: 12px;
  background: var(--bg-light);
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: var(--text-dark);
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

/* How it Works */
.how-it-works {
  padding: 6rem 2rem;
  background: var(--bg-light);
}

.steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 3rem;
  margin-top: 4rem;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.step {
  text-align: center;
}

.step-number {
  width: 60px;
  height: 60px;
  background: var(--primary);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0 auto 1.5rem;
}

/* About Section Styles */
.about-section {
    max-width: 1200px;
    margin: 4rem auto;
    padding: 0 2rem;
}

.section-header {
    text-align: center;
    margin-bottom: 4rem;
}

.section-title {
    font-size: 3rem;
    color: var(--primary);
    margin-bottom: 1rem;
    font-weight: 700;
}

.section-subtitle {
    font-size: 1.3rem;
    color: var(--text-light);
    max-width: 800px;
    margin: 0 auto;
}

/* Main Description */
.main-description {
    background: white;
    padding: 3rem;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 3rem;
}

.main-description h3 {
    color: var(--primary);
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.main-description p {
    color: var(--text-dark);
    font-size: 1.1rem;
    line-height: 1.8;
    margin-bottom: 1.2rem;
}

.highlight-box {
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    padding: 1.5rem;
    border-radius: 12px;
    border-left: 4px solid var(--primary);
    margin: 2rem 0;
}

.highlight-box strong {
    color: var(--primary);
}

/* Problem-Solution Grid */
.problem-solution {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin: 3rem 0;
}

.ps-card {
    background: white;
    padding: 2.5rem;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.ps-card h4 {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.ps-card.problem h4 {
    color: #dc2626;
}

.ps-card.solution h4 {
    color: var(--secondary);
}

.ps-list {
    list-style: none;
    padding: 0;
}

.ps-list li {
    padding: 0.8rem 0;
    padding-left: 2rem;
    position: relative;
    color: var(--text-dark);
}

.ps-list li::before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.problem .ps-list li::before {
    background: #dc2626;
}

.solution .ps-list li::before {
    background: var(--secondary);
}

/* Objectives Section */
.objectives {
    background: white;
    padding: 3rem;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin: 3rem 0;
}

.objectives h3 {
    color: var(--primary);
    font-size: 1.8rem;
    margin-bottom: 2rem;
    text-align: center;
}

.objective-item {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 2rem;
    padding: 1.5rem;
    background: var(--bg-light);
    border-radius: 12px;
    transition: all 0.3s;
}

.objective-item:hover {
    transform: translateX(10px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.objective-number {
    flex-shrink: 0;
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: bold;
}

.objective-content h4 {
    color: var(--text-dark);
    margin-bottom: 0.5rem;
    font-size: 1.2rem;
}

.objective-content p {
    color: var(--text-light);
}

/* Methodologies */
.methodologies {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin: 3rem 0;
}

.methodology-card {
    background: white;
    padding: 2.5rem;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    text-align: center;
    transition: all 0.3s;
}

.methodology-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}

.methodology-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.methodology-card h4 {
    color: var(--primary);
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.methodology-card p {
    color: var(--text-light);
}

.methodology-phases {
    margin-top: 1.5rem;
    text-align: left;
}

.phase-tag {
    display: inline-block;
    background: var(--bg-light);
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    font-size: 0.85rem;
    margin: 0.3rem; /* Adjusted for wrapping */
    color: var(--text-dark);
}

/* Team Section */
.team-section {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    padding: 3rem;
    border-radius: 16px;
    color: white;
    margin: 3rem 0;
}

.team-section h3 {
    font-size: 1.8rem;
    margin-bottom: 2rem;
    text-align: center;
    color: white; /* Ensure title is white */
}

.team-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}

.team-member {
    text-align: center;
    padding: 2rem;
    background: rgba(255,255,255,0.1);
    border-radius: 12px;
    backdrop-filter: blur(10px);
}

.team-avatar {
    width: 100px;
    height: 100px;
    background: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
    font-size: 2.5rem;
}

.team-name {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: white; 
}

.team-role {
    opacity: 0.9;
    font-size: 0.95rem;
    color: white;
}

/* Timeline */
.timeline {
    background: white;
    padding: 3rem;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin: 3rem 0;
}

.timeline h3 {
    color: var(--primary);
    font-size: 1.8rem;
    margin-bottom: 2rem;
    text-align: center;
}

.timeline-item {
    display: flex;
    gap: 2rem;
    margin-bottom: 2rem;
    position: relative;
}

.timeline-item::before {
    content: '';
    position: absolute;
    left: 29px;
    top: 60px;
    bottom: -20px;
    width: 2px;
    background: var(--bg-light);
}

.timeline-item:last-child::before {
    display: none;
}

.timeline-date {
    flex-shrink: 0;
    width: 60px;
    height: 60px;
    background: var(--primary);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 0.9rem;
    text-align: center;
}

.timeline-content {
    flex: 1;
    padding-top: 0.5rem;
}

.timeline-content h4 {
    color: var(--text-dark);
    margin-bottom: 0.5rem;
}

.timeline-content p {
    color: var(--text-light);
}

/* Stats */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    margin: 3rem 0;
}

.stat-card {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    text-align: center;
}

.stat-number {
    font-size: 3rem;
    font-weight: bold;
    color: var(--primary);
    display: block;
    margin-bottom: 0.5rem;
}

.stat-label {
    color: var(--text-light);
    font-size: 0.95rem;
}

@media (max-width: 768px) {
    .problem-solution {
        grid-template-columns: 1fr;
    }

    .main-description {
        padding: 2rem;
    }
    
    .timeline-item {
        gap: 1rem;
    }
}

/* CTA Section */
.cta {
  padding: 6rem 2rem;
  background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  text-align: center;
  color: white;
}

.cta h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.btn-cta {
  background: white;
  color: var(--primary);
  padding: 1rem 3rem;
  border: none;
  border-radius: 8px;
  font-size: 1.2rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-cta:hover {
  transform: scale(1.05);
}

/* Footer */
footer {
  background: var(--text-dark);
  color: white;
  padding: 3rem 2rem 1rem;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.footer-section h4 {
  margin-bottom: 1rem;
  color: var(--accent);
}

.footer-bottom {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.5);
}

@media (max-width: 768px) {
  .hero-container {
    grid-template-columns: 1fr;
  }

  .hero-content h1 {
    font-size: 2rem;
  }

  .nav-links {
    display: none;
  }
}
</style>
