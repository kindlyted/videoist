<template>
  <div class="container mx-auto px-4 py-8 flex justify-center">
    <div class="w-full max-w-md bg-white rounded-lg shadow-md p-8">
      <h2 class="text-2xl font-bold text-center mb-8">{{ t('register.title') }}</h2>

      <!-- 邮箱密码注册表单 -->
      <form @submit.prevent="handleRegister" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('register.email') }}</label>
          <div class="relative">
            <input
              v-model="form.email"
              type="email"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-150"
              placeholder="your@email.com"
              required
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('register.password') }}</label>
          <div class="relative">
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-150"
              :placeholder="t('register.password')"
              required
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute inset-y-0 right-0 pr-3 flex items-center cursor-pointer"
            >
              <!-- Eye open icon -->
              <svg v-if="!showPassword" class="h-5 w-5 text-gray-500 hover:text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <!-- Eye slash icon -->
              <svg v-else class="h-5 w-5 text-gray-500 hover:text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
              </svg>
            </button>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('register.confirmPassword') }}</label>
          <div class="relative">
            <input
              v-model="form.password2"
              :type="showConfirmPassword ? 'text' : 'password'"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-150"
              :placeholder="t('register.confirmPassword')"
              required
            />
            <button
              type="button"
              @click="showConfirmPassword = !showConfirmPassword"
              class="absolute inset-y-0 right-0 pr-3 flex items-center cursor-pointer"
            >
              <!-- Eye open icon -->
              <svg v-if="!showConfirmPassword" class="h-5 w-5 text-gray-500 hover:text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <!-- Eye slash icon -->
              <svg v-else class="h-5 w-5 text-gray-500 hover:text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
              </svg>
            </button>
          </div>
          <p v-if="passwordError" class="mt-1 text-sm text-red-600">{{ passwordError }}</p>
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

      <!-- 第三方注册 -->
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
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useI18n } from 'vue-i18n'
import { handleApiError, getErrorMessageKey } from '@/utils/errorHandler'

const router = useRouter()
const userStore = useUserStore()
const { t } = useI18n()

// 注册表单
const form = ref({
  email: '',
  password: '',
  password2: ''
})

// 密码显示状态
const showPassword = ref(false)
const showConfirmPassword = ref(false)

// 错误信息
const passwordError = ref('')

// 加载状态
const loading = ref(false)

// 密码确认验证
watch(
  () => form.value.password2,
  (newPassword2) => {
    if (newPassword2 && newPassword2 !== form.value.password) {
      passwordError.value = t('register.passwordMismatch')
    } else {
      passwordError.value = ''
    }
  }
)

// 注册方法
const handleRegister = async () => {
  // 密码确认验证
  if (form.value.password !== form.value.password2) {
    alert(t('register.passwordMismatch'))
    return
  }

  // 密码长度验证
  if (form.value.password.length < 6) {
    alert(t('register.passwordTooShort'))
    return
  }

  loading.value = true

  try {
    const { success, error } = await userStore.register({
      email: form.value.email,
      password: form.value.password
    })

    loading.value = false

    if (success) {
      // 注册成功，提示用户去邮箱激活
      alert(t('register.activationSent'))
      // 跳转到登录页
      router.push('/login')
    } else {
      // 处理错误信息
      const errorResult = handleApiError(error)
      alert(errorResult.message || t('register.registrationFailed'))
    }
  } catch (err) {
    loading.value = false
    const errorResult = handleApiError(err)
    alert(errorResult.message || t('register.registrationFailed'))
  }
}

// Google注册/登录
const handleGoogleLogin = async () => {
  if (typeof google === 'undefined' || !google.accounts) {
    alert(t('register.googleSdkNotLoaded'))
    return
  }

  const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID || 'your-google-client-id'

  if (clientId === 'your-google-client-id') {
    alert(t('register.googleNotConfigured'))
    return
  }

  google.accounts.oauth2.initTokenClient({
    client_id: clientId,
    scope: 'email profile',
    callback: async (response) => {
      if (response.error) {
        console.error('Google login error:', response.error)
        alert(t('register.googleLoginFailed'))
        return
      }

      loading.value = true
      const { success, error } = await userStore.googleLogin(response.access_token)
      loading.value = false

      if (success) {
        router.push('/')
      } else {
        const errorResult = handleApiError(error)
        alert(errorResult.message || t('register.googleLoginFailed'))
      }
    }
  }).requestAccessToken()
}
</script>