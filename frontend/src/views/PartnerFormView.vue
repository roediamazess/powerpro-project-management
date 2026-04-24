<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { X, Save, UserPlus, Hotel, Plus, Trash2, History, RefreshCw } from 'lucide-vue-next'
import { usePartnerStore } from '../store/partner'
import { useSettingsStore } from '../store/settings'
import LookupPopup from '../components/LookupPopup.vue'
import DatePickerPopup from '../components/DatePickerPopup.vue'

const props = defineProps<{
  partner?: any
}>()

const emit = defineEmits(['close', 'success'])
const partnerStore = usePartnerStore()
const settingsStore = useSettingsStore()

const formData = ref({
  name: '',
  partner_cnc: '',
  type_id: 'HOTEL',
  status_id: 'ACTIVE',
  group_id: '',
  area_id: '',
  sub_area_id: '',
  version_id: '',
  imp_type_id: '',
  server_information_id: '',
  server_information_detail: '',
  stars: 0,
  rooms: 0,
  outlets: 0,
  address: '',
  system_live_at: null,
  last_visit_at: null,
  last_visit_type: '',
  last_project: null,
  last_project_type: '',
  contacts: [] as any[]
})

const currentTab = ref('general')

const lastVisitTypeName = computed(() => {
  const typeId = formData.value.last_visit_type
  if (!typeId) return ''
  const type = settingsStore.projectLookups.types.find(t => t.id === typeId || t.type_id === typeId)
  return type ? type.name : typeId
})

const lastProjectTypeName = computed(() => {
  const typeId = formData.value.last_project_type
  if (!typeId) return ''
  const type = settingsStore.projectLookups.types.find(t => t.id === typeId || t.type_id === typeId)
  return type ? type.name : typeId
})

onMounted(async () => {
  await partnerStore.fetchLookups()
  await settingsStore.fetchProjectLookups()
  if (props.partner) {
    formData.value = { ...props.partner }
  }
})

const isSubmitting = ref(false)

const error = ref('')

const addContact = () => {
  formData.value.contacts.push({
    name: '',
    position: '',
    email: '',
    phone: '',
    is_primary: false
  })
}

const removeContact = (index: number) => {
  formData.value.contacts.splice(index, 1)
}

