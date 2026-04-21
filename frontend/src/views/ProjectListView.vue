<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useProjectStore } from '../store/project'
import AppGrid from '../components/ui/AppGrid.vue'
import ProjectFormView from './ProjectFormView.vue'
import { Plus, Calendar, Users, RefreshCw, Layers, Search } from 'lucide-vue-next'

const projectStore = useProjectStore()
const isFormOpen = ref(false)
const selectedProject = ref<any>(null)
const currentSearch = ref('')
const selectedTab = ref('ALL')

const STATUSTABS = [
  { id: 'PREPARATION', name: 'Preparation', statuses: ['TENTATIVE', 'SCHEDULED'], color: 'text-accent-cyan' },
  { id: 'PROGRESS', name: 'Progress', statuses: ['RUNNING'], color: 'text-accent-emerald' },
  { id: 'DOCUMENTATION', name: 'Documentation', statuses: ['DOCUMENT', 'DOCUMENT CHECK'], color: 'text-accent-teal' },
  { id: 'DONE', name: 'Done', statuses: ['DONE'], color: 'text-surface-400' },
  { id: 'X', name: 'X', statuses: ['CANCELLED', 'REJECTED'], color: 'text-red-400' },
  { id: 'ALL', name: 'All', statuses: [], color: 'text-primary' }
]

const filteredItems = computed(() => {
  let items = projectStore.projects

  // Status Filter
  const activeTab = STATUSTABS.find(t => t.id === selectedTab.value)
  if (activeTab && activeTab.statuses.length > 0) {
    items = items.filter((p: any) => activeTab.statuses.includes(p.status_id))
  }

  // Search Filter
  if (currentSearch.value) {
    const q = currentSearch.value.toLowerCase()
    items = items.filter((p: any) => 
      p.name.toLowerCase().includes(q) || 
      (p.partner?.name || '').toLowerCase().includes(q)
    )
  }

  return items
})

const columnDefs = [
  { 
    headerName: 'Project Name', field: 'name', sortable: true, filter: true, pinned: 'left',
    cellRenderer: (params: any) => `
      <div class="flex flex-col py-2">
        <span class="font-bold text-primary">${params.value}</span>
        <span class="text-xs text-accent-cyan">${params.data.partner?.name || 'No Partner'}</span>
      </div>
    `
  },
  { 
    headerName: 'Status', field: 'status_id', width: 130,
    cellRenderer: (params: any) => {
      const colors: any = { 
        PLANNING: 'text-surface-400 bg-surface-400/10', 
        IN_PROGRESS: 'text-accent-cyan bg-accent-cyan/10 border-accent-cyan/20', 
        COMPLETED: 'text-accent-emerald bg-accent-emerald/10',
        ON_HOLD: 'text-orange-400 bg-orange-400/10'
      }
      const color = colors[params.value] || 'text-surface-500 bg-surface-500/10'
      return `<span class="px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest border ${color}">${params.value.replace('_', ' ')}</span>`
    }
  },
  {
    headerName: 'Progress', field: 'point_percent', width: 150,
    cellRenderer: (params: any) => `
      <div class="w-full bg-surface-800 h-1.5 rounded-full mt-5 relative overflow-hidden">
        <div class="bg-gradient-to-r from-accent-cyan to-accent-emerald h-full rounded-full transition-all" style="width: ${params.value || 0}%"></div>
      </div>
    `
  },
  {
    headerName: 'Team', field: 'pic_assignments', width: 220,
    cellRenderer: (params: any) => {
      if (!params.value || params.value.length === 0) return '<span class="text-xs text-secondary italic">No assigned team</span>'
      const names = params.value.map((pic: any) => pic.username || 'Anonymous')
      return `
        <div class="flex flex-wrap gap-1 mt-2">
          ${names.map((name: string) => `
            <span class="px-2 py-0.5 rounded bg-surface-500/10 text-[10px] font-bold text-primary border border-border-app shadow-sm transition-all">
              ${name}
            </span>
          `).join('')}
        </div>
      `
    }
  },
  { 
    headerName: 'Timeline', field: 'start_date', width: 180,
    cellRenderer: (params: any) => {
      if (!params.data.start_date) return '-'
      const start = new Date(params.data.start_date).toLocaleDateString()
      const end = params.data.end_date ? new Date(params.data.end_date).toLocaleDateString() : 'TBD'
      return `<div class="text-[10px] font-medium text-surface-400 mt-2">${start} → ${end}</div>`
    }
  },
  { headerName: 'Days', field: 'total_days', width: 80 }
]

onMounted(() => {
  projectStore.fetchProjects()
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
  <div class="space-y-8" v-auto-animate>
    <!-- Header -->
    <div class="flex-none flex items-center justify-between">
      <div class="flex items-center gap-3">
        <button @click="openAddForm" class="btn-primary !w-auto px-8 flex items-center gap-2 bg-gradient-to-r from-accent-cyan to-accent-emerald border-none shadow-lg shadow-accent-emerald/10">
          Add Project
        </button>
        <button @click="projectStore.fetchProjects()" class="p-3 glass rounded-xl text-secondary hover:text-accent-emerald transition-all">
          <RefreshCw class="w-5 h-5" :class="{ 'animate-spin': projectStore.isLoading }" />
        </button>
        
        <!-- Local Search -->
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

    <!-- Status Tabs -->
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

    <!-- Data Grid -->
    <div class="relative">
      <AppGrid 
        :rowData="filteredItems" 
        :columnDefs="columnDefs" 
        :quickFilterText="currentSearch"
        height="550px" 
        @rowDoubleClicked="onRowDoubleClicked"
      />
      
      <div v-if="projectStore.isLoading" class="absolute inset-0 glass flex items-center justify-center z-10 rounded-2xl">
        <RefreshCw class="w-10 h-10 text-accent-emerald animate-spin" />
      </div>
    </div>

    <!-- Form Slide-over -->
    <ProjectFormView 
      v-if="isFormOpen" 
      :project="selectedProject"
      @close="isFormOpen = false"
      @success="handleFormSuccess"
    />
  </div>
</template>
