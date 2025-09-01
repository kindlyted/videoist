<template>
  <div class="container mx-auto px-4 py-8 flex justify-center">
    <div class="w-full max-w-md bg-white rounded-lg shadow-md p-6">
      <h2 class="text-2xl font-bold text-center mb-6">{{ $t('resetPassword.title') }}</h2>
      <form @submit.prevent="handleResetPassword">
        <div class="mb-4">
          <label for="email" class="block text-gray-700 text-sm font-bold mb-2">{{ $t('resetPassword.email') }}</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            :placeholder="$t('resetPassword.emailPlaceholder')"
            required
          />
        </div>
        <div class="flex items-center justify-between">
          <button
            type="submit"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            :disabled="loading"
          >
            {{ loading ? $t('resetPassword.sending') : $t('resetPassword.sendResetLink') }}
          </button>
        </div>
      </form>
      <div class="mt-4 text-center">
        <p class="text-gray-600">
          {{ $t('resetPassword.rememberedPassword') }}
          <router-link to="/login" class="text-blue-500 hover:text-blue-800 font-bold">
            {{ $t('resetPassword.clickToLogin') }}
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

const router = useRouter()
const userStore = useUserStore()
const { t } = useI18n()

// 表单数据
const form = ref({
  email: ''
})

// 加载状态
const loading = ref(false)

// 重置密码方法
const handleResetPassword = async () => {
  loading.value = true
  
  const { success, message, error, resetUrl } = await userStore.resetPassword(form.value.email)
  
  if (success) {
    // 显示成功信息和重置链接
    alert(message || t('resetPassword.resetLinkSent'))
    
    // 如果有重置链接（仅用于测试），显示它
    if (resetUrl) {
      alert(t('resetPassword.testResetLink') + `: ${resetUrl}`)
    }
    
    // 跳转到登录页面
    router.push('/login')
  } else {
    // 显示错误信息
    alert(error || t('resetPassword.operationFailed'))
  }
  
  loading.value = false
}
</script>