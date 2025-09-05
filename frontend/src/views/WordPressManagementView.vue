<template>
  <div class="px-container py-container">
    <div class="mb-6 flex items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">{{ $t('wordpressManagement.title') }}</h1>
        <p class="text-gray-600 mt-1">{{ $t('wordpressManagement.description') }}</p>
      </div>
      <GlobeAltIcon class="h-8 w-8 text-blue-500 ml-4" />
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 站点列表 -->
      <div class="lg:col-span-2">
        <div class="card">
          <div class="card-header flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
            <h2 class="card-title">{{ $t('wordpressManagement.sites') }}</h2>
            <button 
              @click="openAddSiteModal"
              class="btn btn-primary flex items-center"
            >
              <PlusIcon class="h-5 w-5 mr-2" />
              {{ $t('wordpressManagement.addSite') }}
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
                    <p class="text-sm text-gray-500 mt-1">用户名: {{ site.username }}</p>
                    <p class="text-sm text-gray-500 mt-1">WP Tag: {{ site.wpTag }}</p>
                    <div class="text-sm text-gray-500 mt-1">
                      <p class="font-medium">Footer:</p>
                      <div class="border border-gray-300 rounded p-2 mt-1 bg-white" v-html="site.wpFooter"></div>
                    </div>
                  </div>
                  <div class="flex space-x-2">
                    <button 
                      @click="editSite(site)"
                      class="text-blue-600 hover:text-blue-900 flex items-center"
                    >
                      <PencilIcon class="h-4 w-4 mr-1" />
                      {{ $t('wordpressManagement.edit') }}
                    </button>
                    <button 
                      @click="requestDeleteSite(site)"
                      class="text-red-600 hover:text-red-900 flex items-center"
                    >
                      <TrashIcon class="h-4 w-4 mr-1" />
                      {{ $t('wordpressManagement.delete') }}
                    </button>
                  </div>
                </div>
                <div class="mt-3 flex items-center text-sm text-gray-500">
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              {{ $t('wordpressManagement.noSites') }}
            </div>
          </div>
        </div>
      </div>
      
      <!-- 文章列表 -->
      <div>
        <div class="card">
          <div class="card-header flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
            <h2 class="card-title">{{ $t('wordpressManagement.posts') }}</h2>
            <select 
              v-model="selectedSite" 
              class="form-select w-full sm:w-auto"
              :disabled="sites.length === 0"
            >
              <option value="">{{ $t('wordpressManagement.selectSite') }}</option>
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
              {{ $t('wordpressManagement.noPosts') }}
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              {{ $t('wordpressManagement.noSiteSelected') }}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 添加/编辑站点模态框 -->
    <Modal
        v-model:visible="showAddSiteModal"
        :title="showEditSiteModal ? $t('wordpressManagement.editSite') : $t('wordpressManagement.addSite')"
        :confirm-text="$t('wordpressManagement.save')"
        :cancel-text="$t('wordpressManagement.cancel')"
        :show-footer="true"
        size="md"
        @confirm="handleSaveSite"
        @cancel="closeModal"
      >
      <form @submit.prevent="saveSite">
        <div class="mb-4">
          <label class="form-label">{{ $t('wordpressManagement.siteName') }}</label>
          <input 
            v-model="siteForm.name" 
            type="text" 
            class="form-input w-full" 
            :placeholder="$t('wordpressManagement.siteNamePlaceholder')"
            required
          >
        </div>
        <div class="mb-4">
          <label class="form-label">{{ $t('wordpressManagement.siteUrl') }}</label>
          <input 
            v-model="siteForm.url" 
            type="url" 
            class="form-input w-full" 
            :placeholder="$t('wordpressManagement.siteUrlPlaceholder')"
            required
          >
        </div>
        <div class="mb-4">
          <label class="form-label">{{ $t('wordpressManagement.username') }}</label>
          <input 
            v-model="siteForm.username" 
            type="text" 
            class="form-input w-full" 
            :placeholder="$t('wordpressManagement.usernamePlaceholder')"
            required
          >
        </div>
        <div class="mb-4">
            <label class="form-label">{{ $t('wordpressManagement.apiKey') }}</label>
            <input 
              v-model="siteForm.apiKey" 
              type="password" 
              class="form-input w-full" 
              :placeholder="$t('wordpressManagement.apiKeyPlaceholder')"
              required
            >
          </div>
          <div class="mb-4">
            <label class="form-label">{{ $t('wordpressManagement.wpTag') }}</label>
            <input 
              v-model="siteForm.wpTag" 
              type="text" 
              class="form-input w-full"
              :placeholder="$t('wordpressManagement.wpTagPlaceholder')"
              required
            >
          </div>
          <div class="mb-4">
            <label class="form-label">{{ $t('wordpressManagement.wpFooter') }}</label>
            <textarea 
              v-model="siteForm.wpFooter" 
              class="form-input w-full" 
              rows="3"
              :placeholder="$t('wordpressManagement.wpFooterPlaceholder')"
              required
            ></textarea>
          </div>
      </form>
    </Modal>
    
    <!-- 删除确认模态框 -->
    <Modal
      v-model:visible="showDeleteModal"
      :title="$t('wordpressManagement.confirmDeleteTitle')"
      :confirm-text="$t('wordpressManagement.delete')"
      :cancel-text="$t('wordpressManagement.cancel')"
      :show-footer="true"
      size="md"
      confirm-button-class="bg-red-600 hover:bg-red-700 focus:ring-red-500"
      @confirm="confirmDeleteSite"
      @cancel="showDeleteModal = false"
    >
      <p class="text-gray-700">{{ $t('wordpressManagement.deleteConfirm', { name: siteToDelete?.name }) }}</p>
      <p class="text-sm text-gray-500 mt-2">{{ $t('wordpressManagement.deleteWarning') }}</p>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '@/services/api'
