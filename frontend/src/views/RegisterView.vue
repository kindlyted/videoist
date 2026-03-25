<template>
  <div class="container mx-auto px-4 py-8 flex justify-center">
    <div class="w-full max-w-md bg-white rounded-lg shadow-md p-8">
      <h2 class="text-2xl font-bold text-center mb-8">{{ t('register.title') }}</h2>

      <!-- 邮箱注册 -->
      <form @submit.prevent="handleEmailRegister" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('register.email') }}</label>
          <div class="relative">
            <input
              v-model="emailForm.email"
              type="email"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-150"
              placeholder="your@email.com"
              required
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('login.code') }}</label>
          <div class="flex gap-3">
            <input
              v-model="emailForm.code"
              type="text"
              class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-150"
              :placeholder="t('login.codePlaceholder') || '6-digit verification code'"
              maxlength="6"
              required
            />
            <button
              type="button"
              @click="sendCode"
              :disabled="countdown > 0"
              class="px-6 py-3 bg-gray-100 text-gray-700 font-medium rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 transition duration-150 disabled:opacity-50 disabled:cursor-not-allowed min-w-[100px]"
            >
              {{ countdown > 0 ? `${countdown}s` : t('login.getCode') }}
            </button>
          </div>
        </div>

        <button
          type="submit"
          class="w-full py-3 px-4 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-150"
          :disabled="loading"
        >
          {{ loading ? t('register.registering') : t('nav.register') }}
        </button>
      </form>

      <div class="relative my-6">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-gray-300"></div>
        </div>
        <div class="relative flex justify-center text-sm">
          <span class="px-2 bg-white text-gray-500">{{ t('login.or') }}</span>
        </div>
      </div>

      <!-- Google注册 -->
      <button
        @click="handleGoogleLogin"
        :disabled="loading"
        class="w-full py-3 px-4 flex items-center justify-center gap-3 border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition duration-150 disabled:opacity-50"
      >
        <svg class="w-5 h-5" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
        </svg>
        {{ t('register.orRegisterWith') }} Google
      </button>

      <p class="mt-4 text-xs text-gray-500 text-center">
        {{ t('register.terms') }}
      </p>

      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600">
          {{ t('register.hasAccount') }}
          <router-link to="/login" class="text-blue-600 hover:text-blue-800 font-medium transition duration-150">
            {{ t('nav.login') }}
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useI18n } from 'vue-i18n'
import { handleApiError, getErrorMessageKey } from '@/utils/errorHandler'

const router = useRouter()
const userStore = useUserStore()
const { t } = useI18n()

// 邮箱注册表单
const emailForm = ref({
  email: '',
  code: ''
})

// 验证码倒计时
const countdown = ref(0)

// 加载状态
const loading = ref(false)

// 发送验证码
const sendCode = async () => {
  if (!emailForm.value.email) {
    alert('请输入邮箱地址')
    return
  }

  const { success, error } = await userStore.sendVerificationCode(emailForm.value.email)

  if (success) {
    alert('验证码已发送到您的邮箱')
    countdown.value = 60
    const timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  } else {
    const errorResult = handleApiError(error)
    alert(errorResult.message || '发送验证码失败')
  }
}

// 邮箱验证码注册
const handleEmailRegister = async () => {
  if (!emailForm.value.code || emailForm.value.code.length !== 6) {
    alert('请输入6位验证码')
    return
  }

  loading.value = true

  try {
    const { success, error } = await userStore.verifyAndLogin({
      email: emailForm.value.email,
      code: emailForm.value.code
    })

    loading.value = false

    if (success) {
      router.push('/')
    } else {
      const errorResult = handleApiError(error)
      alert(errorResult.message || '注册失败')
    }
  } catch (err) {
    loading.value = false
    const errorResult = handleApiError(err)
    alert(errorResult.message || '注册失败')
  }
}

// Google注册/登录
const handleGoogleLogin = async () => {
  if (typeof google === 'undefined' || !google.accounts) {
    alert('Google登录组件未加载，请刷新页面重试')
    return
  }

  const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID || 'your-google-client-id'

  if (clientId === 'your-google-client-id') {
    alert('Google OAuth未配置，请在环境变量中设置VITE_GOOGLE_CLIENT_ID')
    return
  }

  google.accounts.oauth2.initTokenClient({
    client_id: clientId,
    scope: 'email profile',
    callback: async (response) => {
      if (response.error) {
        console.error('Google login error:', response.error)
        alert('Google登录失败')
        return
      }

      loading.value = true
      const { success, error } = await userStore.googleLogin(response.access_token)
      loading.value = false

      if (success) {
        router.push('/')
      } else {
        const errorResult = handleApiError(error)
        alert(errorResult.message || 'Google登录失败')
      }
    }
  }).requestAccessToken()
}
</script>