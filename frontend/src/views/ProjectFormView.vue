<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { X, Save, Users, RefreshCw, Layers, CheckCircle, Plus, AlertCircle, QrCode } from 'lucide-vue-next'
import { useProjectStore } from '../store/project'
import { usePartnerStore } from '../store/partner'
import { useSettingsStore } from '../store/settings'
import LookupPopup from '../components/LookupPopup.vue'
import DatePickerPopup from '../components/DatePickerPopup.vue'
import TrainingManagerModal from '../components/TrainingManagerModal.vue'
import apiClient from '../api/api-client'

const showTrainingManager = ref(false)

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
  cnc_id: '',
  name: '',
  partner_id: '',
  type_id: 'MAINTENANCE',
  status_id: 'SCHEDULED',
  information_id: '',
  start_date: '',
  end_date: '',
  total_days: 1,
  point_req: 0,
  status: 'OPEN',
  pic_assignments: [] as any[],
  
  // Document Tracking Fields
  handover_or: '',
  handover_days: 0,
  pic_kpi_2: 0,
  check_or: '',
  check_days: 0,
  officer_kpi2: 0,
  validation_date: '',
  validation_days: 0,
  okr_kpi2: 0,

  // Automation Reminders Fields
  s1_estimation: '',
  s1_over_days: 0,
  s1_count_email_sent: '',
  s2_email_sent: '',
  s3_email_sent: ''
})

const addPIC = () => {
  formData.value.pic_assignments.push({
    user_id: '',
    arrangement_id: 'SELF',
    assignment_id: 'SELF',
    start_date: formData.value.start_date || '',
    end_date: formData.value.end_date || '',
    total_days: formData.value.total_days || 1,
    status: 'OPEN'
  })
}

const removePIC = (index: number) => {
  formData.value.pic_assignments.splice(index, 1)
}

// Auto-calculate total days
import { watch } from 'vue'
watch([() => formData.value.start_date, () => formData.value.end_date], ([start, end], [oldStart]) => {
  // If Start Date changed and is now after End Date, clear End Date
  if (start && end && start > end && start !== oldStart) {
    formData.value.end_date = ''
    formData.value.total_days = 0
    return
  }

  if (start && end) {
    const s = new Date(start)
    const e = new Date(end)
    const diff = e.getTime() - s.getTime()
    const days = Math.floor(diff / (1000 * 60 * 60 * 24)) + 1
    formData.value.total_days = days > 0 ? days : 0
  } else {
    formData.value.total_days = 0
  }

  // Validate PIC assignments when Project timeline changes
  formData.value.pic_assignments.forEach(pic => {
    // If PIC Start is before Project Start, bump it to Project Start
    if (start && pic.start_date && pic.start_date < start) {
      pic.start_date = start
    }
    // If PIC End is after Project End, pull it back to Project End
    if (end && pic.end_date && pic.end_date > end) {
      pic.end_date = end
    }
    // Cross-check: Start cannot be after project End
    if (end && pic.start_date && pic.start_date > end) {
      pic.start_date = end
    }
    // Cross-check: End cannot be before project Start
    if (start && pic.end_date && pic.end_date < start) {
      pic.end_date = start
    }
  })
})

// Deep watch for PIC assignments to calculate days
watch(() => formData.value.pic_assignments, (pics) => {
  pics.forEach((pic: any) => {
    if (pic.start_date && pic.end_date) {
      if (pic.start_date > pic.end_date) {
        pic.end_date = ''
        pic.total_days = 0
      } else {
        const s = new Date(pic.start_date)
        const e = new Date(pic.end_date)
        const diff = e.getTime() - s.getTime()
        const days = Math.floor(diff / (1000 * 60 * 60 * 24)) + 1
        pic.total_days = days > 0 ? days : 0
      }
    }
  })
}, { deep: true })

// Document Tracking Calculations
watch(() => formData.value.handover_or, (val) => {
  if (val && formData.value.end_date) {
    const start = new Date(formData.value.end_date)
    const end = new Date(val)
    const diff = end.getTime() - start.getTime()
    formData.value.handover_days = Math.floor(diff / (1000 * 60 * 60 * 24))
  } else {
    formData.value.handover_days = 0
  }
})

watch(() => formData.value.check_or, (val) => {
  if (val && formData.value.handover_or) {
    const start = new Date(formData.value.handover_or)
    const end = new Date(val)
    const diff = end.getTime() - start.getTime()
    formData.value.check_days = Math.floor(diff / (1000 * 60 * 60 * 24))
  } else {
    formData.value.check_days = 0
  }
})

