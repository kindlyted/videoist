<template>
  <div class="px-container py-container">
    <div class="mb-6 flex items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">WordPress 管理</h1>
        <p class="text-gray-600 mt-1">管理您的 WordPress 站点和文章</p>
      </div>
      <GlobeAltIcon class="h-8 w-8 text-blue-500 ml-4" />
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 站点列表 -->
      <div class="lg:col-span-2">
        <div class="card">
          <div class="card-header flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
            <h2 class="card-title">WordPress 站点</h2>
            <button 
              @click="showAddSiteModal = true"
              class="btn btn-primary flex items-center"
            >
              <PlusIcon class="h-5 w-5 mr-2" />
              添加站点
            </button>
          </div>
          <div class="card-body">
            <div v-if="sites.length > 0" class="space-y-4">
              <div 
                v-for="site in sites" 
                :key="site.id" 
                class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition"
              >
                <div class="flex justify-between items-start">
                  <div>
                    <h3 class="font-medium text-gray-900">{{ site.name }}</h3>
                    <p class="text-sm text-gray-500 mt-1">{{ site.url }}</p>
                  </div>
                  <div class="flex space-x-2">
                    <button 
                      @click="editSite(site)"
                      class="text-blue-600 hover:text-blue-900 flex items-center"
                    >
                      <PencilIcon class="h-4 w-4 mr-1" />
                      编辑
                    </button>
                    <button 
                      @click="requestDeleteSite(site)"
                      class="text-red-600 hover:text-red-900 flex items-center"
                    >
                      <TrashIcon class="h-4 w-4 mr-1" />
                      删除
                    </button>
                  </div>
                </div>
                <div class="mt-3 flex items-center text-sm text-gray-500">
                  <span>{{ site.postsCount }} 篇文章</span>
                  <span class="mx-2">•</span>
                  <span>上次同步: {{ formatDate(site.lastSync) }}</span>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              暂无 WordPress 站点
            </div>
          </div>
        </div>
      </div>
      
      <!-- 文章列表 -->
      <div>
        <div class="card">
          <div class="card-header flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
            <h2 class="card-title">文章</h2>
            <select 
              v-model="selectedSite" 
              class="form-select w-full sm:w-auto"
              :disabled="sites.length === 0"
            >
              <option value="">选择站点</option>
              <option 
                v-for="site in sites" 
                :key="site.id" 
                :value="site.id"
              >
                {{ site.name }}
              </option>
            </select>
          </div>
          <div class="card-body">
            <div v-if="selectedSite && filteredPosts.length > 0" class="space-y-4">
              <div 
                v-for="post in filteredPosts" 
                :key="post.id" 
                class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition cursor-pointer"
                @click="viewPost(post)"
              >
                <h3 class="font-medium text-gray-900">{{ post.title }}</h3>
                <p class="text-sm text-gray-500 mt-1">{{ formatDate(post.date) }}</p>
                <p class="text-sm text-gray-600 mt-2 line-clamp-2">{{ post.excerpt }}</p>
              </div>
            </div>
            <div v-else-if="selectedSite" class="text-center py-8 text-gray-500">
              该站点暂无文章
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              请先选择一个站点
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 添加/编辑站点模态框 -->
    <Modal
      v-model:visible="showAddSiteModal"
      :title="showEditSiteModal ? '编辑站点' : '添加站点'"
      :confirm-text="'保存'"
      :cancel-text="'取消'"
      :show-footer="true"
      size="md"
      @confirm="saveSite"
      @cancel="closeModal"
    >
      <form @submit.prevent="saveSite">
        <div class="mb-4">
          <label class="form-label">站点名称</label>
          <input 
            v-model="siteForm.name" 
            type="text" 
            class="form-input w-full" 
            required
          >
        </div>
        <div class="mb-4">
          <label class="form-label">站点URL</label>
          <input 
            v-model="siteForm.url" 
            type="url" 
            class="form-input w-full" 
            required
          >
        </div>
        <div class="mb-4">
          <label class="form-label">API 密钥</label>
          <input 
            v-model="siteForm.apiKey" 
            type="password" 
            class="form-input w-full" 
            required
          >
        </div>
      </form>
    </Modal>
    
    <!-- 删除确认模态框 -->
    <Modal
      v-model:visible="showDeleteModal"
      title="确认删除"
      :confirm-text="'删除'"
      :cancel-text="'取消'"
      :show-footer="true"
      size="md"
      confirm-button-class="bg-red-600 hover:bg-red-700 focus:ring-red-500"
      @confirm="confirmDeleteSite"
      @cancel="showDeleteModal = false"
    >
      <p class="text-gray-700">您确定要删除站点 "{{ siteToDelete?.name }}" 吗？</p>
      <p class="text-sm text-gray-500 mt-2">此操作无法撤销，关联的文章也将被删除。</p>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Modal from '@/components/Modal.vue'
