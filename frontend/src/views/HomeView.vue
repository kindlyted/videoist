<template>
  <div class="container mx-auto px-4 py-8">
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold mb-2">{{ $t('home.welcome') }}</h1>
      <p class="text-gray-600">{{ today }}</p>
    </div>
    
    <!-- 未登录状态 -->
    <div v-if="!isAuthenticated" class="flex justify-center space-x-4 mb-8">
      <button 
        @click="goToLogin" 
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        {{ $t('nav.login') }}
      </button>
      <button 
        @click="goToRegister" 
        class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded"
      >
        {{ $t('nav.register') }}
      </button>
    </div>
    
    <!-- 已登录状态 -->
    <div v-else class="flex justify-center space-x-4 mb-8">
      <button 
        @click="goToVideoCreation" 
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        {{ $t('nav.videoCreation') }}
      </button>
      <button 
        @click="goToDashboard" 
        class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded"
      >
        {{ $t('nav.dashboard') }}
      </button>
    </div>
    
    <!-- 功能介绍区域 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-2">{{ $t('home.podcastGeneration') }}</h2>
        <p class="text-gray-600">{{ $t('home.podcastGenerationDesc') }}</p>
      </div>
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-2">{{ $t('home.noteCardCreation') }}</h2>
        <p class="text-gray-600">{{ $t('home.noteCardCreationDesc') }}</p>
      </div>
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-2">{{ $t('home.oneClickDistribution') }}</h2>
        <p class="text-gray-600">{{ $t('home.oneClickDistributionDesc') }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useI18n } from 'vue-i18n'

const router = useRouter()
const userStore = useUserStore()
const { locale } = useI18n()

// 计算属性
const isAuthenticated = computed(() => userStore.isAuthenticated)
const today = computed(() => {
  const date = new Date()
  return date.toLocaleDateString(locale.value, { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric',
    weekday: 'long'
  })
})

// 方法
const goToLogin = () => {
  router.push('/login')
}

const goToRegister = () => {
  router.push('/register')
}

const goToVideoCreation = () => {
  router.push('/video-creation')
}

const goToDashboard = () => {
  router.push('/dashboard')
}
</script>