watch(() => formData.value.validation_date, (val) => {
  if (val && formData.value.check_or) {
    const start = new Date(formData.value.check_or)
    const end = new Date(val)
    const diff = end.getTime() - start.getTime()
    formData.value.validation_days = Math.floor(diff / (1000 * 60 * 60 * 24))
  } else {
    formData.value.validation_days = 0
  }
})

watch(() => formData.value.s1_estimation, (val) => {
  if (val && formData.value.end_date) {
    const start = new Date(formData.value.end_date)
    const end = new Date(val)
    const diff = end.getTime() - start.getTime()
    formData.value.s1_over_days = Math.floor(diff / (1000 * 60 * 60 * 24))
  } else {
    formData.value.s1_over_days = 0
  }
})

onMounted(async () => {
  // Fetch dependencies
  partnerStore.fetchPartners()
  settingsStore.fetchProjectLookups()
  
  try {
    const res = await apiClient.get('/users/')
    users.value = res.data
  } catch (e) {
    // Fallback if user endpoint not ready
    users.value = []
  }

  if (props.project) {
    formData.value = { 
      ...props.project,
      cnc_id: props.project.cnc_id || '',
      information_id: props.project.information_id || '',
      pic_assignments: props.project.pic_assignments?.map((p: any) => ({
        user_id: p.user_id,
        arrangement_id: p.arrangement_id || 'SELF',
        assignment_id: p.assignment_id || 'SELF',
        start_date: p.start_date || props.project.start_date,
        end_date: p.end_date || props.project.end_date,
        total_days: p.total_days || props.project.total_days,
        status: p.status || 'OPEN'
      })) || [],
      status: props.project.status || 'OPEN'
    }

    // Force date boundaries for PICs on load
    formData.value.pic_assignments.forEach((pic: any) => {
      if (formData.value.start_date && pic.start_date && pic.start_date < formData.value.start_date) {
        pic.start_date = formData.value.start_date
      }
      if (formData.value.end_date && pic.end_date && pic.end_date > formData.value.end_date) {
        pic.end_date = formData.value.end_date
      }
    })
  }
})

const isSubmitting = ref(false)
const error = ref('')

