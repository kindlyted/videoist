<template>
  <div class="px-container py-container">
    <div class="mb-6 flex items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">{{ $t('wechatManagement.title') }}</h1>
        <p class="text-gray-600 mt-1">{{ $t('wechatManagement.description') }}</p>
      </div>
      <ChatBubbleLeftRightIcon class="h-8 w-8 text-green-500 ml-4" />
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 账号列表 -->
      <div class="lg:col-span-2">
        <div class="card">
          <div class="card-header flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
            <h2 class="card-title">{{ $t('wechatManagement.accounts') }}</h2>
            <button 
              @click="showAddAccountModal = true"
              class="btn btn-primary flex items-center"
            >
              <PlusIcon class="h-5 w-5 mr-2" />
              {{ $t('wechatManagement.addAccount') }}
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
                    <p class="text-sm text-gray-500 mt-1">{{ $t('wechatManagement.accountIdLabel') }}: {{ account.accountId }}</p>
                  <p class="text-sm text-gray-500 mt-1">{{ $t('wechatManagement.appIdLabel') }}: {{ account.appId }}</p>
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
                      {{ $t('wechatManagement.edit') }}
                    </button>
                    <button 
                      @click="requestDeleteAccount(account)"
                      class="text-red-600 hover:text-red-900 flex items-center"
                    >
                      <TrashIcon class="h-4 w-4 mr-1" />
                      {{ $t('wechatManagement.delete') }}
                    </button>
                  </div>
                </div>
                <!-- 移除了状态显示部分 -->
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              {{ $t('wechatManagement.noAccounts') }}
            </div>
          </div>
        </div>
      </div>
      
      <!-- 内容列表 -->
      <div>
        <div class="card">
          <div class="card-header flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
            <h2 class="card-title">{{ $t('wechatManagement.content') }}</h2>
            <select 
              v-model="selectedAccount" 
              class="form-select w-full sm:w-auto"
              :disabled="accounts.length === 0"
            >
              <option value="">{{ $t('wechatManagement.selectAccount') }}</option>
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
              {{ $t('wechatManagement.noContent') }}
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              {{ $t('wechatManagement.noAccountSelected') }}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 添加/编辑账号模态框 -->
    <Modal
        v-model:visible="showAddAccountModal"
        :title="showEditAccountModal ? $t('wechatManagement.editAccount') : $t('wechatManagement.addAccount')"
        :confirm-text="showEditAccountModal ? $t('wechatManagement.update') : $t('wechatManagement.add')"
        :cancel-text="$t('wechatManagement.cancel')"
        :show-footer="true"
        size="md"
        @confirm="saveAccount"
        @cancel="closeModal"
      >
      <form @submit.prevent="saveAccount">
        <div class="mb-4">
          <label class="form-label">{{ $t('wechatManagement.accountName') }}</label>
          <input 
            v-model="accountForm.name" 
            type="text" 
            class="form-input w-full" 
            :placeholder="$t('wechatManagement.accountNamePlaceholder')"
            required
          >
        </div>
        
        <div class="mb-4">
          <label class="form-label">{{ $t('wechatManagement.appId') }}</label>
          <input 
            v-model="accountForm.appId" 
            type="text" 
            class="form-input w-full" 
            :placeholder="$t('wechatManagement.appIdPlaceholder')"
            required
          >
        </div>
        <div class="mb-4">
            <label class="form-label">{{ $t('wechatManagement.accountId') }}</label>
            <input 
              v-model="accountForm.accountId" 
              type="text" 
              class="form-input w-full" 
              :placeholder="$t('wechatManagement.accountIdPlaceholder')"
              required
            >
          </div>
          <div class="mb-4">
            <label class="form-label">{{ $t('wechatManagement.appSecret') }}</label>
            <input 
              v-model="accountForm.appSecret" 
              type="password" 
              class="form-input w-full" 
              :placeholder="$t('wechatManagement.appSecretPlaceholder')"
              required
            >
          </div>
          <div class="mb-4">
            <label class="form-label">{{ $t('wechatManagement.wxFooter') }}</label>
            <textarea 
              v-model="accountForm.wxFooter" 
              class="form-input w-full" 
              :placeholder="$t('wechatManagement.wxFooterPlaceholder')"
              rows="3"
            ></textarea>
          </div>
      </form>
    </Modal>
    
    <!-- 删除确认模态框 -->
    <Modal
      v-model:visible="showDeleteModal"
      :title="$t('wechatManagement.confirmDeleteTitle')"
      :confirm-text="$t('wechatManagement.delete')"
      :cancel-text="$t('wechatManagement.cancel')"
      :show-footer="true"
      size="md"
      confirm-button-class="bg-red-600 hover:bg-red-700 focus:ring-red-500"
      @confirm="confirmDeleteAccount"
      @cancel="showDeleteModal = false"
    >
      <p class="text-gray-700">{{ $t('wechatManagement.deleteConfirm', { name: accountToDelete?.name }) }}</p>
      <p class="text-sm text-gray-500 mt-2">{{ $t('wechatManagement.deleteWarning') }}</p>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import Modal from '@/components/Modal.vue'
import api from '@/services/api'
import { ChatBubbleLeftRightIcon, PlusIcon, PencilIcon, TrashIcon } from '@heroicons/vue/24/outline'
import { handleApiError, getErrorMessageKey } from '@/utils/errorHandler'

const { t } = useI18n()

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

// 验证表单
const validateForm = () => {
  if (!accountForm.value.name || !accountForm.value.appId || !accountForm.value.accountId || !accountForm.value.appSecret || !accountForm.value.wxFooter) {
    alert(t('wechatManagement.allFieldsRequired'))
    return false
  }
  return true
}

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
    published: t('wechatManagement.contentStatus.published'),
    draft: t('wechatManagement.contentStatus.draft'),
    scheduled: t('wechatManagement.contentStatus.scheduled')
  }
  return statusMap[status] || t('unknown')
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
    
    alert(errorMessage || '获取账号列表失败');
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
    if (!validateForm()) return
    
    const newAccount = {
      ...accountForm.value,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    
    const response = await api.post('/wechat/accounts', newAccount)
    accounts.value.push(response.data)
    closeModal()
    alert(t('wechatManagement.accountAdded'))
    
    // 重置表单
    Object.keys(accountForm.value).forEach(key => {
      accountForm.value[key] = ''
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
    
    alert(errorMessage || t('wechatManagement.addAccountFailed'));
  }
}

// 更新微信账号
const updateAccount = async () => {
  try {
    if (!validateForm()) return
    
    const updatedAccount = {
      ...accountForm.value,
      updated_at: new Date().toISOString()
    }
    
    const response = await api.put(`/wechat/accounts/${accountForm.value.id}`, updatedAccount)
    
    // 更新本地数据
    const index = accounts.value.findIndex(account => account.id === accountForm.value.id)
    if (index !== -1) {
      accounts.value[index] = { ...accounts.value[index], ...response.data }
    }
    
    closeModal()
    alert(t('wechatManagement.accountUpdated'))
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
    
    alert(errorMessage || t('wechatManagement.updateAccountFailed'));
  }
}

// 删除微信账号
const deleteAccount = async () => {
  try {
    await api.delete(`/wechat/accounts/${accountToDelete.value.id}`)
    
    // 删除成功后重新获取账号列表
    await fetchAccounts()
    showDeleteModal.value = false
    accountToDelete.value = null
    alert(t('wechatManagement.accountDeleted'))
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
    
    alert(errorMessage || t('wechatManagement.deleteAccountFailed'));
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