const handleSubmit = async () => {
  isSubmitting.value = true
  error.value = ''
  
  // Client-side Mandatory Check
  const mandatoryFields = []
  if (!formData.value.name || formData.value.name.trim() === '') mandatoryFields.push('Partner Name')
  if (!formData.value.partner_cnc || formData.value.partner_cnc.trim() === '') mandatoryFields.push('CNC ID')
  if (!formData.value.type_id) mandatoryFields.push('Partner Type')
  if (!formData.value.status_id) mandatoryFields.push('Status')
  if (!formData.value.area_id) mandatoryFields.push('Area')
  if (!formData.value.sub_area_id) mandatoryFields.push('SubArea')
  if (!formData.value.address || formData.value.address.trim() === '') mandatoryFields.push('Address')
  if (!formData.value.version_id) mandatoryFields.push('System Version')

  if (mandatoryFields.length > 0) {
    error.value = `MANDATORY FIELD MISSING: ${mandatoryFields.join(', ')} must be provided.`
    isSubmitting.value = false
    return
  }

  // Clean data: convert empty strings to null for optional fields
  const payload = { ...formData.value }
  Object.keys(payload).forEach(key => {
    if (typeof (payload as any)[key] === 'string' && (payload as any)[key].trim() === '') {
      (payload as any)[key] = null
    }
  })

  try {
    if (props.partner?.partner_id) {
      await partnerStore.updatePartner(props.partner.partner_id, payload)
    } else {
      await partnerStore.createPartner(payload)
    }
    emit('success')
  } catch (err: any) {
    const detail = err.response?.data?.detail
    if (Array.isArray(detail)) {
      // Map field names to friendly labels
      const fieldMap: Record<string, string> = {
        'name': 'Partner Legal Name',
        'type_id': 'Business Category',
        'status_id': 'Operational Status',
        'area_id': 'Operational Area',
        'sub_area_id': 'Sub-Area / Region'
      }

      error.value = detail.map(d => {
        const fieldKey = d.loc[d.loc.length - 1]
        const fieldName = fieldMap[fieldKey] || fieldKey.toUpperCase()
        return `${fieldName}: ${d.msg}`
      }).join(' | ')
    } else if (typeof detail === 'string') {
      error.value = detail
    } else {
      const serverMessage = err.response?.data?.message || err.response?.data?.error || err.message
      error.value = `TECHNICAL ERROR: ${serverMessage || 'Unknown error occurs during save.'}. Please check system logs.`
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-[80] flex items-center justify-center p-4 sm:p-6 overflow-hidden">
      <!-- Backdrop with advanced blur -->
      <div class="absolute inset-0 bg-surface-950/40 backdrop-blur-md" @click="emit('close')"></div>

      <!-- Centered Modal Panel -->
      <div v-auto-animate 
        class="relative w-full max-w-4xl max-h-[90vh] border border-white/10 shadow-2xl flex flex-col rounded-[32px] overflow-hidden animate-in fade-in zoom-in duration-300"
        :style="{ backgroundColor: 'var(--bg-app)' }"
      >
        <!-- Header -->
        <div class="p-8 border-b border-border-app flex flex-col gap-6" :style="{ backgroundColor: 'var(--bg-card)' }">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 rounded-2xl bg-accent-emerald/10 border border-accent-emerald/20 flex items-center justify-center text-accent-emerald shadow-lg">
                <Hotel class="w-7 h-7" />
              </div>
              <div>
                <h2 class="text-2xl font-bold text-primary tracking-tight">
                  {{ props.partner ? 'Partner Identity Profile' : 'Initialize New Partner' }}
                </h2>
                <p class="text-[10px] text-secondary font-black tracking-widest uppercase mt-1">Operational Module v2.1</p>
              </div>
            </div>
            <button @click="emit('close')" class="p-2 hover:bg-surface-500/10 dark:hover:bg-surface-700 rounded-xl text-secondary transition-all hover:rotate-90">
              <X class="w-6 h-6" />
            </button>
          </div>

          <!-- Tab Navigation -->
          <div class="flex gap-2 p-1.5 bg-surface-200/50 dark:bg-surface-950/50 rounded-2xl w-fit border border-border-app">
            <button 
              @click="currentTab = 'general'"
              class="px-6 py-2.5 text-sm font-bold rounded-xl transition-all flex items-center gap-2"
              :class="currentTab === 'general' ? 'bg-accent-emerald/10 text-accent-emerald ring-1 ring-accent-emerald/20 shadow-lg' : 'text-secondary hover:text-primary'"
            >
              <Hotel class="w-4 h-4" />
              General Details
            </button>
            <button 
              @click="currentTab = 'contacts'"
              class="px-6 py-2.5 text-sm font-bold rounded-xl transition-all flex items-center gap-2"
              :class="currentTab === 'contacts' ? 'bg-accent-cyan/10 text-accent-cyan ring-1 ring-accent-cyan/20 shadow-lg' : 'text-secondary hover:text-primary'"
            >
              <UserPlus class="w-4 h-4" />
              Management & PIC
            </button>
            <button 
              @click="currentTab = 'history'"
              class="px-6 py-2.5 text-sm font-bold rounded-xl transition-all flex items-center gap-2"
              :class="currentTab === 'history' ? 'bg-accent-amber/10 text-accent-amber ring-1 ring-accent-amber/20 shadow-lg' : 'text-secondary hover:text-primary'"
            >
              <History class="w-4 h-4" />
              Project History
            </button>
          </div>
        </div>

        <!-- Scrollable Content Interface -->
        <div v-auto-animate class="flex-1 overflow-y-auto p-8 custom-scrollbar" :style="{ backgroundColor: 'var(--bg-app)' }">
          <!-- Enhanced Error Alert -->
          <div v-if="error" class="bg-red-500/10 border border-red-500/20 p-6 rounded-[24px] mb-8 animate-in fade-in slide-in-from-top-4 duration-300">
            <div class="flex items-start gap-4">
              <div class="p-2 bg-red-500/20 rounded-xl text-red-400">
                <X class="w-5 h-5" />
              </div>
              <div class="flex-1">
                <h4 class="text-xs font-black text-red-400 uppercase tracking-widest mb-1">Validation Error</h4>
                <p class="text-sm text-red-200/80 font-medium leading-relaxed">{{ error }}</p>
              </div>
              <button @click="error = ''" class="text-red-400/50 hover:text-red-400 transition-colors">
                <X class="w-4 h-4" />
              </button>
            </div>
          </div>

          <!-- Tab 1: General Details -->
          <div v-if="currentTab === 'general'" class="space-y-10">
            <!-- 1. Primary Classification -->
            <section class="space-y-6">
              <div class="flex items-center gap-3">
                <div class="h-px flex-1 bg-gradient-to-r from-transparent to-border-app"></div>
                <h3 class="text-[10px] font-black text-secondary uppercase tracking-[0.3em]">Identity & Classification</h3>
                <div class="h-px flex-1 bg-gradient-to-l from-transparent to-border-app"></div>
              </div>
              
              <div class="grid grid-cols-12 gap-6">
                <div class="col-span-12 md:col-span-8 space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Partner Legal Name</label>
                  <input v-model="formData.name" type="text" class="premium-input-field" placeholder="Identifikasi Nama Lengkap Partner...">
                </div>
                <div class="col-span-12 md:col-span-4 space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">CNC System ID</label>
                  <input v-model="formData.partner_cnc" type="text" class="premium-input-field" placeholder="H-000">
                </div>

                <div class="col-span-12 md:col-span-4 space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Business Category</label>
                  <LookupPopup 
                    v-model="formData.type_id" 
                    :options="partnerStore.lookups.types" 
                    label="Business Category"
                  />
                </div>
                <div class="col-span-12 md:col-span-4 space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Operational Status</label>
                  <LookupPopup 
                    v-model="formData.status_id" 
                    :options="partnerStore.lookups.statuses" 
                    label="Operational Status"
                  />
                </div>
                <div class="col-span-12 md:col-span-4 space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Corporate Group</label>
                  <LookupPopup 
                    v-model="formData.group_id" 
                    :options="[{id: '', name: 'None / Independent'}, ...partnerStore.lookups.groups]" 
                    label="Corporate Group"
                  />
                </div>
              </div>
            </section>

            <!-- 2. Geographical Location -->
            <section class="space-y-6">
              <div class="flex items-center gap-3">
                <div class="h-px flex-1 bg-gradient-to-r from-transparent to-border-app"></div>
                <h3 class="text-[10px] font-black text-secondary uppercase tracking-[0.3em]">Geographical Mapping</h3>
                <div class="h-px flex-1 bg-gradient-to-l from-transparent to-border-app"></div>
              </div>

              <div class="grid grid-cols-2 gap-6">
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-wider">Operational Area</label>
                  <LookupPopup 
                    v-model="formData.area_id" 
                    :options="partnerStore.lookups.areas" 
                    label="Operational Area"
                  />
                </div>
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-wider">Sub-Area / Region</label>
                  <LookupPopup 
                    v-model="formData.sub_area_id" 
                    :options="partnerStore.lookups.sub_areas.filter(x => x.area_id === formData.area_id)" 
                    label="Sub-Area / Region"
                    :disabled="!formData.area_id"
                  />
                </div>
                <div class="col-span-2 space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-wider">Address Specification</label>
                  <textarea v-model="formData.address" rows="2" class="premium-input-field" placeholder="Complete address detail..."></textarea>
                </div>
              </div>
            </section>

            <!-- 3. Operational Performance -->
            <section class="space-y-6">
              <div class="flex items-center gap-3">
                <div class="h-px flex-1 bg-gradient-to-r from-transparent to-border-app"></div>
                <h3 class="text-[10px] font-black text-secondary uppercase tracking-[0.3em]">Operational Metrics</h3>
                <div class="h-px flex-1 bg-gradient-to-l from-transparent to-border-app"></div>
              </div>

              <div class="grid grid-cols-3 gap-6">
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-wider">Total Inventory Units</label>
                  <input v-model.number="formData.rooms" type="number" class="premium-input-field" placeholder="0">
                </div>
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-wider">F&B Outlets</label>
                  <input v-model.number="formData.outlets" type="number" class="premium-input-field" placeholder="0">
                </div>
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-wider">Star Rating (1-5)</label>
                  <input v-model.number="formData.stars" type="number" max="5" class="premium-input-field" placeholder="0">
                </div>
              </div>
            </section>

            <!-- 4. System & Lifecycle -->
            <section class="space-y-6">
              <div class="flex items-center gap-3">
                <div class="h-px flex-1 bg-gradient-to-r from-transparent to-surface-800"></div>
                <h3 class="text-[10px] font-black text-surface-500 uppercase tracking-[0.3em]">System Intelligence</h3>
                <div class="h-px flex-1 bg-gradient-to-l from-transparent to-surface-800"></div>
              </div>

              <div class="grid grid-cols-2 gap-6">
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-wider">Core System Version</label>
                  <LookupPopup 
                    v-model="formData.version_id" 
                    :options="partnerStore.lookups.versions" 
                    label="Core System Version"
                  />
                </div>
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-wider">Implementation Protocol</label>
                  <LookupPopup 
                    v-model="formData.imp_type_id" 
                    :options="partnerStore.lookups.imp_types" 
                    label="Implementation Protocol"
                  />
                </div>
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-wider">Server Information</label>
                  <LookupPopup 
                    v-model="formData.server_information_id" 
                    :options="partnerStore.lookups.server_info" 
                    label="Server Information"
                  />
                </div>
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-wider">Server Detail</label>
                  <input v-model="formData.server_information_detail" type="text" class="premium-input-field" placeholder="Server detail manual input...">
                </div>
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-wider">System Live Date</label>
                  <DatePickerPopup 
                    v-model="formData.system_live_at" 
                    label="System Live Date"
                  />
                </div>
              </div>
            </section>
          </div>

          <!-- Tab 2: Contacts Management -->
          <div v-if="currentTab === 'contacts'" class="space-y-8">
            <div class="flex items-center justify-between bg-surface-950/20 p-4 rounded-2xl border border-white/5">
              <div>
                <h3 class="text-sm font-bold text-white uppercase tracking-wider">Executive Contacts</h3>
                <p class="text-xs text-surface-500 mt-1">Management and PIC directory for this operational partner.</p>
              </div>
              <button @click="addContact" class="px-4 py-2 rounded-xl bg-accent-cyan/10 text-accent-cyan text-xs font-bold hover:bg-accent-cyan/20 border border-accent-cyan/20 transition-all flex items-center gap-2">
                <Plus class="w-4 h-4" /> Add Executive Contact
              </button>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div v-for="(contact, idx) in formData.contacts" :key="idx" class="glass relative border border-white/5 p-6 rounded-3xl space-y-4 group hover:border-accent-cyan/30 transition-all">
                <button @click="removeContact(idx)" class="absolute top-4 right-4 text-surface-600 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity">
                  <Trash2 class="w-4 h-4" />
                </button>
                
                <div class="space-y-4">
                  <div class="space-y-2">
                    <label class="text-[10px] font-black text-surface-500 uppercase tracking-widest">PIC Identity</label>
                    <input v-model="contact.name" type="text" class="premium-input-field text-sm py-2.5" placeholder="Full name">
                  </div>
                  <div class="grid grid-cols-2 gap-4">
                    <div class="space-y-1">
                      <label class="text-[10px] font-medium text-surface-500">Corporate Position</label>
                      <input v-model="contact.position" type="text" class="premium-input-field text-xs py-2" placeholder="e.g. GM, IT">
                    </div>
                    <div class="space-y-1">
                      <label class="text-[10px] font-medium text-surface-500">Communication</label>
                      <input v-model="contact.phone" type="text" class="premium-input-field text-xs py-2" placeholder="Phone">
                    </div>
                  </div>
                  <div class="space-y-1">
                    <label class="text-[10px] font-medium text-surface-500">Professional Email</label>
                    <input v-model="contact.email" type="email" class="premium-input-field text-xs py-2" placeholder="email@address.com">
                  </div>
                </div>
              </div>
            </div>

            <div v-if="formData.contacts.length === 0" class="text-center py-20 bg-surface-950/20 border-2 border-dashed border-surface-800 rounded-[32px]">
              <div class="w-16 h-16 rounded-full bg-surface-900 flex items-center justify-center mx-auto mb-4 border border-white/5">
                <UserPlus class="w-8 h-8 text-surface-700" />
              </div>
              <h4 class="text-white font-bold mb-1">Directory Empty</h4>
              <p class="text-surface-500 text-xs max-w-xs mx-auto">No executive contacts have been assigned to this partner protocol yet.</p>
            </div>
          </div>

          <!-- Tab 3: Project History -->
          <div v-if="currentTab === 'history'" class="space-y-10">
            <section class="space-y-6">
              <div class="flex items-center gap-3">
                <div class="h-px flex-1 bg-gradient-to-r from-transparent to-surface-800"></div>
                <h3 class="text-[10px] font-black text-surface-500 uppercase tracking-[0.3em]">Historical Audit & Progress</h3>
                <div class="h-px flex-1 bg-gradient-to-l from-transparent to-surface-800"></div>
              </div>

              <div class="grid grid-cols-2 gap-6">
                <div class="space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Date of Last Visit</label>
                  <DatePickerPopup 
                    v-model="formData.last_visit_at" 
                    label="Date of Last Visit"
                    placeholder="Last visit date..."
                  />
                </div>
                <div class="space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Type of Last Visit</label>
                  <input 
                    :value="lastVisitTypeName" 
                    type="text" 
                    class="premium-input-field opacity-60 cursor-not-allowed bg-surface-500/10 font-bold" 
                    placeholder="Automated from project..."
                    readonly
                    disabled
                  >
                </div>
                <div class="space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Date of Last Project</label>
                  <DatePickerPopup 
                    v-model="formData.last_project" 
                    label="Date of Last Project"
                    disabled
                    placeholder="No project data..."
                  />
                </div>
                <div class="space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Type of Last Project</label>
                  <input 
                    :value="lastProjectTypeName" 
                    type="text" 
                    class="premium-input-field opacity-60 cursor-not-allowed bg-surface-500/10 font-bold" 
                    placeholder="Automated from project..."
                    readonly
                    disabled
                  >
                </div>
              </div>
            </section>
          </div>
        </div>

        <!-- Combined Footer Action Bar (RIGHT ALIGNED) -->
        <div class="p-8 border-t border-border-app flex flex-row gap-4 items-center justify-end" :style="{ backgroundColor: 'var(--bg-card)' }">
          <!-- Initialize/Save -->
          <button @click="handleSubmit" :disabled="isSubmitting" class="w-auto px-12 h-14 btn-primary bg-gradient-to-r from-accent-emerald to-accent-cyan shadow-xl shadow-accent-emerald/20 flex items-center justify-center gap-3 active:scale-95 transition-all">
            <Save v-if="!isSubmitting" class="w-5 h-5" />
            <RefreshCw v-else class="w-5 h-5 animate-spin" />
            <span class="text-sm font-bold uppercase tracking-widest">
              {{ props.partner ? 'Save' : 'Create' }}
            </span>
          </button>

          <!-- Cancel/Close -->
          <button @click="emit('close')" class="w-auto px-12 h-14 glass text-primary text-sm font-bold rounded-2xl hover:bg-surface-500/5 border border-border-app transition-all uppercase tracking-widest">
            Cancel
          </button>
        </div>

      </div>
    </div>
  </Teleport>
</template>

<style scoped>
@reference "tailwindcss";

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  @apply bg-transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  @apply bg-white/5 rounded-full hover:bg-white/10 transition-all;
}
</style>
