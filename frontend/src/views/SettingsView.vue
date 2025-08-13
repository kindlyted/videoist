<template>
  <div class="container mx-auto px-4 py-8">
    <!-- 页面标题 -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold">设置</h1>
      <p class="text-gray-600">管理您的账户设置和偏好</p>
    </div>
    
    <!-- 设置选项卡 -->
    <div class="bg-white rounded-lg shadow-md overflow-hidden">
      <div class="border-b border-gray-200">
        <nav class="flex -mb-px">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'py-4 px-6 text-center border-b-2 font-medium text-sm',
              activeTab === tab.id
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            {{ tab.name }}
          </button>
        </nav>
      </div>
      
      <!-- 账户设置 -->
      <div v-if="activeTab === 'account'" class="p-6">
        <h2 class="text-xl font-semibold mb-4">账户设置</h2>
        <form @submit.prevent="updateAccount">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
              用户名
            </label>
            <input
              id="username"
              v-model="accountForm.username"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              type="text"
              required
            />
          </div>
          
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="email">
              邮箱
            </label>
            <input
              id="email"
              v-model="accountForm.email"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              type="email"
              required
            />
          </div>
          
          <div class="mb-6">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="avatar">
              头像
            </label>
            <div class="flex items-center">
              <div class="bg-gray-200 border-2 border-dashed rounded-xl w-16 h-16" />
              <button 
                type="button"
                class="ml-4 bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
              >
                上传新头像
              </button>
            </div>
          </div>
          
          <div class="flex items-center justify-between">
            <button
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="submit"
            >
              保存更改
            </button>
          </div>
        </form>
      </div>
      
      <!-- 密码设置 -->
      <div v-if="activeTab === 'password'" class="p-6">
        <h2 class="text-xl font-semibold mb-4">密码设置</h2>
        <form @submit.prevent="updatePassword">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="currentPassword">
              当前密码
            </label>
            <input
              id="currentPassword"
              v-model="passwordForm.currentPassword"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              type="password"
              required
            />
          </div>
          
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="newPassword">
              新密码
            </label>
            <input
              id="newPassword"
              v-model="passwordForm.newPassword"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              type="password"
              required
            />
          </div>
          
          <div class="mb-6">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="confirmPassword">
              确认新密码
            </label>
            <input
              id="confirmPassword"
              v-model="passwordForm.confirmPassword"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              type="password"
              required
            />
          </div>
          
          <div class="flex items-center justify-between">
            <button
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="submit"
            >
              更新密码
            </button>
          </div>
        </form>
      </div>
      
      <!-- 通知设置 -->
      <div v-if="activeTab === 'notifications'" class="p-6">
        <h2 class="text-xl font-semibold mb-4">通知设置</h2>
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-medium">邮件通知</h3>
              <p class="text-gray-600 text-sm">接收重要账户更新的邮件</p>
            </div>
            <label class="switch">
              <input type="checkbox" v-model="notificationSettings.email">
              <span class="slider round"></span>
            </label>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-medium">视频处理完成通知</h3>
              <p class="text-gray-600 text-sm">视频处理完成后接收通知</p>
            </div>
            <label class="switch">
              <input type="checkbox" v-model="notificationSettings.videoProcessing">
              <span class="slider round"></span>
            </label>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-medium">系统更新通知</h3>
              <p class="text-gray-600 text-sm">接收系统更新和新功能通知</p>
            </div>
            <label class="switch">
              <input type="checkbox" v-model="notificationSettings.systemUpdates">
              <span class="slider round"></span>
            </label>
          </div>
        </div>
        
        <div class="mt-6">
          <button
            @click="saveNotificationSettings"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            保存通知设置
          </button>
        </div>
      </div>
      
      <!-- 隐私设置 -->
      <div v-if="activeTab === 'privacy'" class="p-6">
        <h2 class="text-xl font-semibold mb-4">隐私设置</h2>
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-medium">公开个人资料</h3>
              <p class="text-gray-600 text-sm">允许其他用户查看您的个人资料</p>
            </div>
            <label class="switch">
              <input type="checkbox" v-model="privacySettings.publicProfile">
              <span class="slider round"></span>
            </label>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-medium">显示创作历史</h3>
              <p class="text-gray-600 text-sm">在个人资料中显示您的视频创作历史</p>
            </div>
            <label class="switch">
              <input type="checkbox" v-model="privacySettings.showCreationHistory">
              <span class="slider round"></span>
            </label>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-medium">允许评论</h3>
              <p class="text-gray-600 text-sm">允许用户在您的视频下发表评论</p>
            </div>
            <label class="switch">
              <input type="checkbox" v-model="privacySettings.allowComments">
              <span class="slider round"></span>
            </label>
          </div>
        </div>
        
        <div class="mt-6">
          <button
            @click="savePrivacySettings"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            保存隐私设置
          </button>
        </div>
      </div>
    </div>
    
    <!-- 删除账户 -->
    <div class="mt-8 bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-semibold mb-4 text-red-600">危险操作</h2>
      <div class="flex items-center justify-between">
        <div>
          <h3 class="font-medium">删除账户</h3>
          <p class="text-gray-600 text-sm">永久删除您的账户和所有相关数据</p>
        </div>
        <button 
          @click="deleteAccount"
          class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
        >
          删除账户
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 状态
const activeTab = ref('account')

// 表单数据
const accountForm = ref({
  username: userStore.user?.username || '',
  email: userStore.user?.email || ''
})

const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const notificationSettings = ref({
  email: true,
  videoProcessing: true,
  systemUpdates: false
})

const privacySettings = ref({
  publicProfile: true,
  showCreationHistory: true,
  allowComments: true
})

// 选项卡
const tabs = [
  { id: 'account', name: '账户' },
  { id: 'password', name: '密码' },
  { id: 'notifications', name: '通知' },
  { id: 'privacy', name: '隐私' }
]

// 方法
const updateAccount = () => {
  // 这里应该调用API更新账户信息
  console.log('更新账户信息:', accountForm.value)
  alert('账户信息已更新')
}

const updatePassword = () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    alert('新密码和确认密码不匹配')
    return
  }
  
  // 这里应该调用API更新密码
  console.log('更新密码:', passwordForm.value)
  alert('密码已更新')
  
  // 重置表单
  passwordForm.value = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
}

const saveNotificationSettings = () => {
  // 这里应该调用API保存通知设置
  console.log('保存通知设置:', notificationSettings.value)
  alert('通知设置已保存')
}

const savePrivacySettings = () => {
  // 这里应该调用API保存隐私设置
  console.log('保存隐私设置:', privacySettings.value)
  alert('隐私设置已保存')
}

const deleteAccount = () => {
  if (confirm('确定要永久删除您的账户吗？此操作无法撤销。')) {
    // 这里应该调用API删除账户
    console.log('删除账户')
    alert('账户已删除')
  }
}
</script>

<style scoped>
/* 开关样式 */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>