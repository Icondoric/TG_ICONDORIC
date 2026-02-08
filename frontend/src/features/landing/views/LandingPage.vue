<template>
  <div class="landing-page">
    <NavBar />

    <HeroSection
      :isDragging="isDragging"
      :isProcessing="isProcessing"
      :processingFileName="processingFileName"
      @triggerUpload="triggerFileInput"
      @dragOver="handleDragOver"
      @dragLeave="handleDragLeave"
      @drop="handleDrop"
    />

    <input
      type="file"
      ref="fileInputRef"
      accept=".pdf"
      class="hidden"
      @change="handleFileChange"
    >

    <FeaturesSection />
    <HowItWorksSection />
    <CTASection @scrollToTop="scrollToTop" />
    <FooterSection />
  </div>
</template>

<script setup>
import NavBar from '@/shared/components/NavBar.vue'
import HeroSection from '../components/HeroSection.vue'
import FeaturesSection from '../components/FeaturesSection.vue'
import HowItWorksSection from '../components/HowItWorksSection.vue'
import CTASection from '../components/CTASection.vue'
import FooterSection from '../components/FooterSection.vue'
import { useLandingUpload } from '../composables/useLandingUpload'

const {
  fileInputRef,
  isDragging,
  isProcessing,
  processingFileName,
  triggerFileInput,
  handleDragOver,
  handleDragLeave,
  handleDrop,
  handleFileChange,
  scrollToTop
} = useLandingUpload()
</script>
