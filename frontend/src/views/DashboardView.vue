<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { 
  TrendingUp, Clock, AlertCircle, 
  MapPin, Calendar, ExternalLink,
  ChevronRight, ArrowRight
} from 'lucide-vue-next'
import { usePartnerStore } from '../store/partner'
import { useSettingsStore } from '../store/settings'
import PartnerFormView from './PartnerFormView.vue'

const partnerStore = usePartnerStore()
const settingsStore = useSettingsStore()

const isFormOpen = ref(false)
const selectedPartner = ref<any>(null)

onMounted(async () => {
  await Promise.all([
    partnerStore.fetchPartners(),
    partnerStore.fetchLookups(),
    settingsStore.fetchProjectLookups()
  ])
})

// Categories
const VISIT_TYPES = ['IMPLEMENTATION', 'UPGRADE', 'MAINTENANCE', 'RE-TRAINING', 'IH-TRAINING', 'SPEC-REQ']
const PROJECT_TYPES = ['REMOTE-INS', 'OL-TRAINING', 'OTH']

// Color Coding Logic
const getStatusClasses = (dateString: string | undefined) => {
  if (!dateString) return 'bg-surface-500/10 text-surface-500 border-surface-500/20'
  
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - date.getTime())
  const diffYears = diffTime / (1000 * 60 * 60 * 24 * 365)

  if (diffYears > 2) return 'bg-red-500/10 text-red-400 border-red-500/20'
  if (diffYears > 1) return 'bg-amber-500/10 text-amber-400 border-amber-500/20'
  return 'bg-accent-emerald/10 text-accent-emerald border-accent-emerald/20'
}

const formatDate = (dateString: string | undefined) => {
  if (!dateString) return 'No data'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-GB', {
    day: '2-digit',
    month: 'short',
    year: '2-digit'
  }).format(date)
}

const getTypeName = (typeId: string | undefined) => {
  if (!typeId) return '-'
  const type = settingsStore.projectLookups.types.find(t => t.id === typeId || t.type_id === typeId)
  return type ? type.name : typeId
}

// Grouping & Sorting Logic
const processGroupedList = (type: 'visit' | 'project') => {
  const data = partnerStore.partners.map(p => {
    const date = type === 'visit' ? p.last_visit_at : p.last_project
    const typeId = type === 'visit' ? p.last_visit_type : p.last_project_type
    const area = partnerStore.lookups.areas.find(a => a.area_id === p.area_id)?.name || 'Unassigned'
    
    return {
      id: p.partner_id,
      original: p,
      name: p.name,
      date,
      typeId,
      area,
      statusClass: getStatusClasses(date)
    }
  })

  // Sort by date (oldest first)
  data.sort((a, b) => {
    if (!a.date) return -1
    if (!b.date) return 1
    return new Date(a.date).getTime() - new Date(b.date).getTime()
  })

  // Group by Area
  const groups: Record<string, any[]> = {}
  data.forEach(item => {
    const groupName = item.area === 'Unassigned' ? '' : item.area
    if (!groups[groupName]) groups[groupName] = []
    groups[groupName].push(item)
  })

  // Order groups: empty header (Unassigned) first, then alphabetical
  return Object.entries(groups)
    .sort(([a], [b]) => {
      if (a === '') return -1
      if (b === '') return 1
      return a.localeCompare(b)
    })
    .map(([name, partners]) => ({ name, partners }))
}

const visitGroups = computed(() => processGroupedList('visit'))
const projectGroups = computed(() => processGroupedList('project'))

// Modal Handlers
const openPartnerEdit = (partner: any) => {
  selectedPartner.value = partner.original
  isFormOpen.value = true
}

const handleFormSuccess = () => {
  isFormOpen.value = false
  partnerStore.fetchPartners()
}

