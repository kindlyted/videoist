import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import DashboardView from '@/views/DashboardView.vue'
import VideoCreationView from '@/views/VideoCreationView.vue'
import WordPressManagementView from '@/views/WordPressManagementView.vue'
import WeChatManagementView from '@/views/WeChatManagementView.vue'
import VideoListView from '@/views/VideoListView.vue'
import VideoPreviewView from '@/views/VideoPreviewView.vue'
import SettingsView from '@/views/SettingsView.vue'
import ResetPasswordView from '@/views/ResetPasswordView.vue'
import NotesView from '@/views/NotesView.vue'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/video-creation',
      name: 'video-creation',
      component: VideoCreationView
    },
    {
      path: '/wordpress',
      name: 'wordpress',
      component: WordPressManagementView
    },
    {
      path: '/wechat',
      name: 'wechat',
      component: WeChatManagementView
    },
    {
      path: '/videos',
      name: 'videos',
      component: VideoListView
    },
    {
      path: '/video/:id',
      name: 'video-preview',
      component: VideoPreviewView,
      props: true
    },
    {
      path: '/settings',
      name: 'settings',
      component: SettingsView
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      component: ResetPasswordView
    },
    {
      path: '/notes',
      name: 'notes',
      component: NotesView
    }
  ]
})

// 添加导航守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  // 需要登录的路由
  const protectedRoutes = ['/video-creation', '/notes', '/dashboard', '/settings', '/wordpress', '/wechat', '/videos', '/video/:id']
  
  // 如果用户未认证但有token，尝试恢复用户状态
  if (!userStore.isAuthenticated) {
    const token = localStorage.getItem('access_token')
    if (token) {
      await userStore.fetchUser()
    }
  }
  
  // 检查目标路由是否需要登录
  if (protectedRoutes.includes(to.path) && !userStore.isAuthenticated) {
    // 重定向到登录页
    next('/login')
  } else {
    // 允许访问
    next()
  }
})

export default router