import Modal from '@/components/Modal.vue'
import Switch from '@/components/Switch.vue'
import { GlobeAltIcon, PlusIcon, PencilIcon, TrashIcon } from '@heroicons/vue/24/outline'
import { handleApiError, getErrorMessageKey } from '@/utils/errorHandler'

const { t } = useI18n()

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
  username: '',
  apiKey: '',
  wpTag: '',
  wpFooter: ''
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
      wpTag: site.wp_tag || '',
      wpFooter: site.wp_footer || '',
      postsCount: 0, // 需要从后端获取或通过其他方式计算
      lastSync: new Date().toISOString() // 需要从后端获取
    }))
  } catch (error) {
    console.error('获取站点列表失败:', error)
    // 处理错误信息
    const errorResult = handleApiError(error);
    let errorMessage = '';
    
    if (errorResult.message) {
      errorMessage = errorResult.message;
    } else if (errorResult.messageKey) {
      errorMessage = t(errorResult.messageKey);
    } else if (errorResult.errorCode) {
      errorMessage = t(getErrorMessageKey(errorResult.errorCode));
    }
    
    alert(errorMessage || '获取站点列表失败');
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

// 获取 WordPress 文章列表
const fetchPosts = async () => {
  try {
    const response = await api.get('/wordpress/posts')
    posts.value = response.data
  } catch (error) {
    console.error('获取文章列表失败:', error)
    // 使用模拟数据作为后备
    posts.value = [
      {
        id: 1,
        siteId: 1,
        title: '我的第一篇博客文章',
        date: '2023-05-15T14:30:00Z',
        excerpt: '这是我的第一篇博客文章的摘要...'
      },
      {
        id: 2,
        siteId: 1,
        title: '如何使用WordPress',
        date: '2023-05-14T09:15:00Z',
        excerpt: '在这篇文章中，我将介绍如何使用WordPress创建网站...'
      }
    ]
  }
}

// 添加 WordPress 站点
const addSite = async () => {
  try {
    if (!validateForm()) return
    
    const newSite = {
      ...siteForm.value,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    
    const response = await api.post('/wordpress/sites', newSite)
    sites.value.push(response.data)
    closeModal()
    console.log(t('wordpressManagement.siteAdded'))
    
    // 重置表单
    Object.keys(siteForm.value).forEach(key => {
      siteForm.value[key] = ''
    })
  } catch (error) {
    // 处理错误信息
    const errorResult = handleApiError(error);
    let errorMessage = '';
    
    if (errorResult.message) {
      errorMessage = errorResult.message;
    } else if (errorResult.messageKey) {
      errorMessage = t(errorResult.messageKey);
    } else if (errorResult.errorCode) {
      errorMessage = t(getErrorMessageKey(errorResult.errorCode));
    }
    
    alert(errorMessage || t('wordpressManagement.addSiteFailed'));
  }
}

// 更新 WordPress 站点
const updateSite = async () => {
  if (!siteForm.value.id) return
  
  try {
    if (!validateForm()) return
    
    const updatedSite = {
      ...siteForm.value,
      updated_at: new Date().toISOString()
    }
    
    const response = await api.put(`/wordpress/sites/${siteForm.value.id}`, updatedSite)
    
    // 更新本地数据
    const index = sites.value.findIndex(site => site.id === siteForm.value.id)
    if (index !== -1) {
      sites.value[index] = { ...sites.value[index], ...response.data }
    }
    
    closeModal()
    console.log(t('wordpressManagement.siteUpdated'))
  } catch (error) {
    // 处理错误信息
    const errorResult = handleApiError(error);
    let errorMessage = '';
    
    if (errorResult.message) {
      errorMessage = errorResult.message;
    } else if (errorResult.messageKey) {
      errorMessage = t(errorResult.messageKey);
    } else if (errorResult.errorCode) {
      errorMessage = t(getErrorMessageKey(errorResult.errorCode));
    }
    
    alert(errorMessage || t('wordpressManagement.updateSiteFailed'));
  }
}

// 删除 WordPress 站点
const deleteSite = async (siteId) => {
  if (!confirm(t('wordpressManagement.confirmDelete'))) return
  
  try {
    await api.delete(`/wordpress/sites/${siteId}`)
    sites.value = sites.value.filter(site => site.id !== siteId)
    if (selectedSite.value === siteId) {
      selectedSite.value = ''
      posts.value = []
    }
    console.log(t('wordpressManagement.siteDeleted'))
  } catch (error) {
    // 处理错误信息
    const errorResult = handleApiError(error);
    let errorMessage = '';
    
    if (errorResult.message) {
      errorMessage = errorResult.message;
    } else if (errorResult.messageKey) {
      errorMessage = t(errorResult.messageKey);
    } else if (errorResult.errorCode) {
      errorMessage = t(getErrorMessageKey(errorResult.errorCode));
    }
    
    alert(errorMessage || t('wordpressManagement.deleteSiteFailed'));
  }
}

const editSite = (site) => {
  siteForm.value = { 
    id: site.id, 
    name: site.name, 
    url: site.url, 
    username: site.username, 
    apiKey: '',
    wpTag: site.wpTag || '',
    wpFooter: site.wpFooter || ''
  }
  showEditSiteModal.value = true
  showAddSiteModal.value = true
}

const validateForm = () => {
  if (!siteForm.value.name || !siteForm.value.url || !siteForm.value.username || 
      !siteForm.value.apiKey || !siteForm.value.wpTag || !siteForm.value.wpFooter) {
    alert(t('wordpressManagement.allFieldsRequired'));
    return false;
  }
  return true;
};

const validateWpTag = (wpTag) => {
  try {
    const tagData = JSON.parse(wpTag);
    if (!tagData.prefix || !tagData.categories || !tagData.tags) {
      return false;
    }
    return (
      Array.isArray(tagData.prefix) &&
      typeof tagData.categories === 'object' &&
      typeof tagData.tags === 'object'
    );
  } catch (e) {
    return false;
  }
};

const validateHttpsUrl = (url) => {
  return url.startsWith('https://');
};

const saveSite = async () => {
  if (!validateForm()) return false;
  
  if (!validateWpTag(siteForm.value.wpTag)) {
    alert(t('wordpressManagement.wpTagInvalid'));
    return false;
  }
  if (!validateHttpsUrl(siteForm.value.url)) {
    alert(t('wordpressManagement.urlMustBeHttps'));
    return false;
  }
  if (siteForm.value.id) {
    // 更新站点
    await updateSite()
  } else {
    // 添加站点
    await addSite()
  }
  return true;
}

const handleSaveSite = async () => {
  const success = await saveSite();
  if (success) {
    closeModal();
  }
}

const requestDeleteSite = (site) => {
  siteToDelete.value = site
  showDeleteModal.value = true
}

const confirmDeleteSite = async () => {
  if (siteToDelete.value) {
    await deleteSite(siteToDelete.value.id)
  }
}

const closeModal = () => {
  showAddSiteModal.value = false
  showEditSiteModal.value = false
  // 重置表单
  resetForm()
}

const resetForm = () => {
  siteForm.value = {
    id: null,
    name: '',
    url: '',
    username: '',
    apiKey: '',
    wpTag: '',
    wpFooter: ''
  }
}

const openAddSiteModal = () => {
  resetForm()
  showAddSiteModal.value = true
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

// 监听选中站点的变化，获取对应的文章列表
watch(selectedSite, (newVal) => {
  if (newVal) {
    fetchPosts()
  } else {
    posts.value = []
  }
})
</script>