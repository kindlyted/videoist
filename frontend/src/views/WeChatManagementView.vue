<template>
  <div class="px-container py-container">
    <div class="mb-6 flex items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">微信管理</h1>
        <p class="text-gray-600 mt-1">管理您的微信账号和发布内容</p>
      </div>
      <ChatBubbleLeftRightIcon class="h-8 w-8 text-green-500 ml-4" />
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 账号列表 -->
      <div class="lg:col-span-2">
        <div class="card">
          <div class="card-header flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
            <h2 class="card-title">微信账号</h2>
            <button 
              @click="showAddAccountModal = true"
              class="btn btn-primary flex items-center"
            >
              <PlusIcon class="h-5 w-5 mr-2" />
              添加账号
            </button>
          </div>
          <div class="card-body">
            <div v-if="accounts.length > 0" class="space-y-4">
              <div 
                v-for="account in accounts" 
                :key="account.id" 
                class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition"
              >
                <div class="flex justify-between items-start">
                  <div>
                    <h3 class="font-medium text-gray-900">{{ account.name }}</h3>
                    <p class="text-sm text-gray-500 mt-1">Account ID: {{ account.accountId }}</p>
                    <p class="text-sm text-gray-500 mt-1">App ID: {{ account.appId }}</p>
                    <div class="text-sm text-gray-500 mt-1">
                      <p class="font-medium">Footer:</p>
                      <div class="border border-gray-300 rounded p-2 mt-1 bg-white" v-html="account.wxFooter"></div>
                    </div>
                  </div>
                  <div class="flex space-x-2">
                    <button 
                      @click="editAccount(account)"
                      class="text-blue-600 hover:text-blue-900 flex items-center"
                    >
                      <PencilIcon class="h-4 w-4 mr-1" />
                      编辑
                    </button>
                    <button 
                      @click="requestDeleteAccount(account)"
                      class="text-red-600 hover:text-red-900 flex items-center"
                    >
                      <TrashIcon class="h-4 w-4 mr-1" />
                      删除
                    </button>
                  </div>
                </div>
                <!-- 移除了状态显示部分 -->
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              暂无微信账号
            </div>
          </div>
        </div>
      </div>
      
      <!-- 内容列表 -->
      <div>
        <div class="card">
          <div class="card-header flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
            <h2 class="card-title">内容</h2>
            <select 
              v-model="selectedAccount" 
              class="form-select w-full sm:w-auto"
              :disabled="accounts.length === 0"
            >
              <option value="">选择账号</option>
              <option 
                v-for="account in accounts" 
                :key="account.id" 
                :value="account.id"
              >
                {{ account.name }}
              </option>
            </select>
          </div>
          <div class="card-body">
            <div v-if="selectedAccount && filteredContent.length > 0" class="space-y-4">
              <div 
                v-for="content in filteredContent" 
                :key="content.id" 
                class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition cursor-pointer"
                @click="viewContent(content)"
              >
                <h3 class="font-medium text-gray-900 line-clamp-1">{{ content.title }}</h3>
                <p class="text-sm text-gray-500 mt-1">{{ formatDate(content.date) }}</p>
                <div class="mt-2 flex items-center">
                  <span 
                    :class="[
                      'px-2 py-1 rounded-full text-xs',
                      content.status === 'published' 
                        ? 'bg-green-100 text-green-800' 
                        : content.status === 'draft' 
                          ? 'bg-yellow-100 text-yellow-800' 
                          : 'bg-blue-100 text-blue-800'
                    ]"
                  >
                    {{ getContentStatusText(content.status) }}
                  </span>
                </div>
              </div>
            </div>
            <div v-else-if="selectedAccount" class="text-center py-8 text-gray-500">
              该账号暂无内容
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              请先选择一个账号
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 添加/编辑账号模态框 -->
    <Modal
      v-model:visible="showAddAccountModal"
      :title="showEditAccountModal ? '编辑账号' : '添加账号'"
      :confirm-text="'保存'"
      :cancel-text="'取消'"
      :show-footer="true"
      size="md"
      @confirm="saveAccount"
      @cancel="closeModal"
    >
      <form @submit.prevent="saveAccount">
        <div class="mb-4">
          <label class="form-label">账号名称</label>
          <input 
            v-model="accountForm.name" 
            type="text" 
            class="form-input w-full" 
            required
          >
        </div>
        
        <div class="mb-4">
          <label class="form-label">AppID</label>
          <input 
            v-model="accountForm.appId" 
            type="text" 
            class="form-input w-full" 
            required
          >
        </div>
        <div class="mb-4">
            <label class="form-label">Account ID</label>
            <input 
              v-model="accountForm.accountId" 
              type="text" 
              class="form-input w-full" 
              required
            >
          </div>
          <div class="mb-4">
            <label class="form-label">AppSecret</label>
            <input 
              v-model="accountForm.appSecret" 
              type="password" 
              class="form-input w-full" 
              required
            >
          </div>
          <div class="mb-4">
            <label class="form-label">WX Footer</label>
            <textarea 
              v-model="accountForm.wxFooter" 
              class="form-input w-full" 
              rows="3"
            ></textarea>
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
      @confirm="confirmDeleteAccount"
      @cancel="showDeleteModal = false"
    >
      <p class="text-gray-700">您确定要删除账号 "{{ accountToDelete?.name }}" 吗？</p>
      <p class="text-sm text-gray-500 mt-2">此操作无法撤销，关联的内容也将被删除。</p>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Modal from '@/components/Modal.vue'
