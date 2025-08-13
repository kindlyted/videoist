<template>
  <div class="container mx-auto px-4 py-8">
    <!-- 欢迎标题 -->
    <div class="mb-8 flex items-center">
      <h1 class="text-3xl font-bold">{{ user?.username }}，欢迎回来！</h1>
      <HandRaisedIcon class="h-8 w-8 text-blue-500 ml-4" />
    </div>
    
    <!-- 账户信息区域 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      <!-- 账户信息卡片 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4">账户信息</h2>
        <div class="space-y-2">
          <p><span class="font-medium">用户名:</span> {{ user?.username }}</p>
          <p><span class="font-medium">邮箱:</span> {{ user?.email }}</p>
        </div>
        <button 
          class="mt-4 bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded flex items-center"
        >
          <InformationCircleIcon class="h-5 w-5 mr-2" />
          查看详情
        </button>
      </div>
      
      <!-- 平台统计卡片 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold mb-4">平台统计</h2>
        <div class="space-y-2">
          <p><span class="font-medium">WordPress站点数量:</span> {{ wordpressSites.length }}</p>
          <p><span class="font-medium">微信公众号数量:</span> {{ wechatAccounts.length }}</p>
        </div>
        <div class="mt-4 flex space-x-2">
          <button 
            class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded flex items-center flex-1 justify-center"
            @click="navigateTo('/wordpress')"
          >
            <GlobeAltIcon class="h-5 w-5 mr-2" />
            WordPress管理
          </button>
          <button 
            class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded flex items-center flex-1 justify-center"
            @click="navigateTo('/wechat')"
          >
            <ChatBubbleLeftRightIcon class="h-5 w-5 mr-2" />
            微信公众号管理
          </button>
        </div>
      </div>
    </div>
    
    <!-- 最近活动区域 -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4">最近活动</h2>
      <ul class="space-y-2">
        <li 
          v-for="activity in recentActivities" 
          :key="activity.id" 
          class="border-b border-gray-200 pb-2"
        >
          {{ activity.description }}
        </li>
        <li v-if="recentActivities.length === 0" class="text-gray-500">
          暂无活动
        </li>
      </ul>
    </div>
    
    <!-- 导航菜单 -->
    <div class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-semibold mb-4">导航菜单</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <button 
          v-for="item in menuItems" 
          :key="item.name"
          @click="navigateTo(item.path)"
          :class="[
            'py-2 px-4 rounded flex items-center',
            item.type === 'primary' 
              ? 'bg-blue-500 hover:bg-blue-700 text-white' 
              : 'bg-transparent hover:bg-blue-500 text-blue-700 hover:text-white border border-blue-500'
          ]"
        >
          <component :is="getIconForMenuItem(item.name)" class="h-5 w-5 mr-2" />
          {{ item.name }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { HandRaisedIcon, InformationCircleIcon, GlobeAltIcon, ChatBubbleLeftRightIcon, UserIcon, CogIcon, InformationCircleIcon as InfoIcon, QuestionMarkCircleIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const userStore = useUserStore()

// 用户数据
const user = computed(() => userStore.user)

// 模拟数据
const wordpressSites = ref([
  { id: 1, name: '我的博客' },
  { id: 2, name: '公司网站' }
])

const wechatAccounts = ref([
  { id: 1, name: '个人公众号' }
])

const recentActivities = ref([
  { id: 1, description: '系统登录' },
  { id: 2, description: '视频生成成功' }
])

// 菜单项
const menuItems = ref([
  { name: '账户信息', path: '/account', type: 'primary' },
  { name: '设置', path: '/settings', type: 'secondary' },
  { name: 'WordPress', path: '/wordpress', type: 'secondary' },
  { name: '微信公众号', path: '/wechat', type: 'secondary' },
  { name: '关于我们', path: '/about', type: 'secondary' },
  { name: '退出登录', path: '/logout', type: 'secondary' }
])

// 导航方法
const navigateTo = (path) => {
  if (path === '/logout') {
    handleLogout()
  } else {
    router.push(path)
  }
}

// 为菜单项获取相应图标
const getIconForMenuItem = (itemName) => {
  const iconMap = {
    '账户信息': UserIcon,
    '设置': CogIcon,
    'WordPress': GlobeAltIcon,
    '微信公众号': ChatBubbleLeftRightIcon,
    '关于我们': InfoIcon,
    '退出登录': QuestionMarkCircleIcon
  }
  return iconMap[itemName] || InfoIcon
}

// 退出登录方法
const handleLogout = async () => {
  await userStore.logout()
  router.push('/login')
}
</script>