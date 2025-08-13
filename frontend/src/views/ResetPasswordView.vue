<template>
  <div class="container mx-auto px-4 py-8 flex justify-center">
    <div class="w-full max-w-md bg-white rounded-lg shadow-md p-6">
      <h2 class="text-2xl font-bold text-center mb-6">重置密码</h2>
      <form @submit.prevent="handleResetPassword">
        <div class="mb-4">
          <label for="email" class="block text-gray-700 text-sm font-bold mb-2">邮箱地址</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            placeholder="您的邮箱地址"
            required
          />
        </div>
        <div class="flex items-center justify-between">
          <button
            type="submit"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            :disabled="loading"
          >
            {{ loading ? '发送中...' : '发送重置链接' }}
          </button>
        </div>
      </form>
      <div class="mt-4 text-center">
        <p class="text-gray-600">
          想起来了?
          <router-link to="/login" class="text-blue-500 hover:text-blue-800 font-bold">
            点击登录
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
  email: ''
})

// 加载状态
const loading = ref(false)

// 重置密码方法
const handleResetPassword = async () => {
  loading.value = true
  
  const { success, message, error } = await userStore.resetPassword(form.value.email)
  
  if (success) {
    // 显示成功信息
    alert(message || '重置链接已发送到您的邮箱')
    
    // 跳转到登录页面
    router.push('/login')
  } else {
    // 显示错误信息
    alert(error || '操作失败')
  }
  
  loading.value = false
}
</script>