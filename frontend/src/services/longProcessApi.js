import axios from 'axios'

// 创建用于长时间处理的axios实例，不设置超时时间
const longProcessApi = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// 添加请求拦截器
longProcessApi.interceptors.request.use(
  config => {
    // 添加JWT token到请求头
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

export default longProcessApi