import api from '@/services/api'
import { GlobeAltIcon, PlusIcon, PencilIcon, TrashIcon } from '@heroicons/vue/24/outline'

// 状态
const sites = ref([])
const posts = ref([])
const selectedSite = ref('')
const showAddSiteModal = ref(false)
const showEditSiteModal = ref(false)
const showDeleteModal = ref(false)
const siteToDelete = ref(null)
const loading = ref(false)

const siteForm = ref({
  id: null,
  name: '',
  url: '',
  apiKey: ''
})

// 计算属性
const filteredPosts = computed(() => {
  if (!selectedSite.value) return []
  return posts.value.filter(post => post.siteId === parseInt(selectedSite.value))
})

// 方法
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

// 获取 WordPress 站点列表
const fetchSites = async () => {
  try {
    loading.value = true
    const response = await api.get('/wordpress')
    sites.value = response.data.map(site => ({
      id: site.id,
      name: site.site_name,
      url: site.site_url,
      username: site.username,
      postsCount: 0, // 需要从后端获取或通过其他方式计算
      lastSync: new Date().toISOString() // 需要从后端获取
    }))
  } catch (error) {
    console.error('获取站点列表失败:', error)
    // 使用模拟数据作为后备
    sites.value = [
      {
        id: 1,
        name: '我的博客',
        url: 'https://myblog.com',
        username: 'admin',
        postsCount: 24,
        lastSync: '2023-05-15T14:30:00Z'
      },
      {
        id: 2,
        name: '公司网站',
        url: 'https://company.com',
        username: 'admin',
        postsCount: 15,
        lastSync: '2023-05-14T09:15:00Z'
      }
    ]
  } finally {
    loading.value = false
  }
}

// 添加 WordPress 站点
const addSite = async () => {
  try {
    const response = await api.post('/wordpress', {
      site_name: siteForm.value.name,
      site_url: siteForm.value.url,
      username: siteForm.value.username,
      api_key: siteForm.value.apiKey
    })
    
    // 添加成功后重新获取站点列表
    await fetchSites()
    closeModal()
  } catch (error) {
    console.error('添加站点失败:', error)
    alert('添加站点失败: ' + (error.response?.data?.error || '未知错误'))
  }
}

// 更新 WordPress 站点
const updateSite = async () => {
  try {
    await api.put(`/wordpress/${siteForm.value.id}`, {
      site_name: siteForm.value.name,
      site_url: siteForm.value.url,
      username: siteForm.value.username,
      api_key: siteForm.value.apiKey
    })
    
    // 更新成功后重新获取站点列表
    await fetchSites()
    closeModal()
  } catch (error) {
    console.error('更新站点失败:', error)
    alert('更新站点失败: ' + (error.response?.data?.error || '未知错误'))
  }
}

// 删除 WordPress 站点
const deleteSite = async () => {
  try {
    await api.delete(`/wordpress/${siteToDelete.value.id}`)
    
    // 删除成功后重新获取站点列表
    await fetchSites()
    showDeleteModal.value = false
    siteToDelete.value = null
  } catch (error) {
    console.error('删除站点失败:', error)
    alert('删除站点失败: ' + (error.response?.data?.error || '未知错误'))
  }
}

const editSite = (site) => {
  showAddSiteModal.value = true
  showEditSiteModal.value = true
  siteForm.value = { 
    id: site.id, 
    name: site.name, 
    url: site.url, 
    username: site.username, 
    apiKey: '' 
  }
}

const saveSite = async () => {
  if (siteForm.value.id) {
    // 更新站点
    await updateSite()
  } else {
    // 添加站点
    await addSite()
  }
}

const requestDeleteSite = (site) => {
  siteToDelete.value = site
  showDeleteModal.value = true
}

const confirmDeleteSite = async () => {
  if (siteToDelete.value) {
    await deleteSite()
  }
}

const closeModal = () => {
  showAddSiteModal.value = false
  showEditSiteModal.value = false
}

const viewPost = (post) => {
  alert(`查看文章: ${post.title}`)
  // 这里可以导航到文章详情页面
}

// 组件挂载时获取站点列表
onMounted(() => {
  fetchSites()
})
</script>