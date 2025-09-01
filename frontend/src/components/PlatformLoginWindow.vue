<template>
  <div class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>

      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center">
              <LockClosedIcon class="h-5 w-5 mr-2 text-blue-500" />
              <h3 class="text-lg font-medium text-gray-900">{{ platformName }}登录</h3>
            </div>
            <button 
              @click="$emit('login-error', new Error('用户取消登录'))"
              class="text-gray-400 hover:text-gray-500 focus:outline-none"
            >
              <XMarkIcon class="h-6 w-6" />
            </button>
          </div>
          
          <div class="min-h-[200px] flex items-center justify-center" v-if="!loginStarted">
            <button 
              @click="startLogin"
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            >
              点击启动{{ platformName }}登录
            </button>
          </div>
          
          <div class="min-h-[200px] flex items-center justify-center" v-else>
            <div class="text-center">
              <SpinnerIcon class="h-10 w-10 mx-auto text-blue-500" />
              <p class="mt-2">正在启动{{ platformName }}登录，请稍候...</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { LockClosedIcon, XMarkIcon } from '@heroicons/vue/24/solid'
import SpinnerIcon from '@/components/SpinnerIcon.vue'
import api from '@/services/api'

const props = defineProps({
  platform: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['login-success', 'login-error'])

const platformNames = {
  'xiaohongshu': '小红书',
  'douyin': '抖音',
  'shipinhao': '视频号'
}

const platformName = ref(platformNames[props.platform])
const loginStarted = ref(false)

const startLogin = async () => {
  loginStarted.value = true
  
  try {
    const response = await api.post('/platform-login', {
      platform: props.platform
    })
    
    if (response.data.success) {
      emit('login-success')
    } else {
      emit('login-error', new Error(response.data.error || '登录失败'))
    }
  } catch (error) {
    console.error('启动登录失败:', error)
    emit('login-error', error)
  }
}
</script>
