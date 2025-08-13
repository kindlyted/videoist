<template>
  <div class="container mx-auto px-4 py-8 flex justify-center">
    <div class="w-full max-w-md bg-white rounded-lg shadow-md p-6">
      <h2 class="text-2xl font-bold text-center mb-6">登录</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label for="username" class="block text-gray-700 text-sm font-bold mb-2">用户名</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            placeholder="用户名"
            required
          />
        </div>
        <div class="mb-6">
          <label for="password" class="block text-gray-700 text-sm font-bold mb-2">密码</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
            placeholder="******************"
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
            <span class="ml-2 text-sm text-gray-600">记住我</span>
          </label>
        </div>
        <div class="flex items-center justify-between">
          <button
            type="submit"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            :disabled="loading"
          >
            {{ loading ? '登录中...' : '登录' }}
          </button>
          <router-link
            to="/reset-password"
            class="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800"
          >
            忘记密码?
          </router-link>
        </div>
      </form>
      <div class="mt-4 text-center">
        <p class="text-gray-600">
          还没有账户?
          <router-link to="/register" class="text-blue-500 hover:text-blue-800 font-bold">
            点击注册
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

const router = useRouter()
const userStore = useUserStore()

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
  
  const { success, error } = await userStore.login({
    username: form.value.username,
    password: form.value.password
  })
  
  loading.value = false
  
  if (success) {
    // 登录成功，跳转到首页
    router.push('/')
  } else {
    // 显示错误信息
    alert(error || '登录失败')
  }
}
</script>