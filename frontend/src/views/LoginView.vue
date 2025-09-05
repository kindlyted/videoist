<template>
  <div class="container mx-auto px-4 py-8 flex justify-center">
    <div class="w-full max-w-md bg-white rounded-lg shadow-md p-6">
      <h2 class="text-2xl font-bold text-center mb-6">{{ $t('login.title') }}</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label for="username" class="block text-gray-700 text-sm font-bold mb-2">{{ $t('login.username') }}</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            :placeholder="$t('login.username')"
            required
          />
        </div>
        <div class="mb-6">
          <label for="password" class="block text-gray-700 text-sm font-bold mb-2">{{ $t('login.password') }}</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
            :placeholder="$t('login.password')"
            required
          />
        </div>
        <div class="mb-6">
          <label class="flex items-center">
            <input
              v-model="form.rememberMe"
              type="checkbox"
              class="form-checkbox h-4 w-4 text-blue-600 transition duration-150 ease-in-out"
            />
            <span class="ml-2 text-sm text-gray-600">{{ $t('login.rememberMe') }}</span>
          </label>
        </div>
        <div class="flex items-center justify-between">
          <button
            type="submit"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            :disabled="loading"
          >
            {{ loading ? $t('login.loggingIn') : $t('nav.login') }}
          </button>
          <router-link
            to="/reset-password"
            class="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800"
          >
            {{ $t('login.forgotPassword') }}
          </router-link>
        </div>
      </form>
      <div class="mt-4 text-center">
        <p class="text-gray-600">
          {{ $t('login.noAccount') }}
          <router-link to="/register" class="text-blue-500 hover:text-blue-800 font-bold">
            {{ $t('nav.register') }}
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

// 表单数据
const form = ref({
  username: '',
  password: '',
  rememberMe: false
})

// 加载状态
const loading = ref(false)

// 登录方法
const handleLogin = async () => {
  loading.value = true
  
  try {
    const { success, error } = await userStore.login({
      username: form.value.username,
      password: form.value.password
    })
    
    loading.value = false
    
    if (success) {
      // 登录成功，跳转到首页
      router.push('/')
    } else {
      // 处理错误信息
      const errorResult = handleApiError(error);
      let errorMessage = '';
      
      if (errorResult.message) {
        errorMessage = errorResult.message;
      } else if (errorResult.messageKey) {
        errorMessage = t(errorResult.messageKey);
      } else if (errorResult.errorCode) {
        errorMessage = t(getErrorMessageKey(errorResult.errorCode));
      }
      
      alert(errorMessage || t('login.loginFailed'));
    }
  } catch (err) {
    loading.value = false
    // 处理网络错误等异常情况
    const errorResult = handleApiError(err);
    let errorMessage = '';
    
    if (errorResult.message) {
      errorMessage = errorResult.message;
    } else if (errorResult.messageKey) {
      errorMessage = t(errorResult.messageKey);
    } else if (errorResult.errorCode) {
      errorMessage = t(getErrorMessageKey(errorResult.errorCode));
    }
    
    alert(errorMessage || t('login.loginFailed'));
  }
}
</script>