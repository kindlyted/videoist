<template>
  <div class="px-container py-container">
    <div class="mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
      <h1 class="text-2xl font-bold text-gray-900">{{ t('videoList.title') }}</h1>
      <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3 w-full sm:w-auto">
        <input 
          v-model="searchQuery" 
          type="text" 
          :placeholder="t('videoList.searchPlaceholder')" 
          class="form-input w-full sm:w-64"
        >
        <select 
          v-model="statusFilter" 
          class="form-select w-full sm:w-auto"
        >
          <option value="">{{ t('videoList.statusAll') }}</option>
          <option value="draft">{{ t('videoList.statusDraft') }}</option>
          <option value="processing">{{ t('videoList.statusProcessing') }}</option>
          <option value="published">{{ t('videoList.statusPublished') }}</option>
          <option value="failed">{{ t('videoList.statusFailed') }}</option>
        </select>
        <button 
          @click="fetchVideos" 
          class="btn btn-primary w-full sm:w-auto"
        >
          {{ t('videoList.refresh') }}
        </button>
      </div>
    </div>
    
    <div v-if="loading" class="text-center py-10">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      <p class="mt-4 text-gray-600">{{ t('videoList.loading') }}</p>
    </div>
    
    <div v-else-if="filteredVideos.length === 0" class="text-center py-10">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
      </svg>
      <h3 class="mt-2 text-lg font-medium text-gray-900">{{ t('videoList.noVideosFound') }}</h3>
      <p class="mt-1 text-gray-500">{{ t('videoList.noVideosDescription') }}</p>
    </div>
    
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <VideoCard 
        v-for="video in filteredVideos" 
        :key="video.id" 
        :video="video"
        :show-edit="true"
        :show-delete="true"
        :disabled="true"
        @preview="previewVideo"
        @edit="editVideo"
        @upload="uploadVideo"
        @delete="requestDeleteVideo"
        @download="downloadVideo"
        @share="shareVideo"
      />
    </div>
    
    <!-- 删除确认模态框 -->
    <Modal
      v-model:visible="showDeleteModal"
      :title="t('videoList.deleteConfirmTitle')"
      :confirm-text="t('videoList.delete')"
      :cancel-text="t('videoList.cancel')"
      :show-footer="true"
      size="md"
      confirm-button-class="bg-red-600 hover:bg-red-700 focus:ring-red-500"
      @confirm="confirmDeleteVideo"
      @cancel="showDeleteModal = false"
    >
      <p class="text-gray-700">{{ t('videoList.deleteConfirmText', { title: videoToDelete?.title }) }}</p>
      <p class="text-sm text-gray-500 mt-2">{{ t('videoList.deleteConfirmWarning') }}</p>
    </Modal>
    
    <LoginPlatformCard 
      v-if="showLoginDialog" 
      @select-platform="handlePlatformSelect"
      @close="showLoginDialog = false"
    />
    
    <PlatformLoginWindow
      v-if="showPlatformLoginWindow"
      :platform="selectedPlatform"
      @login-success="onPlatformLogin"
      @login-error="onPlatformLoginError"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import VideoCard from '@/components/VideoCard.vue'
import Modal from '@/components/Modal.vue'
import LoginPlatformCard from '@/components/LoginPlatformCard.vue'
import PlatformLoginWindow from '@/components/PlatformLoginWindow.vue'
import api from '@/services/api.js'

// 初始化国际化
const { t } = useI18n()

// 状态
const loading = ref(false)
const videos = ref([])
const searchQuery = ref('')
const statusFilter = ref('')
const showDeleteModal = ref(false)
const videoToDelete = ref(null)
const showLoginDialog = ref(false)
const showPlatformLoginWindow = ref(false)
const selectedVideo = ref(null)
const selectedPlatform = ref(null)
const router = useRouter()

// 获取视频
const fetchVideos = async () => {
  loading.value = true
  
  try {
    const response = await api.get('/videos');
    // 处理新的API返回格式 { success: true, data: [...] }
    const videosData = response.data.success ? response.data.data : response.data;
    
    // 转换后端数据格式以匹配前端组件的期望
    videos.value = videosData.map(video => ({
      id: video.id,
      title: video.title,
      description: video.description,
      thumbnail: video.thumbnail_path || 'https://picsum.photos/seed/default/400/225',
      videoUrl: video.file_path, // 添加视频链接
      // 后端没有返回duration字段，暂时设置为0
      duration: 0,
      // 后端返回的是created_at而不是createdAt，且是ISO格式
      createdAt: video.created_at,
      // 后端没有返回status字段，暂时设置为published
      status: 'published'
    }));
  } catch (error) {
    console.error('获取视频失败:', error);
    // 出错时使用空数组
    videos.value = [];
  } finally {
    loading.value = false;
  }
}

// 过滤后的视频
const filteredVideos = computed(() => {
  return videos.value.filter(video => {
    const matchesSearch = video.title.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                         video.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesStatus = statusFilter.value ? video.status === statusFilter.value : true
    return matchesSearch && matchesStatus
  })
})

// 预览视频
const previewVideo = (video) => {
  router.push(`/video/${video.id}`)
}

// 编辑视频
const editVideo = (video) => {
  router.push(`/edit-video/${video.id}`)
}

const uploadVideo = async (video) => {
  // Show platform selection dialog
  showLoginDialog.value = true
  selectedVideo.value = video
}

const handlePlatformSelect = async (platform) => {
  showLoginDialog.value = false
  selectedPlatform.value = platform
  showPlatformLoginWindow.value = true
}

const onPlatformLogin = async () => {
  showPlatformLoginWindow.value = false
  
  // Start the upload process
  if (selectedVideo.value && selectedPlatform.value) {
    try {
      const response = await api.post('/publish-video', {
        article_url: selectedVideo.value.article_url,
        platforms: [selectedPlatform.value],
        content_mode: 'regenerate'  // Using regenerate as default, can be changed if needed
      })
      
      if (response.data.success) {
        console.log('视频上传成功')
        // Update video status
        const videoIndex = videos.value.findIndex(v => v.id === selectedVideo.value.id)
        if (videoIndex !== -1) {
          videos.value[videoIndex].status = 'published'
        }
      } else {
        console.error('视频上传失败:', response.data.error)
      }
    } catch (error) {
      console.error('视频上传失败:', error)
    }
  }
}

const onPlatformLoginError = (error) => {
  showPlatformLoginWindow.value = false
  console.error('平台登录失败:', error)
}

// 请求删除视频
const requestDeleteVideo = (video) => {
  videoToDelete.value = video
  showDeleteModal.value = true
}

// 确认删除视频
const confirmDeleteVideo = async () => {
  if (videoToDelete.value) {
    try {
      await api.delete(`/video/${videoToDelete.value.id}`)
      // 删除成功后更新本地列表
      videos.value = videos.value.filter(v => v.id !== videoToDelete.value.id)
      console.log('删除视频:', videoToDelete.value)
    } catch (error) {
      console.error('删除视频失败:', error)
      alert('删除视频失败，请重试')
    } finally {
      videoToDelete.value = null
    }
  }
  showDeleteModal.value = false
}

// 下载视频
const downloadVideo = (video) => {
  console.log('下载视频:', video)
  // 这里可以实现下载逻辑
}

// 分享视频
const shareVideo = (video) => {
  console.log('分享视频:', video)
  // 这里可以实现分享逻辑
}

// 组件挂载时获取视频
onMounted(() => {
  fetchVideos()
})
</script>