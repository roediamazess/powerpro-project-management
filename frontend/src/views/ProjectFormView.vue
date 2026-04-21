<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { X, Save, Users, RefreshCw, Layers } from 'lucide-vue-next'
import { useProjectStore } from '../store/project'
import { usePartnerStore } from '../store/partner'
import { useSettingsStore } from '../store/settings'
import LookupPopup from '../components/LookupPopup.vue'
import DatePickerPopup from '../components/DatePickerPopup.vue'
import apiClient from '../api/api-client'

const props = defineProps<{
  project?: any
}>()

const emit = defineEmits(['close', 'success'])
const projectStore = useProjectStore()
const partnerStore = usePartnerStore()
const settingsStore = useSettingsStore()

const currentTab = ref('scope')
const users = ref<any[]>([])
const formData = ref({
  name: '',
  partner_id: '',
  type_id: '',
  status_id: '',
  arrangement_id: '',
  assignment_id: '',
  start_date: '',
  end_date: '',
  point_req: 0,
  pic_ids: [] as string[]
})

onMounted(async () => {
  // Fetch dependencies
  partnerStore.fetchPartners()
  settingsStore.fetchProjectLookups()
  
  try {
    const res = await apiClient.get('/api/v1/users') // Assumed endpoint
    users.value = res.data
  } catch (e) {
    // Fallback if user endpoint not ready
    users.value = []
  }

  if (props.project) {
    formData.value = { 
      ...props.project, 
      pic_ids: props.project.pics?.map((p: any) => p.user_id) || [] 
    }
  }
})

const isSubmitting = ref(false)
const error = ref('')

