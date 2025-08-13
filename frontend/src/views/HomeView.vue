<template>
  <div class="container mx-auto px-4 py-8">
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold mb-2">欢迎访问 Videoist!</h1>
      <p class="text-gray-600">今天是 {{ today }}</p>
    </div>
    
    <!-- 未登录状态 -->
    <div v-if="!isAuthenticated" class="flex justify-center space-x-4 mb-8">
      <button 
        @click="goToLogin" 
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        登录
      </button>
      <button 
        @click="goToRegister" 
        class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded"
      >
        注册
      </button>
    </div>
    
    <!-- 已登录状态 -->
    <div v-else class="flex justify-center space-x-4 mb-8">
      <button 
        @click="goToVideoCreation" 
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        开始创作视频
      </button>
      <button 
        @click="goToDashboard" 
        class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded"
      >
        访问仪表板
      </button>
    </div>
    
    <!-- 功能介绍区域 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-2">AI智能生成</h2>
        <p class="text-gray-600">使用先进的AI技术，自动生成高质量的视频内容，让创作更轻松。</p>
      </div>
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-2">快速高效</h2>
        <p class="text-gray-600">只需几分钟，即可将文章转化为精美视频，大大提升内容创作效率。</p>
      </div>
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-2">一键分发</h2>
        <p class="text-gray-600">支持多平台内容分发，让您的创作快速触达更多受众。</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

// 计算属性
const isAuthenticated = computed(() => userStore.isAuthenticated)
const today = computed(() => {
  const date = new Date()
  return date.toLocaleDateString('zh-CN', { 
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
  router.push('/video')
}

const goToDashboard = () => {
  router.push('/dashboard')
}
</script>