import api from '@/services/api'
import { ChatBubbleLeftRightIcon, PlusIcon, PencilIcon, TrashIcon } from '@heroicons/vue/24/outline'

// 状态
const accounts = ref([])
const content = ref([])
const selectedAccount = ref('')
const showAddAccountModal = ref(false)
const showEditAccountModal = ref(false)
const showDeleteModal = ref(false)
const accountToDelete = ref(null)

const accountForm = ref({
  id: null,
  name: '',
  accountId: '',
  appId: '',
  appSecret: '',
  wxFooter: ''
})

// 计算属性
const filteredContent = computed(() => {
  if (!selectedAccount.value) return []
  return content.value.filter(item => item.accountId === parseInt(selectedAccount.value))
})

// 方法
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const getContentStatusText = (status) => {
  const statusMap = {
    published: '已发布',
    draft: '草稿',
    scheduled: '定时发布'
  }
  return statusMap[status] || '未知'
}

// 获取微信账号列表
const fetchAccounts = async () => {
  try {
    const response = await api.get('/wechat')
    accounts.value = response.data.map(account => ({
      id: account.id,
      name: account.account_name,
      accountId: account.account_id || '',
      appId: account.app_id,
      appSecret: '', // 出于安全考虑，不返回appSecret
      wxFooter: account.wx_footer || '',
      status: 'connected' // 假设所有从后端获取的账号都是已连接状态
    }))
  } catch (error) {
    console.error('获取账号列表失败:', error)
    // 使用模拟数据作为后备
    accounts.value = [
      {
        id: 1,
        name: '公司公众号',
        type: 'official',
        appId: 'wx1234567890abcdef',
        appSecret: 'secret1234567890abcdef',
        status: 'connected'
      },
      {
        id: 2,
        name: '个人视频号',
        type: 'channels',
        appId: 'wx0987654321fedcba',
        appSecret: 'secret0987654321fedcba',
        status: 'disconnected'
      }
    ]
  }
}

// 添加微信账号
const addAccount = async () => {
  try {
    const response = await api.post('/wechat', {
      account_name: accountForm.value.name,
      account_id: accountForm.value.accountId,
      app_id: accountForm.value.appId,
      app_secret: accountForm.value.appSecret,
      wx_footer: accountForm.value.wxFooter
    })
    
    // 添加成功后重新获取账号列表
    await fetchAccounts()
    closeModal()
  } catch (error) {
    console.error('添加账号失败:', error)
    alert('添加账号失败: ' + (error.response?.data?.error || '未知错误'))
  }
}

// 更新微信账号
const updateAccount = async () => {
  try {
    await api.put(`/wechat/${accountForm.value.id}`, {
      account_name: accountForm.value.name,
      account_id: accountForm.value.accountId,
      app_id: accountForm.value.appId,
      app_secret: accountForm.value.appSecret,
      wx_footer: accountForm.value.wxFooter
    })
    
    // 更新成功后重新获取账号列表
    await fetchAccounts()
    closeModal()
  } catch (error) {
    console.error('更新账号失败:', error)
    alert('更新账号失败: ' + (error.response?.data?.error || '未知错误'))
  }
}

// 删除微信账号
const deleteAccount = async () => {
  try {
    await api.delete(`/wechat/${accountToDelete.value.id}`)
    
    // 删除成功后重新获取账号列表
    await fetchAccounts()
    showDeleteModal.value = false
    accountToDelete.value = null
  } catch (error) {
    console.error('删除账号失败:', error)
    alert('删除账号失败: ' + (error.response?.data?.error || '未知错误'))
  }
}

const editAccount = (account) => {
  showAddAccountModal.value = true
  showEditAccountModal.value = true
  accountForm.value = { 
    id: account.id, 
    name: account.name, 
    accountId: account.accountId || '',
    appId: account.appId, 
    appSecret: '',
    wxFooter: account.wxFooter || ''
  }
}

const saveAccount = async () => {
  if (accountForm.value.id) {
    // 更新账号
    await updateAccount()
  } else {
    // 添加账号
    await addAccount()
  }
}

const requestDeleteAccount = (account) => {
  accountToDelete.value = account
  showDeleteModal.value = true
}

const confirmDeleteAccount = async () => {
  if (accountToDelete.value) {
    await deleteAccount()
  }
}

const closeModal = () => {
  showAddAccountModal.value = false
  showEditAccountModal.value = false
}

const viewContent = (contentItem) => {
  alert(`查看内容: ${contentItem.title}`)
  // 这里可以导航到内容详情页面
}

// 组件挂载时获取账号列表
onMounted(() => {
  fetchAccounts()
})
</script>