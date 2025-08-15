<template>
  <div class="container mx-auto px-4 py-8 flex justify-center">
    <div class="w-full max-w-md bg-white rounded-lg shadow-md p-6">
      <h2 class="text-2xl font-bold text-center mb-6">重置密码</h2>
      <form @submit.prevent="handleResetPasswordConfirm">
        <div class="mb-4">
          <label for="password" class="block text-gray-700 text-sm font-bold mb-2">新密码</label>
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
          <label for="password2" class="block text-gray-700 text-sm font-bold mb-2">确认新密码</label>
          <input
            id="password2"
            v-model="form.password2"
            type="password"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
            placeholder="******************"
            required
          />
        </div>
        <div class="flex items-center justify-between">
          <button
            type="submit"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            :disabled="loading"
          >
            {{ loading ? '重置中...' : '重置密码' }}
          </button>
        </div>
      </form>
      <div v-if="message" class="mt-4 p-2 bg-green-100 text-green-700 rounded">
        {{ message }}
      </div>
      <div v-if="error" class="mt-4 p-2 bg-red-100 text-red-700 rounded">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/services/api'

const router = useRouter()
const route = useRoute()

// 表单数据
const form = ref({
  password: '',
  password2: ''
})

// 加载状态
const loading = ref(false)

// 消息和错误状态
const message = ref('')
const error = ref('')

// 重置消息和错误
const resetMessages = () => {
  message.value = ''
  error.value = ''
}

// 重置密码确认方法
const handleResetPasswordConfirm = async () => {
  resetMessages()
  
  // 简单的密码确认验证
  if (form.value.password !== form.value.password2) {
    error.value = '两次输入的密码不一致'
    return
  }
  
  loading.value = true
  
  try {
    // 获取URL中的token参数
    const token = route.params.token
    
    // 调用后端重置密码确认接口
    const response = await api.post(`/reset-password/${token}`, {
      password: form.value.password
    })
    
    // 显示成功信息
    message.value = response.data.message || '密码重置成功'
    
    // 3秒后跳转到登录页面
    setTimeout(() => {
      router.push('/login')
    }, 3000)
  } catch (err) {
    // 显示错误信息
    error.value = err.response?.data?.message || '操作失败'
  } finally {
    loading.value = false
  }
}
</script>