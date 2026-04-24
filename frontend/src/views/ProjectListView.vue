<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { 
  Search, Plus, RefreshCw, Filter, 
  LayoutGrid, List as ListIcon, 
  ChevronRight, MoreHorizontal,
  Calendar, Users, Info
} from 'lucide-vue-next'
import { useProjectStore } from '../store/project'
import { useSettingsStore } from '../store/settings'
import { usePartnerStore } from '../store/partner'
import AppGrid from '../components/ui/AppGrid.vue'
import ProjectFormView from './ProjectFormView.vue'

const projectStore = useProjectStore()
const settingsStore = useSettingsStore()
const partnerStore = usePartnerStore()

const currentSearch = ref('')
const selectedTab = ref('PROGRESS')
const showAddForm = ref(false)
const selectedProject = ref<any>(null)

/**
 * Status Groups mapping for Tabs
 * Mapped to actual database values: TENTATIVE, SCHEDULED, RUNNING, DOCUMENT, DONE, etc.
 */
const STATUSTABS = [
  { id: 'PREPARATION', name: 'Preparation', statuses: ['TENTATIVE', 'SCHEDULED'], color: 'text-accent-cyan' },
  { id: 'PROGRESS', name: 'Progress', statuses: ['RUNNING'], color: 'text-accent-emerald' },
  { id: 'DOCUMENTATION', name: 'Documentation', statuses: ['DOCUMENT', 'DOCUMENT-CHECK'], color: 'text-orange-400' },
  { id: 'DONE', name: 'Done', statuses: ['DONE'], color: 'text-primary' },
  { id: 'X', name: 'X', statuses: ['CANCELLED', 'REJECTED'], color: 'text-red-400' },
  { id: 'ALL', name: 'All', statuses: [], color: 'text-primary' }
]

const filteredItems = computed(() => {
  let items = projectStore.projects || []
  const q = currentSearch.value.toLowerCase().trim()

  // 1. Status Tab Filtering
  const activeTab = STATUSTABS.find(t => t.id === selectedTab.value)
  if (activeTab && activeTab.statuses.length > 0) {
    items = items.filter((p: any) => {
      const pStatus = String(p.status_id || '').trim().toUpperCase()
      return activeTab.statuses.includes(pStatus)
    })
  }

  // 2. Smart Search Filtering
  if (q) {
    items = items.filter((p: any) => {
      const typeObj = settingsStore.projectLookups?.types?.find((t: any) => 
        String(t.type_id || t.id) === String(p.type_id)
      )
      const typeName = typeObj?.name || ''
      
      const statusObj = settingsStore.projectLookups?.statuses?.find((s: any) => 
        String(s.status_id || s.id) === String(p.status_id)
      )
      const statusName = statusObj?.name || ''
      
      const teamNames = Array.isArray(p.pic_assignments) ? p.pic_assignments.map((pic: any) => `${pic.username || ''} ${pic.fullname || ''}`).join(' ') : ''
      const formatDate = (d: any) => d ? new Intl.DateTimeFormat('en-GB', { day: '2-digit', month: 'short', year: '2-digit' }).format(new Date(d)) : ''
      const timelineStr = `${p.start_date || ''} ${p.end_date || ''} ${formatDate(p.start_date)} ${formatDate(p.end_date)}`
      
      const searchTarget = `${p.name} ${p.cnc_id || ''} ${p.partner?.name || ''} ${typeName} ${statusName} ${p.status_id} ${teamNames} ${timelineStr}`.toLowerCase()
      return searchTarget.includes(q)
    })
  }

  return items
})

