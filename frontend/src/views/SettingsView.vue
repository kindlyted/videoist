<template>
  <div class="container mx-auto px-4 py-8">
    <!-- 页面标题 -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold">{{ $t('settings.title') }}</h1>
      <p class="text-gray-600">{{ $t('settings.description') }}</p>
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
        <h2 class="text-xl font-semibold mb-4">{{ $t('settings.account.title') }}</h2>
        <form @submit.prevent="updateAccount">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
              {{ $t('settings.account.username') }}
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
              {{ $t('settings.account.email') }}
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
              {{ $t('settings.account.avatar') }}
            </label>
            <div class="flex items-center">
              <div class="bg-gray-200 border-2 border-dashed rounded-xl w-16 h-16" />
              <button 
                type="button"
                class="ml-4 bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
              >
                {{ $t('settings.account.uploadAvatar') }}
              </button>
            </div>
          </div>
          
          <div class="flex items-center justify-between">
            <button
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="submit"
            >
              {{ $t('settings.account.saveChanges') }}
            </button>
          </div>
        </form>
      </div>
      
      <!-- 密码设置 -->
      <div v-if="activeTab === 'password'" class="p-6">
        <h2 class="text-xl font-semibold mb-4">{{ $t('settings.password.title') }}</h2>
        <div v-if="passwordMessage" class="mb-4 p-2 rounded" :class="passwordMessageType === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
          {{ passwordMessage }}
        </div>
        <form @submit.prevent="updatePassword">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="currentPassword">
              {{ $t('settings.password.currentPassword') }}
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
              {{ $t('settings.password.newPassword') }}
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
              {{ $t('settings.password.confirmPassword') }}
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
              :disabled="passwordLoading"
            >
              {{ passwordLoading ? $t('settings.password.updating') : $t('settings.password.updatePassword') }}
            </button>
          </div>
        </form>
      </div>
      
      <!-- 通知设置 -->
      <div v-if="activeTab === 'notifications'" class="p-6">
        <h2 class="text-xl font-semibold mb-4">{{ $t('settings.notifications.title') }}</h2>
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-medium">{{ $t('settings.notifications.emailNotifications') }}</h3>
              <p class="text-gray-600 text-sm">{{ $t('settings.notifications.emailDescription') }}</p>
            </div>
            <label class="switch">
              <input type="checkbox" v-model="notificationSettings.email">
              <span class="slider round"></span>
            </label>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-medium">{{ $t('settings.notifications.videoProcessingNotifications') }}</h3>
              <p class="text-gray-600 text-sm">{{ $t('settings.notifications.videoProcessingDescription') }}</p>
            </div>
            <label class="switch">
              <input type="checkbox" v-model="notificationSettings.videoProcessing">
              <span class="slider round"></span>
            </label>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-medium">{{ $t('settings.notifications.systemUpdateNotifications') }}</h3>
              <p class="text-gray-600 text-sm">{{ $t('settings.notifications.systemUpdateDescription') }}</p>
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
            {{ $t('settings.notifications.saveNotificationSettings') }}
          </button>
        </div>
      </div>
      
      <!-- 隐私设置 -->
      <div v-if="activeTab === 'privacy'" class="p-6">
        <h2 class="text-xl font-semibold mb-4">{{ $t('settings.privacy.title') }}</h2>
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-medium">{{ $t('settings.privacy.publicProfile') }}</h3>
              <p class="text-gray-600 text-sm">{{ $t('settings.privacy.publicProfileDescription') }}</p>
            </div>
            <label class="switch">
              <input type="checkbox" v-model="privacySettings.publicProfile">
              <span class="slider round"></span>
            </label>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-medium">{{ $t('settings.privacy.searchVisibility') }}</h3>
              <p class="text-gray-600 text-sm">{{ $t('settings.privacy.searchVisibilityDescription') }}</p>
            </div>
            <label class="switch">
              <input type="checkbox" v-model="privacySettings.searchVisibility">
              <span class="slider round"></span>
            </label>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-medium">{{ $t('settings.privacy.dataCollection') }}</h3>
              <p class="text-gray-600 text-sm">{{ $t('settings.privacy.dataCollectionDescription') }}</p>
            </div>
            <label class="switch">
              <input type="checkbox" v-model="privacySettings.dataCollection">
              <span class="slider round"></span>
            </label>
          </div>
        </div>
        
        <div class="mt-6">
          <button
            @click="savePrivacySettings"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            {{ $t('settings.privacy.savePrivacySettings') }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- 删除账户 -->
    <div class="mt-8 bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-semibold mb-4 text-red-600">{{ $t('settings.dangerZone.title') }}</h2>
      <div class="flex items-center justify-between">
        <div>
          <h3 class="font-medium">{{ $t('settings.dangerZone.deleteAccount') }}</h3>
          <p class="text-gray-600 text-sm">{{ $t('settings.dangerZone.deleteAccountDescription') }}</p>
        </div>
        <button 
          @click="deleteAccount"
          class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
        >
          {{ $t('settings.dangerZone.deleteAccount') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useI18n } from 'vue-i18n'

const userStore = useUserStore()
const { t } = useI18n()

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

// 密码更新状态
const passwordLoading = ref(false)
const passwordMessage = ref('')
const passwordMessageType = ref('') // 'success' or 'error'

// 选项卡
const tabs = [
  { id: 'account', name: t('settings.tabs.account') },
  { id: 'password', name: t('settings.tabs.password') },
  { id: 'notifications', name: t('settings.tabs.notifications') },
  { id: 'privacy', name: t('settings.tabs.privacy') }
]

// 方法
const updateAccount = () => {
  // 这里应该调用API更新账户信息
  console.log('更新账户信息:', accountForm.value)
  alert(t('settings.account.updateSuccess'))
}

const updatePassword = async () => {
  // 重置消息
  passwordMessage.value = ''
  passwordMessageType.value = ''
  
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    passwordMessage.value = t('settings.password.passwordMismatch')
    passwordMessageType.value = 'error'
    return
  }
  
  passwordLoading.value = true
  
  try {
    const { success, message, error } = await userStore.updatePassword({
      current_password: passwordForm.value.currentPassword,
      new_password: passwordForm.value.newPassword
    })
    
    if (success) {
      passwordMessage.value = message || t('settings.password.updateSuccess')
      passwordMessageType.value = 'success'
      
      // 重置表单
      passwordForm.value = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    } else {
      passwordMessage.value = error || t('settings.password.updateFailed')
      passwordMessageType.value = 'error'
    }
  } catch (err) {
    passwordMessage.value = t('settings.password.unknownError')
    passwordMessageType.value = 'error'
  } finally {
    passwordLoading.value = false
  }
}

const saveNotificationSettings = () => {
  // 这里应该调用API保存通知设置
  console.log('保存通知设置:', notificationSettings.value)
  alert(t('settings.notifications.saveSuccess'))
}

const savePrivacySettings = () => {
  // 这里应该调用API保存隐私设置
  console.log('保存隐私设置:', privacySettings.value)
  alert(t('settings.privacy.saveSuccess'))
}

const deleteAccount = () => {
  if (confirm(t('settings.dangerZone.deleteConfirm'))) {
    // 这里应该调用API删除账户
    console.log('删除账户')
    alert(t('settings.dangerZone.deleteSuccess'))
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