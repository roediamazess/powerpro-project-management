<script setup lang="ts">
import { ref } from 'vue'
import { Plus, Edit2, Save, X, RefreshCw } from 'lucide-vue-next'
import { useSettingsStore } from '../../store/settings'
import LookupPopup from '../../components/LookupPopup.vue'

const props = defineProps<{
  title: string
  subtitle: string
  items: any[]
  endpoint: string
  extraFields?: any[] // For specialized fields like area_id in sub_areas
  extraData?: any[] // Data for dropdowns/options for extraFields
}>()

const settingsStore = useSettingsStore()
const isModalOpen = ref(false)
const isSubmitting = ref(false)
const isEdit = ref(false)

const formData = ref<any>({
  id: '',
  name: '',
  listindex: 0,
  is_active: true
})

const openModal = (item?: any) => {
  if (item) {
    formData.value = { ...item }
    isEdit.value = true
  } else {
    formData.value = { 
      id: '', 
      name: '', 
      listindex: 0, 
      is_active: true,
      ...props.extraFields?.reduce((acc, field) => ({ ...acc, [field.key]: '' }), {})
    }
    isEdit.value = false
  }
  isModalOpen.value = true
}

const handleSubmit = async () => {
  isSubmitting.value = true
  try {
    await settingsStore.saveLookup(props.endpoint, formData.value, isEdit.value)
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
        <h2 class="text-xl font-bold text-primary italic">{{ title }}</h2>
        <p class="text-[10px] text-secondary font-black uppercase tracking-[0.2em]">{{ subtitle }}</p>
      </div>
      <button @click="openModal()" class="!w-auto h-10 px-6 btn-primary bg-accent-cyan shadow-lg shadow-accent-cyan/20">
        <Plus class="w-4 h-4" /> Add New
      </button>
    </div>

    <div class="overflow-x-auto rounded-3xl border border-border-app bg-surface-500/5 backdrop-blur-sm shadow-xl">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="border-b border-border-app text-[10px] font-black text-secondary uppercase tracking-widest">
            <th class="py-5 px-6">ID</th>
            <th class="py-5 px-6">Name</th>
            <th v-if="extraFields?.length" v-for="field in extraFields" :key="field.key" class="py-5 px-6">{{ field.label }}</th>
            <th class="py-5 px-6">Index</th>
            <th class="py-5 px-6">Status</th>
            <th class="py-5 px-6 text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-border-app">
          <tr v-for="item in items" :key="item.id" class="group hover:bg-surface-500/10 transition-colors relative">
            <td class="py-5 px-6 text-sm font-bold text-accent-cyan">{{ item.id }}</td>
            <td class="py-5 px-6 text-sm text-primary font-medium">{{ item.name }}</td>
            <td v-if="extraFields?.length" v-for="field in extraFields" :key="field.key" class="py-5 px-6 text-sm text-secondary font-medium">
               {{ extraData?.find(d => d.id === item[field.key])?.name || item[field.key] }}
            </td>
            <td class="py-5 px-6 text-sm text-secondary">{{ item.listindex }}</td>
            <td class="py-5 px-6">
              <span class="px-3 py-1 rounded-full text-[10px] font-black tracking-wider shadow-inner" :class="item.is_active ? 'bg-accent-emerald/10 text-accent-emerald ring-1 ring-accent-emerald/20' : 'bg-red-500/10 text-red-500 ring-1 ring-red-500/20'">
                {{ item.is_active ? 'ACTIVE' : 'INACTIVE' }}
              </span>
            </td>
            <td class="py-5 px-6 text-right">
              <button @click="openModal(item)" class="p-2.5 bg-surface-500/10 hover:bg-accent-cyan/20 rounded-xl text-secondary hover:text-accent-cyan transition-all transform hover:-translate-y-0.5 active:scale-95">
                <Edit2 class="w-4 h-4" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Centered Modal (Standardized) -->
    <Teleport to="body">
      <div v-if="isModalOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4 overflow-hidden">
        <!-- Backdrop with standardized blur -->
        <div class="absolute inset-0 bg-surface-950/40 backdrop-blur-md animate-in fade-in duration-500" @click="isModalOpen = false"></div>
        
        <!-- Centered Modal Panel -->
        <div class="relative w-full max-w-lg glass border border-white/10 shadow-2xl flex flex-col rounded-[32px] overflow-hidden animate-in fade-in zoom-in duration-300">
          <!-- Header -->
          <div class="p-8 border-b border-border-app bg-surface-500/5 shadow-inner">
             <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-2xl font-black text-primary italic tracking-tight">{{ isEdit ? 'Update' : 'Register' }} <span class="text-accent-cyan">{{ title }}</span></h3>
                  <p class="text-[10px] text-secondary font-black uppercase tracking-widest mt-1">Industrial Metadata Configuration</p>
                </div>
                <button @click="isModalOpen = false" class="p-3 hover:bg-surface-500/10 rounded-2xl text-secondary hover:text-primary transition-all">
                  <X class="w-6 h-6" />
                </button>
             </div>
          </div>

          <!-- Scrollable Content -->
          <div class="p-8 space-y-8 bg-surface-500/5 overflow-y-auto max-h-[70vh] custom-scrollbar">
             <div class="space-y-6">
                <div v-if="!isEdit" class="group space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1 group-focus-within:text-accent-cyan transition-colors">Unique Identifier (ID)</label>
                  <input v-model="formData.id" type="text" class="premium-input-field uppercase font-bold tracking-widest" placeholder="E.G. BALI">
                </div>
                
                <div class="group space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1 group-focus-within:text-accent-cyan transition-colors">Display Name</label>
                  <input v-model="formData.name" type="text" class="premium-input-field" placeholder="Enter descriptive name...">
                </div>

                <!-- Extra Fields (like parent Area) -->
                <div v-for="field in extraFields" :key="field.key" class="group space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1 group-focus-within:text-accent-cyan transition-colors">{{ field.label }}</label>
                  <LookupPopup 
                    v-model="formData[field.key]" 
                    :options="extraData ? extraData.map(d => ({id: d.id, name: d.name})) : []" 
                    :label="field.label"
                  />
                </div>

                <div class="grid grid-cols-2 gap-6">
                  <div class="group space-y-2">
                    <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1 group-focus-within:text-accent-cyan transition-colors">Sort Index</label>
                    <input v-model.number="formData.listindex" type="number" class="premium-input-field font-bold">
                  </div>
                  <div class="group space-y-2">
                     <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1 group-focus-within:text-accent-cyan transition-colors">System Status</label>
                     <label class="flex items-center gap-4 p-[11px] bg-surface-500/5 border border-border-app rounded-2xl cursor-pointer hover:border-accent-emerald/20 transition-all">
                        <div class="relative inline-flex items-center">
                          <input type="checkbox" v-model="formData.is_active" class="sr-only peer">
                          <div class="w-11 h-6 bg-surface-500/20 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-accent-emerald shadow-inner"></div>
                        </div>
                        <span class="text-sm font-bold transition-colors" :class="formData.is_active ? 'text-accent-emerald' : 'text-secondary'">{{ formData.is_active ? 'Active' : 'Disabled' }}</span>
                     </label>
                  </div>
                </div>
             </div>
          </div>

          <!-- Combined Footer Action Bar (RIGHT ALIGNED) -->
          <div class="p-8 border-t border-border-app bg-surface-500/5 flex flex-row gap-4 items-center justify-end">
            <!-- Save/Create -->
            <button @click="handleSubmit" :disabled="isSubmitting" class="w-auto px-10 h-14 btn-primary bg-gradient-to-r from-accent-emerald to-accent-cyan shadow-xl shadow-accent-emerald/20 flex items-center justify-center gap-3 active:scale-95 transition-all">
              <Save v-if="!isSubmitting" class="w-5 h-5" />
              <RefreshCw v-else class="w-5 h-5 animate-spin" />
              <span class="text-sm font-bold uppercase tracking-widest">
                {{ isEdit ? 'Save' : 'Create' }}
              </span>
            </button>

            <!-- Cancel/Close -->
            <button @click="isModalOpen = false" class="w-auto px-10 h-14 glass text-primary text-sm font-bold rounded-2xl hover:bg-surface-500/5 border border-border-app transition-all uppercase tracking-widest">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.scrollbar-none::-webkit-scrollbar { display: none; }
.scrollbar-none { -ms-overflow-style: none; scrollbar-width: none; }
.text-shadow-glow { text-shadow: 0 0 20px rgba(34, 211, 238, 0.3); }
.shadow-secondary { box-shadow: inset 0 0 20px rgba(16, 185, 129, 0.2); }
</style>