const columnDefs = [
  { 
    headerName: 'CNC ID', 
    field: 'cnc_id', 
    width: 100,
    cellClass: 'font-mono text-accent-cyan font-bold'
  },
  { 
    headerName: 'Project Name', 
    field: 'name', 
    flex: 2,
    cellRenderer: (params: any) => {
      return `
        <div class="flex flex-col py-1">
          <span class="font-bold text-primary line-clamp-1">${params.value}</span>
          <span class="text-[10px] text-secondary truncate">${params.data.partner?.name || 'No Partner'}</span>
        </div>
      `
    }
  },
  { 
    headerName: 'Type', 
    field: 'type_id', 
    width: 150,
    valueFormatter: (params: any) => {
      const type = settingsStore.projectLookups?.types?.find((t: any) => String(t.type_id || t.id) === String(params.value))
      return type?.name || params.value
    }
  },
  { 
    headerName: 'Status', 
    field: 'status_id', 
    width: 160,
    cellRenderer: (params: any) => {
      const statusObj = settingsStore.projectLookups?.statuses?.find((s: any) => 
        String(s.status_id || s.id) === String(params.value)
      )
      const statusName = statusObj?.name || params.value
      
      const colors_mapping: any = {
        'TENTATIVE': 'bg-accent-cyan/10 text-accent-cyan border-accent-cyan/20',
        'SCHEDULED': 'bg-accent-cyan/10 text-accent-cyan border-accent-cyan/20',
        'RUNNING': 'bg-accent-emerald/10 text-accent-emerald border-accent-emerald/20',
        'DOCUMENT': 'bg-orange-400/10 text-orange-400 border-orange-400/20',
        'DOCUMENT-CHECK': 'bg-orange-400/10 text-orange-400 border-orange-400/20',
        'DONE': 'bg-surface-700 text-surface-400 border-surface-600',
        'CANCELLED': 'bg-red-400/10 text-red-400 border-red-400/20',
        'REJECTED': 'bg-red-400/10 text-red-400 border-red-400/20'
      }
      const colorClass = colors_mapping[params.value] || 'bg-surface-800 text-surface-400'
      return `<div class="flex items-center h-full"><span class="px-3 py-1 rounded-full text-[10px] font-black border ${colorClass}">${statusName}</span></div>`
    }
  },
  {
    headerName: 'Timeline',
    field: 'start_date',
    width: 160,
    cellRenderer: (params: any) => {
      const formatDate = (d: any) => d ? new Intl.DateTimeFormat('en-GB', { day: '2-digit', month: 'short', year: '2-digit' }).format(new Date(d)) : '-'
      return `
        <div class="flex items-center gap-2 text-[10px] font-bold text-secondary">
          <span class="text-accent-cyan">${formatDate(params.data.start_date)}</span>
          <span class="opacity-30">→</span>
          <span class="text-accent-emerald">${formatDate(params.data.end_date)}</span>
        </div>
      `
    }
  },
  { 
    headerName: 'Days', 
    field: 'total_days', 
    width: 80,
    cellClass: 'font-bold text-primary'
  },
  {
    headerName: 'Team',
    field: 'pic_assignments',
    width: 200,
    cellRenderer: (params: any) => {
      if (!params.value || params.value.length === 0) return '<span class="text-surface-600 italic text-xs">No Team</span>'
      return `
        <div class="flex flex-wrap gap-1 items-center h-full py-1">
          ${params.value.map((pic: any) => `
            <span class="px-2 py-0.5 rounded-md bg-accent-cyan/10 text-accent-cyan text-[9px] font-bold border border-accent-cyan/20 whitespace-nowrap">
              ${pic.username}
            </span>
          `).join('')}
        </div>
      `
    }
  },
  {
    headerName: 'Appr.',
    width: 100,
    pinned: 'right',
    cellRenderer: (params: any) => {
      const isApproved = params.data.status === 'APPROVED'
      return `
        <div class="flex items-center justify-center h-full">
          <div class="px-2 py-0.5 rounded text-[8px] font-black uppercase tracking-tighter border ${isApproved ? 'bg-accent-emerald/10 text-accent-emerald border-accent-emerald/20' : 'bg-surface-800 text-surface-500 border-surface-700'}">
            ${isApproved ? 'Approved' : 'Open'}
          </div>
        </div>
      `
    }
  }
]

onMounted(async () => {
  projectStore.fetchProjects()
  settingsStore.fetchProjectLookups()
  partnerStore.fetchPartners()
})

const openAddForm = () => {
  selectedProject.value = null
  showAddForm.value = true
}

const onRowClicked = (params: any) => {
  selectedProject.value = params.data
  showAddForm.value = true
}

const handleSuccess = () => {
  showAddForm.value = false
  projectStore.fetchProjects()
}
</script>

