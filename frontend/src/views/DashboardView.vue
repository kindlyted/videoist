<template>
  <div class="container mx-auto px-4 py-8">
    <!-- 欢迎标题 -->
    <div class="mb-8 flex items-center">
      <h1 class="text-3xl font-bold">{{ $t('dashboard.welcome', { username: user?.username }) }}</h1>
      <HandRaisedIcon class="h-8 w-8 text-blue-500 ml-4" />
    </div>
    
    <!-- 第一行卡片区域 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <!-- 账户信息卡片 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4">{{ $t('dashboard.accountInfo') }}</h2>
        <div class="space-y-2">
          <p><span class="font-medium">{{ $t('dashboard.username') }}:</span> {{ user?.username }}</p>
          <p><span class="font-medium">{{ $t('dashboard.email') }}:</span> {{ user?.email }}</p>
        </div>
        <button 
          class="mt-4 bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded flex items-center"
          @click="router.push('/settings')"
        >
          <InformationCircleIcon class="h-5 w-5 mr-2" />
          {{ $t('dashboard.viewDetails') }}
        </button>
      </div>
      
      <!-- 文章平台卡片 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4">{{ $t('dashboard.articlePlatforms') }}</h2>
        <div class="space-y-2">
          <p><span class="font-medium">{{ $t('dashboard.wordpressSitesCount') }}:</span> {{ platformStats.wordpressSitesCount }}</p>
          <p><span class="font-medium">{{ $t('dashboard.wechatAccountsCount') }}:</span> {{ platformStats.wechatAccountsCount }}</p>
        </div>
        <div class="mt-4 flex space-x-2">
          <button 
            class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded flex items-center flex-1 justify-center"
            @click="navigateTo('/wordpress')"
          >
            <GlobeAltIcon class="h-5 w-5 mr-2" />
            {{ $t('dashboard.wordpressManagement') }}
          </button>
          <button 
            class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded flex items-center flex-1 justify-center"
            @click="navigateTo('/wechat')"
          >
            <ChatBubbleLeftRightIcon class="h-5 w-5 mr-2" />
            {{ $t('dashboard.wechatManagement') }}
          </button>
        </div>
      </div>
      
      <!-- 视频平台卡片 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4">{{ $t('dashboard.videoPlatforms') }}</h2>
        <div class="space-y-2">
          <p><span class="font-medium">{{ $t('dashboard.douyin') }}:</span> {{ $t('dashboard.connected') }}</p>
          <p><span class="font-medium">{{ $t('dashboard.xiaohongshu') }}:</span> {{ $t('dashboard.notConnected') }}</p>
        </div>
        <button 
          class="mt-4 bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded flex items-center"
        >
          <InformationCircleIcon class="h-5 w-5 mr-2" />
          {{ $t('dashboard.managePlatforms') }}
        </button>
      </div>
    </div>
    
    <!-- 第二行卡片区域 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <!-- 视频统计卡片 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4">{{ $t('dashboard.videoStats') }}</h2>
        <div class="space-y-2">
          <p><span class="font-medium">{{ $t('dashboard.totalVideos') }}:</span> {{ videoStats.videoCount }}</p>
        </div>
        <button 
          class="mt-4 bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded flex items-center"
          @click="navigateTo('/video-list')"
        >
          <InformationCircleIcon class="h-5 w-5 mr-2" />
          {{ $t('dashboard.videoManagement') }}
        </button>
      </div>
      
      <!-- 笔记统计卡片 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4">{{ $t('dashboard.noteStats') }}</h2>
        <div class="space-y-2">
          <p><span class="font-medium">{{ $t('dashboard.totalNotes') }}:</span> {{ noteStats.noteCount }}</p>
        </div>
        <button 
          class="mt-4 bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded flex items-center"
          @click="navigateTo('/note-list')"
        >
          <InformationCircleIcon class="h-5 w-5 mr-2" />
          {{ $t('dashboard.noteManagement') }}
        </button>
      </div>
      
      <!-- 最近活动卡片 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4">{{ $t('dashboard.recentActivities') }}</h2>
        <ul class="space-y-2">
          <li 
            v-for="activity in recentActivities" 
            :key="activity.id" 
            class="border-b border-gray-200 pb-2"
          >
            {{ activity.description }}
          </li>
          <li v-if="recentActivities.length === 0" class="text-gray-500">
            {{ $t('dashboard.noActivities') }}
          </li>
        </ul>
      </div>
    </div>
    

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useI18n } from 'vue-i18n'
import api from '@/services/api'
import { HandRaisedIcon, InformationCircleIcon, GlobeAltIcon, ChatBubbleLeftRightIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const userStore = useUserStore()
const { t } = useI18n()

// 用户数据
const user = computed(() => userStore.user)

// 平台统计数据
const platformStats = ref({
  wordpressSitesCount: 0,
  wechatAccountsCount: 0
})

// 视频统计数据
const videoStats = ref({
  videoCount: 0
})

// 笔记统计数据
const noteStats = ref({
  noteCount: 0
})

const recentActivities = ref([
  { id: 1, description: t('dashboard.activities.login') },
  { id: 2, description: t('dashboard.activities.videoGenerated') }
])

// 获取平台统计数据
const fetchPlatformStats = async () => {
  try {
    const response = await api.get('/platform-stats')
    platformStats.value = {
      wordpressSitesCount: response.data.wordpress_sites_count,
      wechatAccountsCount: response.data.wechat_accounts_count
    }
  } catch (error) {
    import('@/utils/errorHandler').then(module => {
      const errorMessage = module.handleApiError(error);
      console.error(errorMessage || '获取平台统计数据失败');
    });
  }
}

// 获取视频统计数据
const fetchVideoStats = async () => {
  try {
    const response = await api.get('/video-stats')
    videoStats.value = {
      videoCount: response.data.video_count
    }
  } catch (error) {
    import('@/utils/errorHandler').then(module => {
      const errorMessage = module.handleApiError(error);
      console.error(errorMessage || '获取视频统计数据失败');
    });
  }
}

// 获取笔记统计数据
const fetchNoteStats = async () => {
  try {
    const response = await api.get('/note-stats')
    noteStats.value = {
      noteCount: response.data.note_count
    }
  } catch (error) {
    import('@/utils/errorHandler').then(module => {
      const errorMessage = module.handleApiError(error);
      console.error(errorMessage || '获取笔记统计数据失败');
    });
  }
}

// 导航方法
const navigateTo = (path) => {
  router.push(path)
}

// 退出登录方法
const handleLogout = async () => {
  await userStore.logout()
  router.push('/login')
}

// 组件挂载时获取数据
onMounted(async () => {
  await fetchPlatformStats()
  await fetchVideoStats()
  await fetchNoteStats()
})
</script>