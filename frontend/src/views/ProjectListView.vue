<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useProjectStore } from '../store/project'
import { useSettingsStore } from '../store/settings'
import { useUIStore } from '../store/ui'
import AppGrid from '../components/ui/AppGrid.vue'
import ProjectFormView from './ProjectFormView.vue'
import { RefreshCw, Search } from 'lucide-vue-next'

// Match Partner Pattern: Local Search State
const currentSearch = ref('')

const projectStore = useProjectStore()
const settingsStore = useSettingsStore()
const uiStore = useUIStore()

const isFormOpen = ref(false)
const selectedProject = ref<any>(null)
const selectedTab = ref('ALL')
const gridResultCount = ref(0)

/**
 * Section 11.5 Standardized Status Groups
 * Mapped to actual database values: PLANNING, SCHEDULED, RUNNING, DOCUMENT, DONE, etc.
 */
const STATUSTABS = [
  { id: 'PREPARATION', name: 'Preparation', statuses: ['PLANNING', 'SCHEDULED'], color: 'text-accent-cyan' },
  { id: 'PROGRESS', name: 'Progress', statuses: ['RUNNING'], color: 'text-accent-emerald' },
  { id: 'DOCUMENTATION', name: 'Documentation', statuses: ['DOCUMENT', 'DOCUMENT-CHECK'], color: 'text-orange-400' },
  { id: 'DONE', name: 'Done', statuses: ['DONE', 'COMPLETED'], color: 'text-primary' },
  { id: 'X', name: 'X', statuses: ['CANCELLED', 'REJECTED'], color: 'text-red-400' },
  { id: 'ALL', name: 'All', statuses: [], color: 'text-primary' }
]

const filteredItems = computed(() => {
  let items = projectStore.projects || []
  const q = currentSearch.value.toLowerCase().trim()

  // 1. Status Tab Filtering
  const activeTab = STATUSTABS.find(t => t.id === selectedTab.value)
  if (activeTab && activeTab.statuses.length > 0) {
    items = items.filter((p: any) => activeTab.statuses.includes(p.status_id))
  }

  // 2. Smart Search Filtering (FORCED VUE-LEVEL)
  if (q) {
    items = items.filter((p: any) => {
      // Find Name from lookup using either id or type_id
      const typeObj = settingsStore.projectLookups?.types?.find((t: any) => 
        String(t.type_id || t.id) === String(p.type_id)
      )
      const typeName = typeObj?.name || ''
      const typeId = String(p.type_id || '')
      
      const statusObj = settingsStore.projectLookups?.statuses?.find((s: any) => 
        String(s.status_id || s.id) === String(p.status_id)
      )
      const statusName = statusObj?.name || ''
      
      const teamNames = Array.isArray(p.pic_assignments) ? p.pic_assignments.map((pic: any) => `${pic.username || ''} ${pic.fullname || ''}`).join(' ') : ''
      
      // Timeline formatting for search (e.g. "22 Apr 26")
      const formatDate = (d: any) => d ? new Intl.DateTimeFormat('en-GB', { day: '2-digit', month: 'short', year: '2-digit' }).format(new Date(d)) : ''
      const timelineStr = `${p.start_date || ''} ${p.end_date || ''} ${formatDate(p.start_date)} ${formatDate(p.end_date)}`
      
      const searchTarget = `
        ${p.name} ${p.cnc_id || ''} ${p.partner?.name || ''} 
        ${typeName} ${typeId} ${statusName} ${p.status_id} ${teamNames} ${timelineStr}
      `.toLowerCase()
      return searchTarget.includes(q)
    })
  }

  return items
})

