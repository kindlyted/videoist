import { defineStore } from 'pinia'
import api from '@/services/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: null,
    isAuthenticated: false
  }),
  
  getters: {
    // 从localStorage获取token的getter
    getToken: (state) => {
      if (!state.token) {
        state.token = localStorage.getItem('access_token')
      }
      return state.token
    }
  },
  
  actions: {
    async login(credentials) {
      try {
        const response = await api.post('/login', credentials)
        const { user, access_token } = response.data
        
        this.user = user
        this.token = access_token
        this.isAuthenticated = true
        
        // 保存token到localStorage
        localStorage.setItem('access_token', access_token)
        
        return { success: true }
      } catch (error) {
        return { success: false, error: error.response?.data?.message || '登录失败' }
      }
    },
    
    async register(userData) {
      try {
        const response = await api.post('/auth/register', userData)
        const { user, access_token } = response.data
        
        this.user = user
        this.token = access_token
        this.isAuthenticated = true
        
        // 保存token到localStorage
        localStorage.setItem('access_token', access_token)
        
        return { success: true }
      } catch (error) {
        return { success: false, error: error.response?.data?.message || '注册失败' }
      }
    },
    
    async logout() {
      try {
        await api.post('/logout')
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.user = null
        this.token = null
        this.isAuthenticated = false
        
        // 清除localStorage中的token
        localStorage.removeItem('access_token')
      }
    },
    
    async fetchUser() {
      try {
        const response = await api.get('/user-info')
        this.user = response.data.user  // 注意：后端返回的数据结构是 { user: {...} }
        this.isAuthenticated = true
        
        return { success: true }
      } catch (error) {
        this.user = null
        this.token = null
        this.isAuthenticated = false
        
        // 清除localStorage中的token
        localStorage.removeItem('access_token')
        
        return { success: false, error: error.response?.data?.message || '获取用户信息失败' }
      }
    },
    
    async resetPassword(email) {
      try {
        const response = await api.post('/auth/reset-password', { email })
        return { success: true, message: response.data.message }
      } catch (error) {
        return { success: false, error: error.response?.data?.error || '重置密码请求失败' }
      }
    }
  }
})