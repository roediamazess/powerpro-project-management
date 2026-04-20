<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useComplianceStore } from '../store/compliance'
import { usePartnerStore } from '../store/partner'
import { useProjectStore } from '../store/project'
import { useUIStore } from '../store/ui'
import LookupPopup from '../components/LookupPopup.vue'
import { 
  ChevronLeft, Save, ShieldCheck, 
  AlertCircle, Camera, MessageSquare, History, 
  Loader2 
} from 'lucide-vue-next'

const complianceStore = useComplianceStore()
const partnerStore = usePartnerStore()
const projectStore = useProjectStore()
const uiStore = useUIStore()
const router = useRouter()

const selectedFormId = ref('')
const selectedPartnerId = ref('')
const selectedProjectId = ref('')
const selectedBaselineId = ref('')
const auditScores = ref<any[]>([])

// Mock Upload State
const isUploading = ref<Record<string, boolean>>({})
const mockUpload = (itemId: string) => {
  isUploading.value[itemId] = true
  setTimeout(() => {
    isUploading.value[itemId] = false
    uiStore.showToast('Photo uploaded and verified successfully', 'success')
  }, 1500)
}

const selectedForm = computed(() => {
  return complianceStore.forms.find(f => f.form_id === selectedFormId.value)
})

const filteredEntries = computed(() => {
  return complianceStore.entries.filter((e: any) => e.partner_id === selectedPartnerId.value)
})

onMounted(async () => {
  await complianceStore.fetchForms()
  await complianceStore.fetchEntries()
  await partnerStore.fetchPartners()
  await projectStore.fetchProjects()
})

const initializeAudit = () => {
  if (!selectedForm.value) return
  auditScores.value = selectedForm.value.items.map((item: any) => ({
    item_id: item.item_id,
    name: item.name,
    weight: item.weight || 1,
    score: 5,
    remark: ''
  }))
}

