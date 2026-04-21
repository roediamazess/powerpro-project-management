<script setup lang="ts">
import { ref } from 'vue'
import { Plus, Edit2, Save, X, RefreshCw, User as UserIcon, Mail, Shield, Award } from 'lucide-vue-next'
import { useSettingsStore } from '../../store/settings'
import LookupPopup from '../../components/LookupPopup.vue'
import apiClient from '../../api/api-client'

const props = defineProps<{
  users: any[]
  roles: any[]
  tiers: any[]
}>()

const settingsStore = useSettingsStore()
const isModalOpen = ref(false)
const isSubmitting = ref(false)
const isEdit = ref(false)

const formData = ref<any>({
  username: '',
  fullname: '',
  email: '',
  password: '',
  role_id: '',
  tier_id: '',
  is_active: true
})

const openModal = (user?: any) => {
  console.log('Opening User Modal. Roles:', props.roles, 'Tiers:', props.tiers)
  if (user) {
    formData.value = { ...user, password: '' }
    isEdit.value = true
  } else {
    formData.value = { 
      username: '', 
      fullname: '', 
      email: '', 
      password: '',
      role_id: props.roles[0]?.id || 'USER',
      tier_id: props.tiers[0]?.id || 'TIER1',
      is_active: true
    }
    isEdit.value = false
  }
  isModalOpen.value = true
}

