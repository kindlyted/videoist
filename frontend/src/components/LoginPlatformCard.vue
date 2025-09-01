<template>
  <div class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>

      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center">
              <LockClosedIcon class="h-5 w-5 mr-2 text-blue-500" />
              <h3 class="text-lg font-medium text-gray-900">平台登录</h3>
            </div>
            <button 
              @click="$emit('close')"
              class="text-gray-400 hover:text-gray-500 focus:outline-none"
            >
              <XMarkIcon class="h-6 w-6" />
            </button>
          </div>
          
          <div class="min-h-[200px] flex items-center justify-center">
            <div class="grid grid-cols-1 gap-4 w-full">
              <button
                v-for="platform in platforms"
                :key="platform.id"
                class="bg-white hover:bg-gray-50 border rounded-lg p-4 flex items-center justify-between"
                @click="$emit('select-platform', platform.id)"
              >
                <div class="flex items-center">
                  <component 
                    :is="platform.icon" 
                    class="h-8 w-8 mr-3 text-gray-600"
                  />
                  <div>
                    <h3 class="font-medium">{{ platform.name }}</h3>
                    <p class="text-sm text-gray-500">点击登录{{ platform.name }}</p>
                  </div>
                </div>
                <ChevronRightIcon class="h-5 w-5 text-gray-400" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { 
  VideoCameraIcon, 
  HeartIcon, 
  ChatBubbleLeftRightIcon,
  ChevronRightIcon,
  LockClosedIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

const platforms = [
  {
    id: 'douyin',
    name: '抖音',
    icon: VideoCameraIcon
  },
  {
    id: 'xiaohongshu',
    name: '小红书',
    icon: HeartIcon
  },
  {
    id: 'shipinhao',
    name: '视频号',
    icon: ChatBubbleLeftRightIcon
  }
]

defineEmits(['select-platform', 'close'])
</script>