const isSubmitting = ref(false)
const handleSubmit = async () => {
  if (!selectedFormId.value || !selectedPartnerId.value) return
  
  isSubmitting.value = true
  try {
    const payload = {
      form_id: selectedFormId.value,
      partner_id: selectedPartnerId.value,
      project_id: selectedProjectId.value || null,
      baseline_id: selectedBaselineId.value || null,
      scores: auditScores.value.map((s: any) => ({
        item_id: s.item_id,
        score: s.score,
        remark: s.remark
      })),
      status: 'SUBMITTED' // Final on submit
    }
    await complianceStore.submitEntry(payload)
    uiStore.showToast('Audit report submitted successfully!', 'success')
    router.push({ name: 'compliance' })
  } catch (err) {
    uiStore.showToast('Failed to sync. Please check connection.', 'error')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-8" v-auto-animate>
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <button @click="router.back()" class="p-2 glass rounded-lg text-surface-400 hover:text-white transition-all">
          <ChevronLeft class="w-6 h-6" />
        </button>
        <div>
          <h1 class="text-2xl font-bold text-white tracking-tight italic text-accent-emerald">Field Audit <span class="text-white">v2.1</span></h1>
          <p class="text-surface-400 text-sm italic">Standardized Weighted Inspection Protocol.</p>
        </div>
      </div>
      <button 
        @click="handleSubmit" 
        :disabled="isSubmitting || !selectedFormId || auditScores.length === 0"
        class="btn-primary flex items-center gap-2 bg-gradient-to-r from-accent-emerald to-emerald-600 border-none shadow-lg shadow-accent-emerald/20"
      >
        <Save class="w-5 h-5" />
        {{ isSubmitting ? 'Syncing...' : 'Finalize Audit' }}
      </button>
    </div>

    <!-- Configuration Card (Extended for Baselines) -->
    <div class="glass-card grid grid-cols-4 gap-4">
      <div class="space-y-2">
        <label class="text-[10px] font-black text-surface-500 uppercase tracking-widest">Inspection Type</label>
        <LookupPopup 
          v-model="selectedFormId" 
          :options="complianceStore.forms.map(f => ({id: f.form_id, name: f.name}))" 
          label="Inspection Type"
          @update:modelValue="initializeAudit"
        />
      </div>
      <div class="space-y-2">
        <label class="text-[10px] font-black text-surface-500 uppercase tracking-widest">Client Partner</label>
        <LookupPopup 
          v-model="selectedPartnerId" 
          :options="partnerStore.partners.map(p => ({id: p.partner_id, name: p.name}))" 
          label="Client Partner"
        />
      </div>
       <div class="space-y-2">
        <label class="text-[10px] font-black text-surface-500 uppercase tracking-widest">Linked Project</label>
        <LookupPopup 
          v-model="selectedProjectId" 
          :options="[{id: '', name: 'No Project'}, ...projectStore.projects.map(pj => ({id: pj.project_id, name: pj.name}))]" 
          label="Linked Project"
        />
      </div>
      <div class="space-y-2">
        <label class="text-[10px] font-black text-accent-emerald uppercase tracking-widest flex items-center gap-1">
          <History class="w-3 h-3" /> Reference Baseline
        </label>
        <LookupPopup 
          v-model="selectedBaselineId" 
          :options="[{id: '', name: 'New Audit (No Baseline)'}, ...filteredEntries.map(e => ({id: e.entry_id, name: `Baseline: ${e.form.name} (${e.compliance_percent.toFixed(0)}%)`}))]" 
          label="Reference Baseline"
        />
      </div>
    </div>

    <!-- Audit Items with Weighting -->
    <div v-if="auditScores.length > 0" class="space-y-4">
      <div v-for="(item, index) in auditScores" :key="item.item_id" class="glass-card group hover:border-accent-emerald/30 transition-all border-l-4" :class="item.weight > 1 ? 'border-l-accent-cyan' : 'border-l-surface-800'">
        <div class="flex items-start gap-6">
          <div class="w-8 h-8 rounded-full bg-surface-800 flex items-center justify-center text-xs font-bold text-accent-emerald border border-white/5 shadow-inner">
            {{ index + 1 }}
          </div>
          
          <div class="flex-1 space-y-4">
            <div class="flex items-center justify-between">
               <h3 class="font-bold text-lg text-white group-hover:text-accent-emerald transition-colors">{{ item.name }}</h3>
               <div v-if="item.weight > 1" class="flex items-center gap-2 px-3 py-1 bg-accent-cyan/10 border border-accent-cyan/20 rounded-full">
                 <ShieldCheck class="w-3 h-3 text-accent-cyan" />
                 <span class="text-[10px] font-black text-accent-cyan uppercase tracking-tighter">Impact Level: {{ item.weight }} (Scale 1-5)</span>
               </div>
            </div>
            
            <div class="flex items-center gap-8">
               <div class="flex flex-col gap-2">
                 <label class="text-[10px] font-black text-surface-500 uppercase tracking-widest mb-1">Pass / Compliance Score</label>
                 <div class="flex items-center gap-1 p-1 bg-surface-950/50 rounded-xl w-fit ring-1 ring-white/5">
                    <button 
                      v-for="s in 6" :key="s-1"
                      @click="item.score = s-1"
                      class="w-10 h-10 rounded-lg text-sm font-black transition-all"
                      :class="item.score === (s-1) ? 'bg-accent-emerald text-surface-950 shadow-lg shadow-accent-emerald/20' : 'text-surface-500 hover:text-white'"
                    >
                      {{ s-1 }}
                    </button>
                 </div>
               </div>

               <div class="flex-1 space-y-2">
                 <label class="text-[10px] font-black text-surface-500 uppercase tracking-widest flex items-center gap-2">
                   <MessageSquare class="w-3 h-3" /> Field Remarks
                 </label>
                 <input v-model="item.remark" type="text" placeholder="Add optional finding description..." class="w-full bg-transparent border-b border-surface-800 focus:border-accent-emerald outline-none py-2 text-sm text-surface-300">
               </div>

               <button 
                 @click="mockUpload(item.item_id)"
                 class="p-4 glass rounded-2xl text-surface-600 hover:text-accent-cyan transition-all mt-4 relative overflow-hidden"
                 :disabled="isUploading[item.item_id]"
               >
                 <Loader2 v-if="isUploading[item.item_id]" class="w-5 h-5 animate-spin text-accent-cyan" />
                 <Camera v-else class="w-5 h-5" />
                 <div v-if="isUploading[item.item_id]" class="absolute bottom-0 left-0 h-1 bg-accent-cyan animate-pulse w-full"></div>
               </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="py-20 text-center glass-card border-dashed bg-white/[0.01]">
      <AlertCircle class="w-12 h-12 text-surface-600 mx-auto mb-4" />
      <h3 class="text-xl font-bold text-surface-500 italic">Select inspection configuration above</h3>
      <p class="text-surface-600 text-sm mt-1">Audit protocols and weighted items will load dynamically.</p>
    </div>
  </div>
</template>

<style scoped>
.glass-card:hover ::-webkit-scrollbar-thumb {
  background: rgba(16, 185, 129, 0.2);
}
</style>
