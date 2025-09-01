<template>
  <div class="card h-full flex flex-col mx-auto w-full max-w-sm">
    <Modal 
      v-model:visible="showPreviewModal" 
      :title="t('videoCard.previewModalTitle')" 
      size="lg"
      custom-class="video-preview-modal"
      :show-close-button="true"
      :show-footer="false"
    >
      <div class="video-container">
        <video 
          v-if="currentVideoUrl" 
          controls 
          class="w-full max-h-[80vh]"
          autoplay
        >
          <source :src="currentVideoUrl" type="video/mp4">
          {{ t('videoCard.noVideoSupport') }}
        </video>
        <div v-else class="text-center py-4">
          <!-- 视频加载失败，请检查链接是否有效。 -->
        </div>
      </div>
    </Modal>
    <div class="relative pb-[75%] h-0 overflow-hidden rounded-t-lg">
      <img 
        :src="video.thumbnail" 
        :alt="video.title" 
        class="absolute inset-0 w-full h-full object-contain"
      />
      <div class="absolute bottom-2 right-2 bg-black bg-opacity-70 text-white text-xs px-2 py-1 rounded">
        {{ formatDuration(video.duration) }}
      </div>
      <div v-if="video.status === 'processing'" class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="text-white text-center">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-white"></div>
          <p class="mt-2">{{ t('videoCard.processing') }}</p>
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
            @click="openPreviewModal(video)"
            class="btn btn-primary text-sm"
          >
            {{ t('videoCard.preview') }}
          </button>
          <button 
            v-if="showEdit" 
            @click="$emit('upload', video)"
            class="btn btn-secondary text-sm"
          >
            {{ t('videoCard.upload') }}
          </button>
          <button 
            v-if="showDelete" 
            @click="$emit('delete', video)"
            class="btn btn-danger text-sm"
          >
            {{ t('videoCard.delete') }}
          </button>
        </div>
        <div v-if="showDownload" class="flex space-x-2">
          <button 
            @click="$emit('download', video)"
            class="text-gray-500 hover:text-gray-700"
            :title="t('videoCard.download')"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
          <button 
            @click="$emit('share', video)"
            class="text-gray-500 hover:text-gray-700"
            :title="t('videoCard.share')"
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
import { ref } from 'vue';
import { useI18n } from 'vue-i18n'
import Modal from './Modal.vue';

// 初始化国际化
const { t } = useI18n()

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
const emit = defineEmits(['preview', 'edit', 'delete', 'download', 'share', 'upload'])

// 预览模态框状态
const showPreviewModal = ref(false)
const currentVideoUrl = ref('')

// 打开预览模态框
const openPreviewModal = (video) => {
  currentVideoUrl.value = video.videoUrl || ''
  showPreviewModal.value = true
}

defineExpose({ openPreviewModal })

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
    'draft': t('videoCard.draft'),
    'processing': t('videoCard.processing'),
    'published': t('videoCard.published'),
    'failed': t('videoCard.failed')
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


<style scoped>
.video-preview-modal {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  background-color: rgba(0, 0, 0, 0.5) !important;
  z-index: 1000 !important;
  margin: 0 !important;
  padding: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.video-preview-modal .inline-block.align-bottom {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 90vw !important;
  max-width: 90vw !important;
  height: 90vh !important;
  max-height: 90vh !important;
  background-color: transparent !important;
  box-shadow: none !important;
  margin: 0 auto !important;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .video-preview-modal .inline-block.align-bottom {
    width: 95vw !important;
    max-width: 95vw !important;
    height: 95vh !important;
    max-height: 95vh !important;
  }
  
  .video-preview-modal video {
    max-width: 95vw !important;
    max-height: 85vh !important;
  }
}

/* 桌面端优化 */
@media (min-width: 1024px) {
  .video-preview-modal .inline-block.align-bottom {
    width: 80vw !important;
    max-width: 1200px !important;
    height: 80vh !important;
    max-height: 800px !important;
  }
  
  .video-preview-modal video {
    max-width: 75vw !important;
    max-height: 70vh !important;
  }
}

.video-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.video-preview-modal video {
  max-width: 90vw !important;
  max-height: 80vh !important;
  width: auto !important;
  height: auto !important;
}
</style>