const handleSubmit = async () => {
  if (!formData.value.partner_id || !formData.value.name) {
    error.value = 'Mohon isi Nama Proyek dan pilih Partner klien.'
    return
  }

  isSubmitting.value = true
  error.value = ''
  try {
    if (props.project?.project_id) {
      await projectStore.updateProject(props.project.project_id, formData.value)
    } else {
      await projectStore.createProject(formData.value)
    }
    emit('success')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Gagal menyimpan data proyek.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6 overflow-hidden">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-surface-950/40 backdrop-blur-md" @click="emit('close')"></div>

    <!-- Panel -->
    <div v-auto-animate class="relative w-full max-w-4xl max-h-[90vh] glass border border-white/10 shadow-2xl flex flex-col rounded-[32px] overflow-hidden animate-in fade-in zoom-in duration-300">
      <!-- Header -->
      <div class="p-8 border-b border-border-app bg-surface-500/5 flex flex-col gap-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-2xl bg-accent-cyan/10 border border-accent-cyan/20 flex items-center justify-center text-accent-cyan shadow-lg">
              <Layers class="w-7 h-7" />
            </div>
            <div>
              <h2 class="text-2xl font-bold text-primary tracking-tight italic">
                {{ props.project ? 'Refine Project' : 'Initialize New Project' }}
              </h2>
              <p class="text-[10px] text-secondary font-black tracking-widest uppercase mt-0.5">Control Module v2.1</p>
            </div>
          </div>
          <button @click="emit('close')" class="p-2 hover:bg-surface-500/10 rounded-xl text-secondary transition-all">
            <X class="w-6 h-6" />
          </button>
        </div>

        <div class="flex gap-2 p-1.5 bg-surface-500/5 rounded-2xl w-fit ring-1 ring-border-app">
          <button 
            @click="currentTab = 'scope'"
            class="px-6 py-2.5 text-sm font-bold rounded-xl transition-all flex items-center gap-2"
            :class="currentTab === 'scope' ? 'bg-accent-cyan/10 text-accent-cyan ring-1 ring-accent-cyan/20 shadow-lg' : 'text-secondary hover:text-primary'"
          >
            Scope & Timeline
          </button>
          <button 
            @click="currentTab = 'team'"
            class="px-6 py-2.5 text-sm font-bold rounded-xl transition-all flex items-center gap-2"
            :class="currentTab === 'team' ? 'bg-accent-emerald/10 text-accent-emerald ring-1 ring-accent-emerald/20 shadow-lg' : 'text-secondary hover:text-primary'"
          >
            Team Assignment
          </button>
        </div>
      </div>

      <!-- Content -->
      <div v-auto-animate class="flex-1 overflow-y-auto p-8 custom-scrollbar">
        <div v-if="error" class="bg-red-500/10 border border-red-500/20 p-4 rounded-xl text-red-400 text-sm mb-6 flex items-center gap-3">
          <AlertCircle class="w-5 h-5 flex-shrink-0" />
          {{ error }}
        </div>

        <!-- Tab 1: Scope -->
        <div v-if="currentTab === 'scope'" class="space-y-10">
          <section class="space-y-6">
            <div class="flex items-center gap-4">
              <div class="h-px flex-1 bg-gradient-to-r from-transparent to-border-app"></div>
              <h3 class="text-[10px] font-black text-secondary uppercase tracking-[0.2em]">Client & Identity</h3>
              <div class="h-px flex-1 bg-gradient-to-l from-transparent to-border-app"></div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-4">
                <div class="space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Project Name</label>
                  <div class="relative group">
                    <input v-model="formData.name" type="text" class="premium-input-field" placeholder="e.g. Implementation Phase 1">
                  </div>
                </div>
                <div class="space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Select Partner Client</label>
                  <LookupPopup 
                    v-model="formData.partner_id" 
                    :options="partnerStore.partners.map(p => ({id: p.partner_id, name: p.name}))" 
                    label="Select Partner Client"
                  />
                </div>
              </div>

              <!-- Configuration Lookups -->
              <div class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                  <div class="space-y-2">
                    <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Project Type</label>
                    <LookupPopup 
                      v-model="formData.type_id" 
                      :options="settingsStore.projectLookups.types.filter(x => x.is_active)" 
                      label="Project Type"
                    />
                  </div>
                  <div class="space-y-2">
                    <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Assignment</label>
                    <LookupPopup 
                      v-model="formData.assignment_id" 
                      :options="settingsStore.projectLookups.assignments.filter(x => x.is_active)" 
                      label="Assignment Type"
                    />
                  </div>
                  <div class="space-y-2">
                    <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Arrangement</label>
                    <LookupPopup 
                      v-model="formData.arrangement_id" 
                      :options="settingsStore.projectLookups.arrangements.filter(x => x.is_active)" 
                      label="Arrangement Data"
                    />
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section class="space-y-6">
            <div class="flex items-center gap-4">
              <div class="h-px flex-1 bg-gradient-to-r from-transparent to-surface-800"></div>
              <h3 class="text-[10px] font-black text-surface-500 uppercase tracking-[0.2em]">Timeline & Performance</h3>
              <div class="h-px flex-1 bg-gradient-to-l from-transparent to-surface-800"></div>
            </div>

            <div class="grid grid-cols-2 lg:grid-cols-4 gap-6">
              <div class="space-y-2">
                <label class="text-xs font-bold text-surface-400 uppercase tracking-widest pl-1">Start Date</label>
                <DatePickerPopup 
                  v-model="formData.start_date" 
                  label="Start Date"
                />
              </div>
              <div class="space-y-2">
                <label class="text-xs font-bold text-surface-400 uppercase tracking-widest pl-1">End Date</label>
                <DatePickerPopup 
                  v-model="formData.end_date" 
                  label="End Date"
                />
              </div>
              <div class="space-y-2">
                <label class="text-xs font-bold text-surface-400 uppercase tracking-widest pl-1">Point Req</label>
                <input v-model.number="formData.point_req" type="number" class="w-full bg-surface-900/50 border border-white/5 rounded-2xl py-4 px-5 text-white outline-none focus:border-accent-cyan/50 transition-all">
              </div>
              <div class="space-y-2">
                <label class="text-xs font-bold text-surface-400 uppercase tracking-widest pl-1">Status</label>
                <LookupPopup 
                  v-model="formData.status_id" 
                  :options="settingsStore.projectLookups.statuses.filter(x => x.is_active)" 
                  label="Project Status"
                />
              </div>
            </div>
          </section>
        </div>

        <!-- Tab 2: Team -->
        <div v-if="currentTab === 'team'" class="space-y-8 py-4">
           <div class="text-center space-y-2 mb-10">
              <h3 class="text-2xl font-bold text-white italic">Assign <span class="text-accent-emerald">Field Officers</span></h3>
              <p class="text-surface-500 text-sm max-w-sm mx-auto">Select the team members responsible for this project's success.</p>
           </div>
           
           <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
             <div v-for="i in 4" :key="i" class="p-5 rounded-[24px] border border-white/5 bg-surface-900/40 flex items-center justify-between group hover:border-accent-emerald/30 hover:bg-surface-900/60 transition-all cursor-pointer ring-1 ring-inset ring-white/[0.02]">
               <div class="flex items-center gap-4">
                 <div class="w-12 h-12 rounded-full bg-surface-800 flex items-center justify-center font-bold text-accent-emerald ring-2 ring-white/5 shadow-inner">U{{ i }}</div>
                 <div>
                   <p class="text-sm font-bold text-white group-hover:text-accent-emerald transition-colors">Field Officer {{ i }}</p>
                   <p class="text-[10px] text-surface-500 font-bold uppercase tracking-widest">Operations</p>
                 </div>
               </div>
               <div class="w-6 h-6 rounded-lg border border-surface-700 flex items-center justify-center group-hover:border-accent-emerald/50 transition-colors">
                 <div class="w-3.5 h-3.5 bg-accent-emerald rounded opacity-0 group-hover:opacity-100 transition-opacity shadow-[0_0_10px_rgba(16,185,129,0.4)]"></div>
               </div>
             </div>
           </div>
        </div>
      </div>

      <!-- Footer Action Bar (RIGHT ALIGNED) -->
      <div class="p-8 border-t border-border-app bg-surface-500/5 flex flex-row gap-4 items-center justify-end">
        <!-- Initialize/Save -->
        <button @click="handleSubmit" :disabled="isSubmitting" class="w-auto px-12 h-14 btn-primary bg-gradient-to-r from-accent-emerald to-accent-cyan shadow-xl shadow-accent-emerald/20 flex items-center justify-center gap-3 active:scale-95 transition-all">
          <Save v-if="!isSubmitting" class="w-5 h-5" />
          <RefreshCw v-else class="w-5 h-5 animate-spin" />
          <span class="text-sm font-bold uppercase tracking-widest">
            {{ props.project ? 'Save' : 'Create' }}
          </span>
        </button>

        <!-- Cancel/Close -->
        <button @click="emit('close')" class="w-auto px-12 h-14 glass text-primary text-sm font-bold rounded-2xl hover:bg-surface-500/5 border border-border-app transition-all uppercase tracking-widest">
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>

