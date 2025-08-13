<template>
  <div class="px-container py-container">
    <div class="max-w-4xl mx-auto">
      <div class="mb-6">
        <button 
          @click="goBack" 
          class="btn btn-secondary flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
          </svg>
          返回视频列表
        </button>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2">
          <div class="card">
            <div class="card-body">
              <div class="mb-6">
                <div class="relative pb-[56.25%] h-0 rounded-lg overflow-hidden bg-gray-100">
                  <img 
                    :src="video.thumbnail" 
                    :alt="video.title" 
                    class="absolute inset-0 w-full h-full object-cover"
                  >
                  <div class="absolute inset-0 flex items-center justify-center">
                    <button 
                      class="bg-black bg-opacity-50 rounded-full p-4 hover:bg-opacity-75 transition"
                      @click="playVideo"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-white" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
              
              <div>
                <h1 class="text-2xl font-bold text-gray-900 mb-2">{{ video.title }}</h1>
                <p class="text-gray-600 mb-4">{{ video.description }}</p>
                
                <div class="flex flex-wrap gap-2 mb-6">
                  <span class="badge badge-primary">{{ video.category }}</span>
                  <span class="badge" :class="getStatusClass(video.status)">
                    {{ getStatusText(video.status) }}
                  </span>
                </div>
                
                <div class="mb-6">
                  <h3 class="font-medium text-gray-900 mb-2">视频描述</h3>
                  <p class="text-gray-600">{{ video.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="lg:col-span-1">
          <div class="card mb-6">
            <div class="card-header">
              <h2 class="card-title">视频信息</h2>
            </div>
            <div class="card-body">
              <ul class="space-y-3 text-sm">
                <li class="flex justify-between">
                  <span class="text-gray-500">创建时间:</span>
                  <span>{{ formatDate(video.createdAt) }}</span>
                </li>
                <li class="flex justify-between">
                  <span class="text-gray-500">时长:</span>
                  <span>{{ formatDuration(video.duration) }}</span>
                </li>
                <li class="flex justify-between">
                  <span class="text-gray-500">分辨率:</span>
                  <span>{{ video.resolution }}</span>
                </li>
                <li class="flex justify-between">
                  <span class="text-gray-500">大小:</span>
                  <span>{{ formatFileSize(video.fileSize) }}</span>
                </li>
              </ul>
            </div>
          </div>
          
          <div class="card">
            <div class="card-header">
              <h2 class="card-title">操作</h2>
            </div>
            <div class="card-body">
              <div class="space-y-3">
                <button 
                  @click="downloadVideo"
                  class="btn btn-primary w-full flex items-center justify-center"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                  下载
                </button>
                <button 
                  @click="shareVideo"
                  class="btn btn-secondary w-full flex items-center justify-center"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />
                  </svg>
                  分享
                </button>
                <button 
                  @click="regenerateVideo"
                  class="btn btn-warning w-full flex items-center justify-center"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
                  </svg>
                  重新生成
                </button>
                <button 
                  @click="requestDelete"
                  class="btn btn-danger w-full flex items-center justify-center"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                  删除
                </button>
              </div>
              
              <!-- 删除确认模态框 -->
              <Modal
                v-model:visible="showDeleteModal"
                title="确认删除"
                :confirm-text="'删除'"
                :cancel-text="'取消'"
                :show-footer="true"
                size="md"
                confirm-button-class="bg-red-600 hover:bg-red-700 focus:ring-red-500"
                @confirm="deleteVideo"
                @cancel="showDeleteModal = false"
              >
                <p class="text-gray-700">您确定要删除视频 "{{ video.title }}" 吗？</p>
                <p class="text-sm text-gray-500 mt-2">此操作无法撤销。</p>
              </Modal>
            </div>
          </div>
        </div>
      </div>
      
      <div class="mt-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">相关视频</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <VideoCard 
            v-for="relatedVideo in relatedVideos" 
            :key="relatedVideo.id" 
            :video="relatedVideo"
            @preview="previewRelatedVideo"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import VideoCard from '@/components/VideoCard.vue'
import Modal from '@/components/Modal.vue'

// 路由
const route = useRoute()
const router = useRouter()

// 状态
const loading = ref(false)
const video = ref(null)
const relatedVideos = ref([])
const showDeleteModal = ref(false)

// 模拟视频数据
const mockVideo = {
  id: 1,
  title: '产品介绍视频',
  description: '这是一个展示我们最新产品的视频，包含了产品的核心功能和优势。',
  thumbnail: 'https://picsum.photos/seed/p1/400/225',
  duration: 120,
  status: 'published',
  createdAt: '2023-05-15',
  content: '视频内容摘要...'
}

// 模拟相关视频数据
const mockRelatedVideos = [
  {
    id: 2,
    title: '教程视频',
    description: '如何使用我们的软件功能',
    thumbnail: 'https://picsum.photos/seed/p2/400/225',
    duration: 300,
    status: 'processing',
    createdAt: '2023-05-16'
  },
  {
    id: 3,
    title: '客户见证',
    description: '听听我们的客户怎么说',
    thumbnail: 'https://picsum.photos/seed/p3/400/225',
    duration: 180,
    status: 'draft',
    createdAt: '2023-05-17'
  },
  {
    id: 4,
    title: '活动回顾',
    description: '公司年度活动精彩瞬间',
    thumbnail: 'https://picsum.photos/seed/p4/400/225',
    duration: 240,
    status: 'published',
    createdAt: '2023-05-18'
  }
]

// 获取视频详情
const fetchVideo = () => {
  loading.value = true
  
  // 模拟API调用
  setTimeout(() => {
    video.value = mockVideo
    relatedVideos.value = mockRelatedVideos
    loading.value = false
  }, 1000)
}

// 请求删除
const requestDelete = () => {
  showDeleteModal.value = true
}

// 删除视频
const deleteVideo = () => {
  showDeleteModal.value = false
  console.log('删除视频:', video.value)
  // 这里可以实现删除逻辑
  router.push('/videos')
}

// 发布视频
const publishVideo = () => {
  if (video.value.status !== 'published') {
    video.value.status = 'published'
    console.log('发布视频:', video.value)
    // 这里可以实现发布逻辑
  }
}

// 组件挂载时获取视频
onMounted(() => {
  fetchVideo()
})
</script>