const handleSubmit = async () => {
  if (!formData.value.name || !formData.value.partner_id || !formData.value.start_date || !formData.value.end_date || !formData.value.information_id) {
    error.value = 'Mohon isi Name, Partner, Start Date, End Date dan Project Information.'
    return
  }

  // Validate Team Assignments
  for (const pic of formData.value.pic_assignments) {
    if (!pic.user_id || !pic.arrangement_id || !pic.assignment_id || !pic.start_date || !pic.end_date) {
      error.value = 'Mohon lengkapi data Officer (Officer, Arrangement, Assignment, Start & End Date).'
      return
    }
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
  <Teleport to="body">
    <div class="fixed inset-0 z-[80] flex items-center justify-center p-4 sm:p-6 overflow-hidden">
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
                <div class="flex items-center gap-3 mt-1">
                  <p class="text-[10px] text-secondary font-black tracking-widest uppercase">Control Module v2.1</p>
                  <div v-if="formData.status === 'APPROVED'" class="px-2 py-0.5 bg-accent-emerald text-white text-[8px] font-black uppercase tracking-widest rounded-full flex items-center gap-1 shadow-lg shadow-accent-emerald/20">
                    <CheckCircle class="w-2.5 h-2.5" /> Approved
                  </div>
                  <div v-else class="px-2 py-0.5 bg-surface-700 text-surface-400 text-[8px] font-black uppercase tracking-widest rounded-full">
                    Draft / Open
                  </div>
                </div>
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
            <button 
              @click="currentTab = 'document'"
              class="px-6 py-2.5 text-sm font-bold rounded-xl transition-all flex items-center gap-2"
              :class="currentTab === 'document' ? 'bg-orange-400/10 text-orange-400 ring-1 ring-orange-400/20 shadow-lg' : 'text-secondary hover:text-primary'"
            >
              Document Tracking
            </button>
            <button 
              @click="currentTab = 'automation'"
              class="px-6 py-2.5 text-sm font-bold rounded-xl transition-all flex items-center gap-2"
              :class="currentTab === 'automation' ? 'bg-accent-amber/10 text-accent-amber ring-1 ring-accent-amber/20 shadow-lg' : 'text-secondary hover:text-primary'"
            >
              Automation Reminders
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
                  <div class="grid grid-cols-3 gap-4">
                    <div class="space-y-2 col-span-1">
                      <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">CNC ID</label>
                      <input v-model="formData.cnc_id" type="text" class="premium-input-field" placeholder="Optional" :disabled="formData.status === 'APPROVED'">
                    </div>
                    <div class="space-y-2 col-span-2">
                      <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Project Name <span class="text-red-500">*</span></label>
                      <input v-model="formData.name" type="text" class="premium-input-field" placeholder="Target Scope Name" :disabled="formData.status === 'APPROVED'">
                    </div>
                  </div>
                  <div class="space-y-2">
                    <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Select Partner Client <span class="text-red-500">*</span></label>
                    <LookupPopup 
                      v-model="formData.partner_id" 
                      :options="partnerStore.partners.map(p => ({id: p.partner_id, name: p.name}))" 
                      label="Select Partner Client"
                      :disabled="formData.status === 'APPROVED'"
                    />
                  </div>
                </div>

                <!-- Configuration Lookups -->
                <div class="space-y-4">
                  <div class="grid grid-cols-2 gap-4">
                    <div class="space-y-2">
                      <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Project Type <span class="text-red-500">*</span></label>
                      <LookupPopup 
                        v-model="formData.type_id" 
                        :options="settingsStore.projectLookups.types.filter(x => x.is_active)" 
                        label="Project Type"
                        :disabled="formData.status === 'APPROVED'"
                      />
                    </div>
                    <div class="space-y-2">
                      <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Status <span class="text-red-500">*</span></label>
                      <LookupPopup 
                        v-model="formData.status_id" 
                        :options="settingsStore.projectLookups.statuses.filter(x => x.is_active)" 
                        label="Project Status"
                        :disabled="formData.status === 'APPROVED'"
                      />
                    </div>
                    <div class="space-y-2 col-span-2">
                      <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Project Information <span class="text-red-500">*</span></label>
                      <LookupPopup 
                        v-model="formData.information_id" 
                        :options="settingsStore.projectLookups.information.filter(x => x.is_active)" 
                        label="Project Information"
                        :disabled="formData.status === 'APPROVED'"
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
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-widest pl-1">Start Date <span class="text-red-500">*</span></label>
                  <DatePickerPopup 
                    v-model="formData.start_date" 
                    label="Start Date"
                    :disabled="formData.status === 'APPROVED'"
                  />
                </div>
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-widest pl-1">End Date <span class="text-red-500">*</span></label>
                  <DatePickerPopup 
                    v-model="formData.end_date" 
                    label="End Date"
                    :minDate="formData.start_date"
                    :disabled="formData.status === 'APPROVED'"
                  />
                </div>
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-widest pl-1">Total Days</label>
                  <div class="premium-input-field flex items-center justify-center text-accent-cyan font-black bg-surface-500/5 shadow-inner">
                    {{ formData.total_days }} Days
                  </div>
                </div>
                <div class="space-y-2 col-span-2">
                  <!-- Empty space for layout balance if needed or just leave as grid item -->
                </div>
              </div>
            </section>
          </div>

          <div v-if="currentTab === 'team'" class="space-y-8 py-4">
             <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-2xl font-bold text-white italic">Assign <span class="text-accent-emerald">Field Officers</span></h3>
                  <p class="text-surface-500 text-sm">Designate the team responsible for this operation.</p>
                </div>
                <button @click="addPIC" class="btn-primary !w-auto !px-6 flex items-center gap-2 bg-accent-emerald/20 text-accent-emerald border border-accent-emerald/30 hover:bg-accent-emerald/30 transition-all font-bold uppercase tracking-widest text-xs">
                  <Plus class="w-4 h-4" /> Add Officer
                </button>
             </div>
             
             <div class="space-y-4">
                <div v-for="(pic, index) in formData.pic_assignments" :key="index" class="p-6 rounded-[24px] border border-white/5 bg-surface-900/40 relative group animate-in slide-in-from-right duration-300" :class="pic.status === 'APPROVED' ? 'opacity-80' : ''">
                  <!-- Status & Remove button -->
                  <div class="absolute -top-3 right-4 flex items-center gap-2">
                    <div v-if="pic.status === 'APPROVED'" class="px-3 py-1 bg-accent-emerald text-white text-[9px] font-black uppercase tracking-widest rounded-full shadow-lg shadow-accent-emerald/20 flex items-center gap-1.5 ring-4 ring-bg-card">
                      <CheckCircle class="w-3 h-3" /> Approved
                    </div>
                    <div v-else class="px-3 py-1 bg-surface-700 text-surface-400 text-[9px] font-black uppercase tracking-widest rounded-full ring-4 ring-bg-card">
                      Draft / Open
                    </div>
                    
                    <button v-if="pic.status === 'OPEN'" @click="removePIC(index)" class="p-1.5 bg-red-500/20 text-red-500 border border-red-500/30 rounded-lg hover:bg-red-500 hover:text-white transition-all opacity-0 group-hover:opacity-100 shadow-xl">
                      <X class="w-3 h-3" />
                    </button>
                  </div>

                  <div class="grid grid-cols-1 xl:grid-cols-12 gap-6 items-end">
                    <!-- User & Role -->
                    <div class="xl:col-span-3 space-y-2">
                      <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">Field Officer <span class="text-red-500">*</span></label>
                      <LookupPopup 
                        v-model="pic.user_id" 
                        :options="users.map(u => ({id: u.user_id, name: u.username}))" 
                        label="Select Officer"
                        :disabled="pic.status === 'APPROVED'"
                      />
                    </div>

                    <!-- Lookups -->
                    <div class="xl:col-span-2 space-y-2">
                       <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">Arrangement <span class="text-red-500">*</span></label>
                       <LookupPopup 
                        v-model="pic.arrangement_id" 
                        :options="settingsStore.projectLookups.arrangements" 
                        label="Arrangement"
                        :disabled="pic.status === 'APPROVED'"
                      />
                    </div>
                    <div class="xl:col-span-2 space-y-2">
                       <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">Assignment <span class="text-red-500">*</span></label>
                       <LookupPopup 
                        v-model="pic.assignment_id" 
                        :options="settingsStore.projectLookups.assignments" 
                        label="Assignment"
                        :disabled="pic.status === 'APPROVED'"
                      />
                    </div>

                    <!-- Dates -->
                    <div class="xl:col-span-2 space-y-2">
                       <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">Start Date <span class="text-red-500">*</span></label>
                       <DatePickerPopup 
                        v-model="pic.start_date" 
                        label="Start Date"
                        :minDate="formData.start_date"
                        :maxDate="formData.end_date"
                        :disabled="pic.status === 'APPROVED'"
                      />
                    </div>
                    <div class="xl:col-span-2 space-y-2">
                       <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">End Date <span class="text-red-500">*</span></label>
                       <DatePickerPopup 
                        v-model="pic.end_date" 
                        label="End Date"
                        :minDate="pic.start_date || formData.start_date"
                        :maxDate="formData.end_date"
                        :disabled="pic.status === 'APPROVED'"
                      />
                    </div>

                    <!-- Actions -->
                    <div class="xl:col-span-1 flex flex-col gap-2">
                      <div class="h-9 premium-input-field flex items-center justify-center text-[11px] font-black text-accent-cyan bg-surface-500/5 shadow-inner">
                        {{ pic.total_days }}D
                      </div>
                      <button 
                        v-if="pic.status === 'OPEN'"
                        @click="() => {
                          if (!pic.user_id || !pic.arrangement_id || !pic.assignment_id || !pic.start_date || !pic.end_date) {
                            error = 'Lengkapi data officer sebelum melakukan Approve.'
                            return
                          }
                          pic.status = 'APPROVED'
                        }"
                        class="h-9 w-full bg-accent-emerald/10 text-accent-emerald text-[9px] font-bold rounded-xl border border-accent-emerald/20 hover:bg-accent-emerald hover:text-white transition-all uppercase tracking-tighter"
                      >
                        Approve
                      </button>
                      <button 
                        v-else
                        @click="pic.status = 'OPEN'"
                        class="h-9 w-full bg-orange-500/10 text-orange-500 text-[9px] font-bold rounded-xl border border-orange-500/20 hover:bg-orange-500 hover:text-white transition-all uppercase tracking-tighter"
                      >
                        Reopen
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Empty State -->
                <div v-if="formData.pic_assignments.length === 0" class="py-12 border border-dashed border-white/5 rounded-[32px] flex flex-col items-center justify-center text-center space-y-4">
                  <div class="w-16 h-16 rounded-3xl bg-surface-500/5 flex items-center justify-center text-secondary ring-1 ring-white/5">
                    <Users class="w-8 h-8 opacity-20" />
                  </div>
                  <div>
                    <p class="text-primary font-bold italic">No officers assigned yet.</p>
                    <p class="text-secondary text-xs">Click "Add Officer" to begin team build-up.</p>
                  </div>
                </div>
             </div>
          </div>

          <!-- Tab 3: Document Tracking -->
          <div v-if="currentTab === 'document'" class="space-y-10 py-4 animate-in fade-in zoom-in duration-300">
            <section class="space-y-8">
              <div class="flex items-center gap-4">
                <div class="h-px flex-1 bg-gradient-to-r from-transparent to-orange-400/20"></div>
                <h3 class="text-[10px] font-black text-orange-400 uppercase tracking-[0.2em]">SLA & Tracking lifecycle</h3>
                <div class="h-px flex-1 bg-gradient-to-l from-transparent to-orange-400/20"></div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <!-- Step 1: Handover -->
                <div class="p-6 rounded-[32px] bg-surface-500/5 border border-white/5 space-y-6">
                  <div class="flex items-center justify-between">
                    <span class="text-[9px] font-black text-secondary uppercase tracking-widest">01. Handover</span>
                    <span class="px-2 py-0.5 rounded-md bg-orange-400/10 text-orange-400 text-[8px] font-bold">Phase 1</span>
                  </div>
                  <div class="space-y-4">
                    <div class="space-y-2">
                      <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">Handover Date (OR)</label>
                      <DatePickerPopup v-model="formData.handover_or" label="Handover Date" />
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                      <div class="space-y-2">
                        <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">Delay Days</label>
                        <div class="h-10 premium-input-field flex items-center justify-center text-xs font-black" :class="formData.handover_days > 0 ? 'text-red-400' : 'text-accent-cyan'">
                          {{ formData.handover_days }} D
                        </div>
                      </div>
                      <div class="space-y-2">
                        <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">PIC KPI 2</label>
                        <input v-model="formData.pic_kpi_2" type="number" class="h-10 premium-input-field" placeholder="0">
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Step 2: Check -->
                <div class="p-6 rounded-[32px] bg-surface-500/5 border border-white/5 space-y-6">
                  <div class="flex items-center justify-between">
                    <span class="text-[9px] font-black text-secondary uppercase tracking-widest">02. Review / Check</span>
                    <span class="px-2 py-0.5 rounded-md bg-orange-400/10 text-orange-400 text-[8px] font-bold">Phase 2</span>
                  </div>
                  <div class="space-y-4">
                    <div class="space-y-2">
                      <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">Check Date (OR)</label>
                      <DatePickerPopup v-model="formData.check_or" label="Check Date" />
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                      <div class="space-y-2">
                        <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">Process Days</label>
                        <div class="h-10 premium-input-field flex items-center justify-center text-xs font-black text-accent-emerald">
                          {{ formData.check_days }} D
                        </div>
                      </div>
                      <div class="space-y-2">
                        <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">Officer KPI 2</label>
                        <input v-model="formData.officer_kpi2" type="number" class="h-10 premium-input-field" placeholder="0">
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Step 3: Validation -->
                <div class="p-6 rounded-[32px] bg-surface-500/5 border border-white/5 space-y-6">
                  <div class="flex items-center justify-between">
                    <span class="text-[9px] font-black text-secondary uppercase tracking-widest">03. Validation</span>
                    <span class="px-2 py-0.5 rounded-md bg-orange-400/10 text-orange-400 text-[8px] font-bold">Phase 3</span>
                  </div>
                  <div class="space-y-4">
                    <div class="space-y-2">
                      <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">Validation Date</label>
                      <DatePickerPopup v-model="formData.validation_date" label="Validation Date" />
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                      <div class="space-y-2">
                        <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">Final Days</label>
                        <div class="h-10 premium-input-field flex items-center justify-center text-xs font-black text-primary">
                          {{ formData.validation_days }} D
                        </div>
                      </div>
                      <div class="space-y-2">
                        <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">OKR KPI 2</label>
                        <input v-model="formData.okr_kpi2" type="number" class="h-10 premium-input-field" placeholder="0">
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>

          <!-- Tab 4: Automation Reminders -->
          <div v-if="currentTab === 'automation'" class="space-y-10 py-4 animate-in fade-in zoom-in duration-300">
            <section class="space-y-8">
              <div class="flex items-center gap-4">
                <div class="h-px flex-1 bg-gradient-to-r from-transparent to-accent-amber/20"></div>
                <h3 class="text-[10px] font-black text-accent-amber uppercase tracking-[0.2em]">Automated notification tracking</h3>
                <div class="h-px flex-1 bg-gradient-to-l from-transparent to-accent-amber/20"></div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <!-- S1: Estimation -->
                <div class="p-6 rounded-[32px] bg-surface-500/5 border border-white/5 space-y-6">
                  <div class="flex items-center justify-between">
                    <span class="text-[9px] font-black text-secondary uppercase tracking-widest">S1. Stage Estimation</span>
                    <span class="px-2 py-0.5 rounded-md bg-accent-amber/10 text-accent-amber text-[8px] font-bold">Automation</span>
                  </div>
                  <div class="grid grid-cols-2 gap-4">
                    <div class="space-y-2">
                      <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">S1 Estimation</label>
                      <DatePickerPopup v-model="formData.s1_estimation" label="S1 Estimation" />
                    </div>
                    <div class="space-y-2">
                      <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">Over Days</label>
                      <div class="h-10 premium-input-field flex items-center justify-center text-xs font-black" :class="formData.s1_over_days > 0 ? 'text-red-400' : 'text-accent-cyan'">
                        {{ formData.s1_over_days }} D
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Email Sent Tracking -->
                <div class="p-6 rounded-[32px] bg-surface-500/5 border border-white/5 space-y-6">
                  <div class="flex items-center justify-between">
                    <span class="text-[9px] font-black text-secondary uppercase tracking-widest">Notification History</span>
                    <span class="px-2 py-0.5 rounded-md bg-accent-amber/10 text-accent-amber text-[8px] font-bold">Log Tracking</span>
                  </div>
                  <div class="grid grid-cols-1 gap-4">
                    <div class="space-y-2">
                      <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">S1 Email Sent Count</label>
                      <input v-model="formData.s1_count_email_sent" type="text" class="h-10 premium-input-field" placeholder="Ex: 1 time, 2 times...">
                    </div>
                  </div>
                </div>

                <div class="p-6 rounded-[32px] bg-surface-500/5 border border-white/5 space-y-4 md:col-span-2">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="space-y-2">
                      <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">S2 Email Sent Log</label>
                      <input v-model="formData.s2_email_sent" type="text" class="h-10 premium-input-field" placeholder="Status email S2...">
                    </div>
                    <div class="space-y-2">
                      <label class="text-[9px] font-black text-secondary uppercase tracking-widest pl-1">S3 Email Sent Log</label>
                      <input v-model="formData.s3_email_sent" type="text" class="h-10 premium-input-field" placeholder="Status email S3...">
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>

        <!-- Footer Action Bar (RIGHT ALIGNED) -->
        <div class="p-8 border-t border-border-app bg-surface-500/5 flex flex-row gap-4 items-center justify-end">
          <!-- Training List (LEFT ALIGNED) -->
          <div class="flex-1 flex justify-start">
            <button 
              v-if="props.project"
              @click="showTrainingManager = true"
              class="h-14 px-8 rounded-2xl bg-white/5 border border-white/5 hover:bg-white/10 text-primary transition-all font-bold text-xs uppercase tracking-widest flex items-center gap-3 group"
            >
              <QrCode class="w-5 h-5 text-accent-cyan group-hover:scale-110 transition-transform" />
              Training List
            </button>
          </div>

          <!-- Status Toggle -->
          <button 
            v-if="props.project"
            @click="formData.status = formData.status === 'OPEN' ? 'APPROVED' : 'OPEN'"
            class="h-14 px-6 rounded-2xl border flex items-center gap-2 transition-all font-bold text-xs uppercase tracking-widest"
            :class="formData.status === 'OPEN' ? 'bg-accent-emerald/10 text-accent-emerald border-accent-emerald/20' : 'bg-orange-500/10 text-orange-500 border-orange-500/20'"
          >
            <CheckCircle v-if="formData.status === 'OPEN'" class="w-4 h-4" />
            <RefreshCw v-else class="w-4 h-4" />
            {{ formData.status === 'OPEN' ? 'Approve Project' : 'Reopen Project' }}
          </button>

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

    <!-- Training Manager Modal -->
    <TrainingManagerModal 
      v-if="showTrainingManager"
      :projectId="props.project?.project_id"
      :projectName="formData.name"
      @close="showTrainingManager = false"
    />
  </Teleport>
</template>

