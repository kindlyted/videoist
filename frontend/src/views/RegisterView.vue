<template>
  <div class="container mx-auto px-4 py-8 flex justify-center">
    <div class="w-full max-w-md bg-white rounded-lg shadow-md p-6">
      <h2 class="text-2xl font-bold text-center mb-6">注册</h2>
      <form @submit.prevent="handleRegister">
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
        <div class="mb-4">
          <label for="email" class="block text-gray-700 text-sm font-bold mb-2">邮箱</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            placeholder="邮箱地址"
            required
          />
        </div>
        <div class="mb-4">
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
          <label for="password2" class="block text-gray-700 text-sm font-bold mb-2">确认密码</label>
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
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </div>
      </form>
      <div class="mt-4 text-center">
        <p class="text-gray-600">
          已有账户?
          <router-link to="/login" class="text-blue-500 hover:text-blue-800 font-bold">
            点击登录
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

const router = useRouter()
const userStore = useUserStore()

// 表单数据
const form = ref({
  username: '',
  email: '',
  password: '',
  password2: ''
})

// 加载状态
const loading = ref(false)

// 密码确认验证
watch(
  () => form.value.password2,
  (newPassword2) => {
    if (newPassword2 && newPassword2 !== form.value.password) {
      // 可以在这里添加密码不匹配的提示
      console.log('密码不匹配')
    }
  }
)

// 注册方法
const handleRegister = async () => {
  // 简单的密码确认验证
  if (form.value.password !== form.value.password2) {
    alert('两次输入的密码不一致')
    return
  }
  
  loading.value = true
  
  const { success, error } = await userStore.register({
    username: form.value.username,
    email: form.value.email,
    password: form.value.password
  })
  
  loading.value = false
  
  if (success) {
    // 注册成功，跳转到首页
    router.push('/')
  } else {
    // 显示错误信息
    alert(error || '注册失败')
  }
}
</script>