<template>
  <div class="h-full flex flex-col space-y-4 pb-2">
    <!-- Header -->
    <div class="flex-none flex items-center justify-between">
      <div class="flex items-center gap-3">
        <button @click="openAddForm" class="btn-primary !w-auto px-8 flex items-center gap-2 bg-gradient-to-r from-accent-cyan to-accent-emerald border-none shadow-lg shadow-accent-emerald/10">
          <Plus class="w-5 h-5" />
          Add Project
        </button>
        <button @click="projectStore.fetchProjects" class="p-3 glass rounded-xl text-secondary hover:text-accent-cyan transition-all shadow-inner">
          <RefreshCw class="w-5 h-5" :class="{ 'animate-spin': projectStore.isLoading }" />
        </button>

        <!-- Search -->
        <div class="relative group ml-2">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-surface-500 group-focus-within:text-accent-cyan transition-colors z-10" />
          <input 
            v-model="currentSearch"
            type="text" 
            placeholder="Search project, CNC ID, partner, or team..."
            class="w-64 xl:w-80 bg-surface-500/5 hover:bg-surface-500/10 border border-border-app hover:border-white/10 rounded-xl py-2.5 pl-10 pr-4 text-sm font-medium focus:outline-none focus:border-accent-cyan/50 focus:ring-1 focus:ring-accent-cyan/50 focus:bg-surface-900 transition-all shadow-inner relative"
          />
        </div>
      </div>

      <div class="text-right">
        <h1 class="text-2xl font-black italic tracking-tight text-primary flex items-center justify-end gap-3">
          Project <span class="text-accent-cyan">Control</span>
        </h1>
        <p class="text-[10px] text-secondary font-medium tracking-wide uppercase">Operational lifecycle, teambuilding, and point achievement monitoring.</p>
      </div>
    </div>

    <!-- Status Tabs -->
    <div class="flex-none flex items-center justify-between bg-surface-500/5 p-1 rounded-2xl border border-border-app glass shadow-inner">
      <div class="flex items-center gap-1">
        <button 
          v-for="tab in STATUSTABS" 
          :key="tab.id"
          @click="selectedTab = tab.id"
          class="relative px-6 py-2 rounded-xl transition-all duration-300 group overflow-hidden"
          :class="selectedTab === tab.id ? 'text-white' : 'text-secondary hover:text-primary'"
        >
          <!-- Active Background -->
          <div v-if="selectedTab === tab.id" class="absolute inset-0 bg-gradient-to-r from-accent-cyan/80 to-accent-emerald/80 -z-10 animate-in fade-in zoom-in duration-300"></div>
          
          <span class="relative z-10 flex items-center gap-2">
            <span class="font-black text-[11px] uppercase tracking-widest">{{ tab.name }}</span>
            <span v-if="projectStore.projects.length > 0"
              class="px-1.5 py-0.5 rounded-md text-[9px] font-black transition-all"
              :class="selectedTab === tab.id ? 'bg-white/20 text-white' : 'bg-surface-800 text-surface-400'"
            >
              {{ 
                tab.id === 'ALL' 
                  ? projectStore.projects.length 
                  : projectStore.projects.filter(p => tab.statuses.includes(String(p.status_id).trim().toUpperCase())).length 
              }}
            </span>
          </span>
        </button>
      </div>
    </div>

    <!-- Grid -->
    <div class="flex-1 min-h-0 relative">
      <AppGrid 
        :columnDefs="columnDefs" 
        :rowData="filteredItems" 
        :isLoading="projectStore.isLoading"
        @rowDoubleClicked="onRowClicked"
      />
    </div>

    <!-- Form Modal -->
    <ProjectFormView 
      v-if="showAddForm" 
      :project="selectedProject"
      @close="showAddForm = false"
      @success="handleSuccess"
    />
  </div>
</template>

<style scoped>
.premium-input-field {
  width: 100%;
  background-color: var(--color-surface-500, rgba(127, 127, 127, 0.05));
  border: 1px solid var(--color-border-app, rgba(255, 255, 255, 0.1));
  border-radius: 0.75rem;
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s;
}
.premium-input-field:focus {
  outline: none;
  border-color: rgba(6, 182, 212, 0.5); /* accent-cyan-500/50 */
  box-shadow: 0 0 0 1px rgba(6, 182, 212, 0.5);
}
</style>
