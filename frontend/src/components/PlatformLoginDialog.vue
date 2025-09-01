<template>
  <div v-if="showModal" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- 背景遮罩 -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>

      <!-- 模态框内容 -->
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <!-- 标题 -->
          <div class="flex items-center mb-4">
            <LockClosedIcon class="h-5 w-5 mr-2 text-blue-500" />
            <h3 class="text-lg leading-6 font-medium text-gray-900">平台登录</h3>
          </div>

          <div class="text-sm text-gray-600 mb-4">
            以下平台需要登录后才能上传视频：
          </div>

          <!-- 平台列表 -->
          <div class="space-y-4">
            <div v-for="platform in invalidPlatforms" :key="platform" class="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div class="flex items-center">
                <component 
                  :is="getPlatformIcon(platform)" 
                  class="h-5 w-5 mr-2" 
                  :class="getIconColor(platform)"
                />
                <span class="text-gray-700">{{ getPlatformName(platform) }}</span>
              </div>
              <button 
                :class="[
                  'inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed',
                  { 'opacity-75 cursor-not-allowed': isLoggingIn }
                ]"
                :disabled="isLoggingIn === platform"
                @click="openLoginWindow(platform)"
              >
                <span v-if="isLoggingIn === platform" class="mr-2">
                  <!-- 加载动画 -->
                  <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </span>
                {{ isLoggingIn === platform ? "等待登录..." : "开始登录" }}
              </button>
            </div>
          </div>
        </div>

        <!-- 底部按钮 -->
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button 
            type="button" 
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:w-auto sm:text-sm"
            @click="close"
          >
            关闭
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { LockClosedIcon, DocumentIcon, MusicalNoteIcon, VideoCameraIcon, QuestionMarkCircleIcon } from "@heroicons/vue/24/solid"
import api from "@/services/api"

const props = defineProps({
  invalidPlatforms: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(["update:invalidPlatforms", "login-success"])

const showModal = ref(true)
const isLoggingIn = ref(null)

// 平台图标和名称映射
const platformInfo = {
  xiaohongshu: {
    name: "小红书",
    icon: DocumentIcon,
    color: "text-red-500"
  },
  douyin: {
    name: "抖音",
    icon: MusicalNoteIcon,
    color: "text-black"
  },
  shipinhao: {
    name: "视频号",
    icon: VideoCameraIcon,
    color: "text-green-500"
  }
}

const getPlatformName = (platform) => {
  return platformInfo[platform]?.name || platform
}

const getPlatformIcon = (platform) => {
  return platformInfo[platform]?.icon || QuestionMarkCircleIcon
}

const getIconColor = (platform) => {
  return platformInfo[platform]?.color || "text-gray-500"
}

const openLoginWindow = async (platform) => {
  const url = PLATFORM_LOGIN_URLS[platform]
  if (!url) {
    alert(`未找到${getPlatformName(platform)}的登录地址`)
    return
  }
  
  isLoggingIn.value = platform
  window.open(url, `${platform}Login`, 'width=800,height=600')
  
  // 开始轮询检查登录状态
  const checkLoginStatus = async () => {
    try {
      const response = await api.get('/check-platform-login', {
        params: { platform }
      })

      if (response.data.is_logged_in) {
        alert(`${getPlatformName(platform)}登录成功`)
        const updatedPlatforms = props.invalidPlatforms.filter(p => p !== platform)
        emit("update:invalidPlatforms", updatedPlatforms)
        
        if (updatedPlatforms.length === 0) {
          emit("login-success")
          showModal.value = false
        }
        return true
      }
      return false
    } catch (error) {
      console.error('检查登录状态失败:', error)
      return false
    }
  }

  // 每2秒检查一次，最多等待2分钟
  let attempts = 0
  const maxAttempts = 60
  const interval = setInterval(async () => {
    if (attempts >= maxAttempts) {
      clearInterval(interval)
      alert(`${getPlatformName(platform)}登录超时，请重试`)
      isLoggingIn.value = null
      return
    }

    const success = await checkLoginStatus()
    if (success) {
      clearInterval(interval)
      isLoggingIn.value = null
    }
    attempts++
  }, 2000)
    
}

const close = () => {
  showModal.value = false
}

defineExpose({
  show: () => {
    showModal.value = true
  }
})
</script>