// Stats
const stats = computed(() => [
  { 
    name: 'Critical Visit', 
    value: partnerStore.partners.filter(p => {
      if (!p.last_visit_at) return true
      return (new Date().getTime() - new Date(p.last_visit_at).getTime()) / (1000 * 60 * 60 * 24 * 365) > 2
    }).length, 
    icon: AlertCircle, 
    color: 'text-red-400' 
  },
  { 
    name: 'Total Partners', 
    value: partnerStore.partners.length, 
    icon: TrendingUp, 
    color: 'text-accent-cyan' 
  },
  { 
    name: 'Active Areas', 
    value: partnerStore.lookups.areas.length, 
    icon: MapPin, 
    color: 'text-accent-emerald' 
  },
])
</script>

<template>
  <div class="h-full flex flex-col space-y-6 pb-2 overflow-hidden">
    <!-- Header Page (Flex None) -->
    <div class="flex-none flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-white tracking-tight italic">Dashboard <span class="text-accent-cyan">Insights</span></h1>
        <p class="text-surface-400 mt-1">Analisa Kunjungan & Proyek Partner <span class="text-accent-emerald">PowerPro Management</span></p>
      </div>
      <div class="flex items-center gap-3">
        <div class="px-4 py-2 rounded-xl bg-surface-500/5 border border-white/5 flex items-center gap-3">
          <div class="flex items-center gap-1.5">
            <div class="w-2 h-2 rounded-full bg-red-400"></div>
            <span class="text-[10px] text-secondary font-bold uppercase">> 2 Yr</span>
          </div>
          <div class="flex items-center gap-1.5">
            <div class="w-2 h-2 rounded-full bg-amber-400"></div>
            <span class="text-[10px] text-secondary font-bold uppercase">> 1 Yr</span>
          </div>
          <div class="flex items-center gap-1.5">
            <div class="w-2 h-2 rounded-full bg-accent-emerald"></div>
            <span class="text-[10px] text-secondary font-bold uppercase">< 1 Yr</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Grid (Flex None) -->
    <div class="flex-none grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-for="stat in stats" :key="stat.name" class="glass-card !bg-surface-900/20 !backdrop-blur-lg p-5 group hover:border-white/10 transition-all duration-300">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs font-black text-secondary uppercase tracking-widest">{{ stat.name }}</p>
            <p class="text-4xl font-bold text-white mt-1">{{ stat.value }}</p>
          </div>
          <div class="w-12 h-12 rounded-2xl bg-surface-500/5 flex items-center justify-center group-hover:scale-110 transition-transform">
            <component :is="stat.icon" class="w-6 h-6" :class="stat.color" />
          </div>
        </div>
      </div>
    </div>

    <!-- Lists Container (Flex 1) -->
    <div class="flex-1 min-h-0 grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Left: Last Visit -->
      <div class="glass-card flex flex-col p-0 overflow-hidden">
        <div class="p-6 border-b border-white/5 bg-white/[0.02] flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-accent-emerald/10 flex items-center justify-center text-accent-emerald">
              <MapPin class="w-5 h-5" />
            </div>
            <div>
              <h3 class="text-lg font-bold text-white italic">Last <span class="text-accent-emerald">Visit</span> Insight</h3>
              <p class="text-[10px] text-secondary uppercase font-bold tracking-widest">Implementation & Maintenance</p>
            </div>
          </div>
          <span class="text-[10px] font-black text-surface-500">{{ partnerStore.partners.length }} Partners</span>
        </div>
        
        <div class="flex-1 overflow-y-auto custom-scrollbar p-6 space-y-8">
          <div v-for="group in visitGroups" :key="group.name" class="space-y-4">
            <div v-if="group.name" class="flex items-center gap-3 sticky top-0 bg-surface-900/80 backdrop-blur-md py-2 z-10">
              <span class="text-[11px] font-black text-accent-cyan uppercase tracking-[0.2em]">{{ group.name }}</span>
              <div class="h-px flex-1 bg-gradient-to-r from-accent-cyan/20 to-transparent"></div>
            </div>
            
            <div class="space-y-3">
              <div v-for="partner in group.partners" :key="partner.id" 
                @click="openPartnerEdit(partner)"
                class="group flex items-center gap-4 p-4 rounded-2xl bg-white/[0.02] border border-white/5 hover:bg-white/[0.05] transition-all cursor-pointer relative overflow-hidden select-none"
              >
                <!-- Indicator Glow -->
                <div class="absolute left-0 top-0 bottom-0 w-1" :class="partner.statusClass.split(' ')[1].replace('text', 'bg')"></div>
                
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between mb-1">
                    <h4 class="font-bold text-white group-hover:text-accent-cyan transition-colors truncate pr-2">{{ partner.name }}</h4>
                    <span class="px-2 py-0.5 rounded-md border text-[9px] font-black uppercase tracking-tighter" :class="partner.statusClass">
                      {{ partner.date ? formatDate(partner.date) : 'NEVER' }}
                    </span>
                  </div>
                  <div class="flex items-center gap-3 text-[10px] text-secondary font-bold uppercase tracking-widest">
                    <span class="flex items-center gap-1.5"><Clock class="w-3 h-3 text-accent-cyan" /> {{ getTypeName(partner.typeId) }}</span>
                  </div>
                </div>
                <ChevronRight class="w-4 h-4 text-surface-600 group-hover:text-white transition-colors" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Last Project -->
      <div class="glass-card flex flex-col p-0 overflow-hidden">
        <div class="p-6 border-b border-white/5 bg-white/[0.02] flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-accent-cyan/10 flex items-center justify-center text-accent-cyan">
              <TrendingUp class="w-5 h-5" />
            </div>
            <div>
              <h3 class="text-lg font-bold text-white italic">Last <span class="text-accent-cyan">Project</span> Insight</h3>
              <p class="text-[10px] text-secondary uppercase font-bold tracking-widest">Remote & Support Activities</p>
            </div>
          </div>
          <span class="text-[10px] font-black text-surface-500">{{ partnerStore.partners.length }} Partners</span>
        </div>

        <div class="flex-1 overflow-y-auto custom-scrollbar p-6 space-y-8">
          <div v-for="group in projectGroups" :key="group.name" class="space-y-4">
            <div v-if="group.name" class="flex items-center gap-3 sticky top-0 bg-surface-900/80 backdrop-blur-md py-2 z-10">
              <span class="text-[11px] font-black text-accent-emerald uppercase tracking-[0.2em]">{{ group.name }}</span>
              <div class="h-px flex-1 bg-gradient-to-r from-accent-emerald/20 to-transparent"></div>
            </div>
            
            <div class="space-y-3">
              <div v-for="partner in group.partners" :key="partner.id" 
                @click="openPartnerEdit(partner)"
                class="group flex items-center gap-4 p-4 rounded-2xl bg-white/[0.02] border border-white/5 hover:bg-white/[0.05] transition-all cursor-pointer relative overflow-hidden select-none"
              >
                <!-- Indicator Glow -->
                <div class="absolute left-0 top-0 bottom-0 w-1" :class="partner.statusClass.split(' ')[1].replace('text', 'bg')"></div>

                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between mb-1">
                    <h4 class="font-bold text-white group-hover:text-accent-emerald transition-colors truncate pr-2">{{ partner.name }}</h4>
                    <span class="px-2 py-0.5 rounded-md border text-[9px] font-black uppercase tracking-tighter" :class="partner.statusClass">
                      {{ partner.date ? formatDate(partner.date) : 'NEVER' }}
                    </span>
                  </div>
                  <div class="flex items-center gap-3 text-[10px] text-secondary font-bold uppercase tracking-widest">
                    <span class="flex items-center gap-1.5"><Calendar class="w-3 h-3 text-accent-emerald" /> {{ getTypeName(partner.typeId) }}</span>
                  </div>
                </div>
                <ChevronRight class="w-4 h-4 text-surface-600 group-hover:text-white transition-colors" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Form Slide-over -->
    <PartnerFormView 
      v-if="isFormOpen" 
      :partner="selectedPartner"
      @close="isFormOpen = false"
      @success="handleFormSuccess"
    />
  </div>
</template>

<style scoped>
.glass-card {
  background-color: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 32px;
  overflow: hidden;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.1);
}
</style>
