<template>
  <nav class="bg-white shadow-lg">
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex justify-between h-16">
        <!-- 左侧导航 -->
        <div class="flex items-center">
          <!-- Logo -->
          <div class="flex-shrink-0 flex items-center">
            <span class="text-xl font-bold text-blue-600">Videoist</span>
          </div>
          
          <!-- 桌面端导航菜单 -->
          <div class="hidden md:ml-6 md:flex md:space-x-8">
            <router-link 
              v-for="item in navigationItems" 
              :key="item.name"
              :to="item.path"
              :class="[
                'inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium',
                isCurrentRoute(item.path)
                  ? 'border-blue-500 text-gray-900'
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
              ]"
            >
              {{ item.name }}
            </router-link>
          </div>
        </div>
        
        <!-- 右侧用户菜单 -->
        <div class="flex items-center">
          <!-- 搜索框 -->
          <div class="flex-1 flex items-center justify-center px-2 lg:ml-6 lg:justify-end">
            <div class="max-w-lg w-full lg:max-w-xs">
              <label for="search" class="sr-only">搜索</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                  </svg>
                </div>
                <input 
                  id="search" 
                  name="search" 
                  class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-blue-500 focus:border-blue-500 sm:text-sm" 
                  placeholder="搜索视频..." 
                  type="search"
                />
              </div>
            </div>
          </div>
          
          <!-- 通知按钮 -->
          <button class="ml-4 bg-white p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none">
            <span class="sr-only">查看通知</span>
            <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </button>
          
          <!-- 用户头像下拉菜单 -->
          <div class="ml-3 relative">
            <div>
              <button 
                @click="toggleUserMenu" 
                class="flex text-sm rounded-full focus:outline-none"
                id="user-menu-button"
                aria-expanded="false"
                aria-haspopup="true"
              >
                <span class="sr-only">打开用户菜单</span>
                <div class="bg-gray-200 border-2 border-dashed rounded-xl w-8 h-8" />
              </button>
            </div>
            
            <!-- 下拉菜单 -->
            <div 
              v-show="showUserMenu"
              class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none" 
              role="menu" 
              aria-orientation="vertical" 
              aria-labelledby="user-menu-button"
              tabindex="-1"
            >
              <template v-if="user">
                <router-link 
                  to="/dashboard" 
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" 
                  role="menuitem" 
                  tabindex="-1"
                >
                  仪表板
                </router-link>
                <router-link 
                  to="/settings" 
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" 
                  role="menuitem" 
                  tabindex="-1"
                >
                  设置
                </router-link>
                <button 
                  @click="handleLogout"
                  class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" 
                  role="menuitem" 
                  tabindex="-1"
                >
                  退出登录
                </button>
              </template>
              <template v-else>
                <router-link 
                  to="/login" 
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" 
                  role="menuitem" 
                  tabindex="-1"
                >
                  登录
                </router-link>
                <router-link 
                  to="/register" 
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" 
                  role="menuitem" 
                  tabindex="-1"
                >
                  注册
                </router-link>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 移动端导航菜单按钮 -->
    <div class="md:hidden">
      <div class="flex items-center justify-between px-4 py-3">
        <button 
          @click="toggleMobileMenu" 
          class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none"
        >
          <span class="sr-only">打开主菜单</span>
          <svg 
            v-if="!showMobileMenu" 
            class="block h-6 w-6" 
            xmlns="http://www.w3.org/2000/svg" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor" 
            aria-hidden="true"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <svg 
            v-else 
            class="block h-6 w-6" 
            xmlns="http://www.w3.org/2000/svg" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor" 
            aria-hidden="true"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <!-- 移动端导航菜单 -->
      <div v-show="showMobileMenu" class="md:hidden">
        <div class="pt-2 pb-3 space-y-1">
          <router-link 
            v-for="item in navigationItems" 
            :key="item.name"
            :to="item.path"
            :class="[
              'block pl-3 pr-4 py-2 border-l-4 text-base font-medium',
              isCurrentRoute(item.path)
                ? 'bg-blue-50 border-blue-500 text-blue-700'
                : 'border-transparent text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800'
            ]"
          >
            {{ item.name }}
          </router-link>
        </div>
        
        <!-- 移动端用户菜单 -->
        <div class="pt-4 pb-3 border-t border-gray-200">
          <div class="flex items-center px-4">
            <div class="flex-shrink-0">
              <div class="bg-gray-200 border-2 border-dashed rounded-xl w-10 h-10" />
            </div>
            <div class="ml-3">
              <div class="text-base font-medium text-gray-800">{{ user?.username }}</div>
              <div class="text-sm font-medium text-gray-500">{{ user?.email }}</div>
            </div>
          </div>
          <div class="mt-3 space-y-1">
            <template v-if="user">
              <router-link 
                to="/dashboard" 
                class="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
              >
                仪表板
              </router-link>
              <router-link 
                to="/settings" 
                class="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
              >
                设置
              </router-link>
              <button 
                @click="handleLogout"
                class="block w-full text-left px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
              >
                退出登录
              </button>
            </template>
            <template v-else>
              <router-link 
                to="/login" 
                class="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
              >
                登录
              </router-link>
              <router-link 
                to="/register" 
                class="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
              >
                注册
              </router-link>
            </template>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 状态
const showUserMenu = ref(false)
const showMobileMenu = ref(false)

// 用户数据
const user = computed(() => userStore.user)

// 导航项
const navigationItems = [
  { name: '首页', path: '/' },
  { name: '视频创作', path: '/video-creation' },
  { name: '整理笔记', path: '/notes' }
]

// 方法
const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const handleLogout = async () => {
  await userStore.logout()
  router.push('/login')
}

const isCurrentRoute = (path) => {
  return route.path === path
}

// 点击外部关闭下拉菜单
document.addEventListener('click', (event) => {
  const userMenuButton = document.getElementById('user-menu-button')
  if (userMenuButton && !userMenuButton.contains(event.target)) {
    showUserMenu.value = false
  }
})
</script>