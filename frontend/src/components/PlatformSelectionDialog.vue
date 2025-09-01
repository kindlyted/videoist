<!-- 平台选择对话框组件 -->
<template>
  <Modal 
    :visible="true"
    title="选择要登录的平台"
    @close="$emit('close')"
    size="md"
  >
    <div class="grid grid-cols-1 gap-4">
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
            <p class="text-sm text-gray-500">{{ platform.description }}</p>
          </div>
        </div>
        <ChevronRightIcon class="h-5 w-5 text-gray-400" />
      </button>
    </div>
  </Modal>
</template>

<script setup>
import Modal from './Modal.vue'
import { 
  VideoCameraIcon, 
  HeartIcon, 
  ChatBubbleLeftRightIcon,
  ChevronRightIcon 
} from '@heroicons/vue/24/outline'

const platforms = [
  {
    id: 'douyin',
    name: '抖音',
    description: '抖音创作者平台',
    icon: VideoCameraIcon
  },
  {
    id: 'xiaohongshu',
    name: '小红书',
    description: '小红书创作者平台',
    icon: HeartIcon
  },
  {
    id: 'shipinhao',
    name: '视频号',
    description: '视频号平台',
    icon: ChatBubbleLeftRightIcon
  }
]

defineEmits(['select-platform', 'close'])
</script>
