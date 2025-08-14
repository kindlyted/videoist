<template>
  <div class="card h-full flex flex-col">
    <div class="relative pb-[133.33%] h-0 overflow-hidden rounded-t-lg">
      <img 
        :src="video.thumbnail" 
        :alt="video.title" 
        class="absolute inset-0 w-full h-full object-cover"
      >
      <div class="absolute bottom-2 right-2 bg-black bg-opacity-70 text-white text-xs px-2 py-1 rounded">
        {{ formatDuration(video.duration) }}
      </div>
      <div v-if="video.status === 'processing'" class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="text-white text-center">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-white"></div>
          <p class="mt-2">处理中...</p>
        </div>
      </div>
    </div>
    <div class="card-body flex-grow flex flex-col">
      <h3 class="card-title text-truncate mb-2">{{ video.title }}</h3>
      <p class="text-gray-600 text-sm mb-3 flex-grow text-truncate">{{ video.description }}</p>
      <div class="flex justify-between items-center text-sm text-gray-500 mb-3">
        <span>{{ formatDate(video.createdAt) }}</span>
        <span class="badge" :class="getStatusClass(video.status)">
          {{ getStatusText(video.status) }}
        </span>
      </div>
      <div class="flex justify-between items-center mt-auto">
        <div class="flex space-x-2">
          <button 
            v-if="showPreview" 
            @click="$emit('preview', video)"
            :disabled="disabled"
            class="btn btn-primary text-sm"
            :class="{ 'opacity-50 cursor-not-allowed': disabled }"
          >
            预览
          </button>
          <button 
            v-if="showEdit" 
            @click="$emit('edit', video)"
            class="btn btn-secondary text-sm"
          >
            编辑
          </button>
          <button 
            v-if="showDelete" 
            @click="$emit('delete', video)"
            class="btn btn-danger text-sm"
          >
            删除
          </button>
        </div>
        <div v-if="showDownload" class="flex space-x-2">
          <button 
            @click="$emit('download', video)"
            class="text-gray-500 hover:text-gray-700"
            title="下载"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
          <button 
            @click="$emit('share', video)"
            class="text-gray-500 hover:text-gray-700"
            title="分享"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

// 定义属性
const props = defineProps({
  video: {
    type: Object,
    required: true
  },
  showPreview: {
    type: Boolean,
    default: true
  },
  showEdit: {
    type: Boolean,
    default: false
  },
  showDelete: {
    type: Boolean,
    default: false
  },
  showDownload: {
    type: Boolean,
    default: true
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

// 定义事件
const emit = defineEmits(['preview', 'edit', 'delete', 'download', 'share'])

// 格式化日期
const formatDate = (date) => {
  return new Date(date).toLocaleDateString('zh-CN')
}

// 格式化时长
const formatDuration = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs < 10 ? '0' : ''}${secs}`
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    'draft': '草稿',
    'processing': '处理中',
    'published': '已发布',
    'failed': '失败'
  }
  return statusMap[status] || status
}

// 获取状态样式类
const getStatusClass = (status) => {
  const classMap = {
    'draft': 'badge-secondary',
    'processing': 'badge-warning',
    'published': 'badge-success',
    'failed': 'badge-danger'
  }
  return classMap[status] || 'badge-secondary'
}
</script>