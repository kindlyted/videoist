import { defineStore } from 'pinia'
import api from '@/services/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    isAuthenticated: false
  }),
  
  actions: {
    async login(credentials) {
      try {
        const response = await api.post('/login', credentials)
        const { user, access_token } = response.data
        
        this.user = user
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
        this.isAuthenticated = false
        
        // 清除localStorage中的token
        localStorage.removeItem('access_token')
      }
    },
    
    async fetchUser() {
      try {
        const response = await api.get('/user-info')
        this.user = response.data
        this.isAuthenticated = true
        
        return { success: true }
      } catch (error) {
        this.user = null
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