const columnDefs = [
  { 
    headerName: 'CNC ID', field: 'cnc_id', width: 90, pinned: 'left',
    cellRenderer: (params: any) => `<span class="text-[11px] font-black text-accent-emerald tracking-tighter uppercase font-sans">${params.value || '-'}</span>`
  },
  { 
    headerName: 'Project Name', field: 'name', sortable: true, filter: true, pinned: 'left',
    getQuickFilterText: (params: any) => `${params.value} ${params.data.partner?.name || ''}`,
    cellRenderer: (params: any) => `
      <div class="flex flex-col py-2">
        <span class="font-bold text-primary">${params.value}</span>
        <span class="text-xs text-accent-cyan font-medium">${params.data.partner?.name || 'No Partner'}</span>
      </div>
    `
  },
  { 
    headerName: 'Type', field: 'type_id', width: 130,
    cellRenderer: (params: any) => {
      const type = settingsStore.projectLookups?.types?.find((t: any) => String(t.type_id || t.id) === String(params.value))
      const label = type?.name || params.value || '-'
      return `<span class="text-[10px] font-bold text-primary uppercase tracking-wider">${label}</span>`
    }
  },
  { 
    headerName: 'Status', field: 'status_id', width: 130,
    getQuickFilterText: (params: any) => (settingsStore.projectLookups?.statuses || []).find(s => String(s.status_id) === String(params.value))?.name || params.value,
    cellRenderer: (params: any) => {
      const colors: any = { 
        PLANNING: 'text-surface-400 bg-surface-400/10', 
        SCHEDULED: 'text-accent-cyan bg-accent-cyan/10 border-accent-cyan/20',
        RUNNING: 'text-accent-emerald bg-accent-emerald/10 border-accent-emerald/20', 
        DONE: 'text-primary bg-primary/10',
        ON_HOLD: 'text-orange-400 bg-orange-400/10'
      }
      const color = colors[params.value] || 'text-surface-500 bg-surface-500/10'
      return `<span class="px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest border ${color}">${params.value?.replace('_', ' ') || ''}</span>`
    }
  },
  { 
    headerName: 'Timeline', field: 'start_date', width: 180,
    getQuickFilterText: (params: any) => `${params.data.start_date || ''} ${params.data.end_date || ''}`,
    cellRenderer: (params: any) => {
      if (!params.data.start_date) return '-'
      const formatDate = (d: any) => new Intl.DateTimeFormat('en-GB', { day: '2-digit', month: 'short', year: '2-digit' }).format(new Date(d))
      const start = formatDate(params.data.start_date)
      const end = params.data.end_date ? formatDate(params.data.end_date) : 'TBD'
      return `
        <div class="flex items-center gap-2 font-bold tracking-tighter text-[11px] font-sans">
          <span class="text-accent-cyan/70">${start}</span>
          <span class="text-surface-400">→</span>
          <span class="text-accent-emerald/70">${end}</span>
        </div>
      `
    }
  },
  { headerName: 'Days', field: 'total_days', width: 80 },
  {
    headerName: 'Team', field: 'pic_assignments', width: 220,
    // THE KOMENG FIX: Ensure we check Array.isArray to prevent filter engine crashes on invalid data
    getQuickFilterText: (params: any) => {
      if (!Array.isArray(params.value)) return ''
      return params.value.map((p: any) => `${p.username || ''} ${p.fullname || ''}`).join(' ')
    },
    cellRenderer: (params: any) => {
      const teamData = params.data.pic_assignments
      const names = Array.isArray(teamData) ? teamData.map((p: any) => p.username || 'Unknown') : []
      if (names.length === 0) return `<span class="text-secondary italic text-xs">No Team</span>`
      
      return `
        <div class="flex flex-wrap gap-1 py-1">
          ${names.map((name: string) => `
            <span class="px-2 py-0.5 bg-surface-500/10 text-secondary text-[10px] font-black uppercase rounded-full border border-border-app tracking-tighter">
              ${name}
            </span>
          `).join('')}
        </div>
      `
    }
  },
  {
    headerName: 'Appr.', field: 'status', width: 100,
    cellRenderer: (params: any) => {
      const isApproved = params.value === 'APPROVED'
      const color = isApproved ? 'text-accent-emerald bg-accent-emerald/10 border-accent-emerald/30' : 'text-surface-500 bg-surface-500/10 border-white/5'
      const icon = isApproved ? '✓' : '○'
      return `<div class="flex items-center justify-center h-full"><span class="px-2 py-0.5 rounded-full text-[9px] font-black uppercase tracking-tighter border ${color}">${icon} ${params.value}</span></div>`
    }
  }
]

