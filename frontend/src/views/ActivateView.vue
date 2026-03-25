<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Videoist</h1>
        <p class="text-gray-600">{{ $t('activation.title') }}</p>
      </div>
      
      <div class="bg-white border border-gray-200 shadow-lg rounded-2xl p-8">
        <!-- 加载中 -->
        <div v-if="loading" class="text-center py-8">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p class="text-gray-600">{{ $t('activation.loading') }}</p>
        </div>
        
        <!-- 激活成功 -->
        <div v-else-if="success" class="text-center py-8">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ $t('activation.successTitle') }}</h2>
          <p class="text-gray-600 mb-6">{{ $t('activation.successMessage') }}</p>
          <button 
            @click="goToLogin"
            class="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl transition-colors"
          >
            {{ $t('activation.goToLogin') }}
          </button>
        </div>
        
        <!-- 激活失败 -->
        <div v-else class="text-center py-8">
          <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ $t('activation.failureTitle') }}</h2>
          <p class="text-gray-600 mb-6">{{ errorMessage }}</p>
          <div class="space-y-3">
            <button 
              v-if="canResend"
              @click="resendActivation"
              :disabled="resending"
              class="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-medium rounded-xl transition-colors"
            >
              {{ resending ? $t('activation.resending') : $t('activation.resendEmail') }}
            </button>
            <button 
              @click="goToLogin"
              class="w-full py-3 px-4 bg-gray-100 hover:bg-gray-200 text-gray-900 font-medium rounded-xl transition-colors"
            >
              {{ $t('activation.backToLogin') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const { t, locale } = useI18n()

const loading = ref(true)
const success = ref(false)
const errorMessage = ref('')
const canResend = ref(false)
const resending = ref(false)

onMounted(async () => {
  const token = route.query.token
  
  if (!token) {
    loading.value = false
    errorMessage.value = t('activation.errors.invalidLink')
    return
  }
  
  try {
    const lang = locale.value
    const response = await axios.get(`/api/activate?token=${token}&lang=${lang}`)
    
    if (response.data.success) {
      success.value = true
    } else {
      success.value = false
      errorMessage.value = response.data.message || t('activation.failureTitle')
      canResend.value = response.data.message?.includes('过期') || 
                        response.data.message?.includes('已使用') ||
                        response.data.message?.includes('expired') ||
                        response.data.message?.includes('used')
    }
  } catch (error) {
    success.value = false
    if (error.response?.data?.message) {
      errorMessage.value = error.response.data.message
      const msg = error.response.data.message.toLowerCase()
      canResend.value = msg.includes('过期') || msg.includes('已使用') || msg.includes('无效') ||
                        msg.includes('expired') || msg.includes('used') || msg.includes('invalid')
    } else {
      errorMessage.value = t('activation.errors.network')
    }
  } finally {
    loading.value = false
  }
})

const goToLogin = () => {
  router.push('/login')
}

const resendActivation = async () => {
  resending.value = true
  try {
    const email = prompt(t('activation.enterEmail'))
    if (!email) {
      resending.value = false
      return
    }
    
    const response = await axios.post('/api/resend-activation', { email })
    
    if (response.data.success) {
      alert(t('activation.emailSent'))
    } else {
      alert(response.data.message || t('activation.sendFailed'))
    }
  } catch (error) {
    alert(error.response?.data?.message || t('activation.sendFailed'))
  } finally {
    resending.value = false
  }
}
</script>