const handleSubmit = async () => {
  isSubmitting.value = true
  try {
    if (isEdit.value) {
      const { user_id, ...updateData } = formData.value
      if (!updateData.password) delete updateData.password
      await apiClient.put(`/users/${user_id}`, updateData)
    } else {
      await apiClient.post('/users/', formData.value)
    }
    await settingsStore.fetchUsers()
    isModalOpen.value = false
  } catch (err) {
    console.error(err)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="space-y-6" v-auto-animate>
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-xl font-bold text-primary italic">User Management</h2>
        <p class="text-[10px] text-secondary font-black uppercase tracking-[0.2em]">Authorized system personnel access control.</p>
      </div>
      <button @click="openModal()" class="!w-auto h-10 px-6 btn-primary bg-accent-cyan shadow-lg shadow-accent-cyan/20">
        <Plus class="w-4 h-4" /> Add User
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="user in users" :key="user.user_id" class="glass-card shadow-sm border border-white/5 p-6 group hover:border-accent-cyan/30 transition-all flex flex-col justify-between">
        <div class="flex items-start justify-between">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-2xl bg-surface-800 flex items-center justify-center text-accent-cyan ring-1 ring-white/5 shadow-inner">
              <UserIcon class="w-6 h-6" />
            </div>
            <div>
              <p class="font-bold text-white group-hover:text-accent-cyan transition-colors">{{ user.fullname }}</p>
              <p class="text-[10px] text-surface-500 font-black uppercase tracking-widest">{{ user.username }}</p>
            </div>
          </div>
          <button @click="openModal(user)" class="p-2 bg-surface-500/5 hover:bg-accent-cyan/20 rounded-xl text-secondary hover:text-accent-cyan transition-all">
            <Edit2 class="w-4 h-4" />
          </button>
        </div>

        <div class="mt-6 space-y-3">
          <div class="flex items-center gap-2 text-xs text-surface-400">
            <Mail class="w-3.5 h-3.5 text-secondary" />
            {{ user.email }}
          </div>
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-1.5 px-2.5 py-1 bg-blue-500/10 text-blue-400 rounded-lg border border-blue-500/20 text-[10px] font-bold">
              <Shield class="w-3 h-3" /> {{ user.role_id }}
            </div>
            <div class="flex items-center gap-1.5 px-2.5 py-1 bg-accent-emerald/10 text-accent-emerald rounded-lg border border-accent-emerald/20 text-[10px] font-bold">
              <Award class="w-3 h-3" /> {{ user.tier_id }}
            </div>
          </div>
        </div>

        <div class="mt-6 pt-4 border-t border-white/5 flex items-center justify-between">
           <span class="px-2 py-0.5 rounded text-[9px] font-black tracking-widest" :class="user.is_active ? 'bg-accent-emerald/10 text-accent-emerald' : 'bg-red-500/10 text-red-500'">
             {{ user.is_active ? 'ACTIVE' : 'LOCKED' }}
           </span>
           <span class="text-[9px] text-surface-600 font-medium">UID: {{ user.user_id.slice(0, 8) }}...</span>
        </div>
      </div>
    </div>

    <!-- User Edit/Create Modal -->
    <Teleport to="body">
      <div v-if="isModalOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-surface-950/40 backdrop-blur-md animate-in fade-in duration-500" @click="isModalOpen = false"></div>
        
        <div class="relative w-full max-w-xl glass border border-white/10 shadow-2xl flex flex-col rounded-[32px] overflow-hidden animate-in fade-in zoom-in duration-300">
          <div class="p-8 border-b border-white/5 bg-surface-500/5 shadow-inner">
             <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-2xl font-black text-primary italic tracking-tight">{{ isEdit ? 'Refine' : 'Register' }} <span class="text-accent-cyan">User Access</span></h3>
                  <p class="text-[10px] text-secondary font-black uppercase tracking-widest mt-1">Credentials & Permissions Hierarchy</p>
                </div>
                <button @click="isModalOpen = false" class="p-2 hover:bg-surface-500/10 rounded-xl text-secondary">
                  <X class="w-6 h-6" />
                </button>
             </div>
          </div>

          <div class="p-8 space-y-6 overflow-y-auto max-h-[70vh] custom-scrollbar">
             <div class="grid grid-cols-2 gap-6">
                <div class="space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Username</label>
                  <input v-model="formData.username" type="text" class="premium-input-field" :disabled="isEdit">
                </div>
                <div class="space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Full Name</label>
                  <input v-model="formData.fullname" type="text" class="premium-input-field">
                </div>
             </div>

             <div class="space-y-2">
                <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Email Address</label>
                <input v-model="formData.email" type="email" class="premium-input-field">
             </div>

             <div class="space-y-2">
                <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Password {{ isEdit ? '(Leave blank to keep)' : '' }}</label>
                <input v-model="formData.password" type="password" class="premium-input-field" placeholder="••••••••">
             </div>

             <div class="grid grid-cols-2 gap-6">
                <div class="space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Role Permission</label>
                  <LookupPopup 
                    v-model="formData.role_id" 
                    :options="roles" 
                    label="Select Role"
                  />
                </div>
                <div class="space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Seniority Tier</label>
                  <LookupPopup 
                    v-model="formData.tier_id" 
                    :options="tiers" 
                    label="Select Tier"
                  />
                </div>
             </div>

             <div class="pt-4">
                <label class="flex items-center gap-4 p-4 bg-surface-500/5 border border-border-app rounded-2xl cursor-pointer hover:border-accent-emerald/20 transition-all">
                  <div class="relative inline-flex items-center">
                    <input type="checkbox" v-model="formData.is_active" class="sr-only peer">
                    <div class="w-11 h-6 bg-surface-500/20 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-accent-emerald shadow-inner"></div>
                  </div>
                  <span class="text-sm font-bold" :class="formData.is_active ? 'text-accent-emerald' : 'text-secondary'">
                    {{ formData.is_active ? 'User Active & Authorized' : 'Account Locked / Disabled' }}
                  </span>
                </label>
             </div>
          </div>

          <div class="p-8 border-t border-white/5 bg-surface-500/5 flex justify-end gap-3">
             <button @click="handleSubmit" :disabled="isSubmitting" class="px-8 h-12 btn-primary bg-accent-cyan flex items-center justify-center gap-2">
                <Save v-if="!isSubmitting" class="w-4 h-4" />
                <RefreshCw v-else class="w-4 h-4 animate-spin" />
                Save Access
             </button>
             <button @click="isModalOpen = false" class="px-8 h-12 glass text-primary rounded-xl">Cancel</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