onMounted(async () => {
  await projectStore.fetchProjects()
  await settingsStore.fetchProjectLookups()
})

const openAddForm = () => {
  selectedProject.value = null
  isFormOpen.value = true
}

const handleFormSuccess = () => {
  isFormOpen.value = false
  projectStore.fetchProjects()
}

const onRowDoubleClicked = (params: any) => {
  selectedProject.value = params.data
  isFormOpen.value = true
}
</script>

<template>
  <div class="h-full flex flex-col space-y-4 pb-2">
    <!-- Header Decor & Title -->
    <div class="flex-none flex items-center justify-between">
      <div class="flex items-center gap-3">
        <button @click="openAddForm" class="btn-primary !w-auto px-8 flex items-center gap-2 bg-gradient-to-r from-accent-cyan to-accent-emerald border-none shadow-lg shadow-accent-emerald/10">
          Add Project
        </button>
        <button @click="projectStore.fetchProjects()" class="p-3 glass rounded-xl text-secondary hover:text-accent-emerald transition-all">
          <RefreshCw class="w-5 h-5" :class="{ 'animate-spin': projectStore.isLoading }" />
        </button>
        
        <!-- Local Search - Partner Reference Style -->
        <div class="relative group ml-2">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-surface-500 group-focus-within:text-accent-emerald transition-colors z-10" />
          <input 
            v-model="currentSearch"
            type="text" 
            placeholder="Search projects..."
            class="w-48 xl:w-64 bg-surface-500/5 hover:bg-surface-500/10 border border-border-app hover:border-white/10 rounded-xl py-2 pl-9 pr-4 text-sm font-medium focus:outline-none focus:border-accent-emerald/50 focus:ring-1 focus:ring-accent-emerald/50 focus:bg-bg-card transition-all shadow-inner relative"
          />
        </div>
      </div>
      <div class="text-right">
        <h1 class="text-3xl font-bold text-primary tracking-tight italic">Project <span class="text-accent-emerald">Control</span></h1>
        <p class="text-secondary mt-1">Operational lifecycle, teambuilding, and point achievement monitoring.</p>
      </div>
    </div>

    <!-- Status Tabs - Standard 11.5 Section -->
    <div class="flex items-center gap-2 p-1.5 glass rounded-2xl w-fit border-border-app/50 shadow-inner">
      <button 
        v-for="tab in STATUSTABS" 
        :key="tab.id"
        @click="selectedTab = tab.id"
        class="relative px-6 py-2.5 rounded-xl text-xs font-black uppercase tracking-widest transition-all duration-300 overflow-hidden group"
        :class="[
          selectedTab === tab.id 
            ? 'text-white shadow-lg' 
            : 'text-surface-500 hover:text-primary hover:bg-white/5'
        ]"
      >
        <!-- Active Background -->
        <div v-if="selectedTab === tab.id" class="absolute inset-0 bg-gradient-to-r from-accent-cyan/80 to-accent-emerald/80 -z-10 animate-in fade-in zoom-in duration-300"></div>
        
        <span class="relative flex items-center gap-2">
          {{ tab.name }}
          <span 
            v-if="selectedTab === tab.id" 
            class="px-1.5 py-0.5 rounded-md bg-white/20 text-[10px] font-bold"
          >
            {{ filteredItems.length }}
          </span>
        </span>
      </button>
    </div>

    <!-- Data Grid - Pure Vue Managed Filter (GURANTEED SYNC) -->
    <div class="flex-1 min-h-0 relative">
      <AppGrid 
        :rowData="filteredItems" 
        :columnDefs="columnDefs" 
        height="100%" 
        @row-double-clicked="onRowDoubleClicked"
      />
      
      <div v-if="projectStore.isLoading" class="absolute inset-0 glass flex items-center justify-center z-10 rounded-2xl">
        <RefreshCw class="w-10 h-10 text-accent-emerald animate-spin" />
      </div>
    </div>

    <!-- Modals -->
    <ProjectFormView 
      v-if="isFormOpen" 
      :project="selectedProject"
      @close="isFormOpen = false"
      @success="handleFormSuccess"
    />
  </div>
</template>
