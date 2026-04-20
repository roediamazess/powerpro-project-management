<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useProjectStore } from '../store/project'
import AppGrid from '../components/ui/AppGrid.vue'
import ProjectFormView from './ProjectFormView.vue'
import { Plus, Calendar, Users, RefreshCw, Layers } from 'lucide-vue-next'

const projectStore = useProjectStore()
const isFormOpen = ref(false)
const selectedProject = ref<any>(null)

const columnDefs = [
  { 
    headerName: 'Project Name', field: 'name', sortable: true, filter: true, pinned: 'left',
    cellRenderer: (params: any) => `
      <div class="flex flex-col py-2">
        <span class="font-bold text-white">${params.value}</span>
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
    headerName: 'Team', field: 'pics', width: 120,
    cellRenderer: (params: any) => {
      if (!params.value || params.value.length === 0) return '<span class="text-xs text-surface-600 italic">No assigned team</span>'
      return `
        <div class="flex -space-x-2 mt-3">
          ${params.value.slice(0, 3).map((pic: any) => `
            <div class="w-7 h-7 rounded-full bg-surface-700 border-2 border-surface-900 flex items-center justify-center text-[10px] font-bold text-accent-cyan ring-1 ring-white/5" title="${pic.fullname}">
              ${pic.fullname.charAt(0)}
            </div>
          `).join('')}
          ${params.value.length > 3 ? `<div class="w-7 h-7 rounded-full bg-surface-800 border-2 border-surface-900 flex items-center justify-center text-[8px] font-medium text-surface-400">+${params.value.length - 3}</div>` : ''}
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
</script>

<template>
  <div class="space-y-8" v-auto-animate>
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-primary tracking-tight italic">Project <span class="text-accent-emerald">Control</span></h1>
        <p class="text-secondary mt-1">Operational lifecycle, teambuilding, and point achievement monitoring.</p>
      </div>
      <div class="flex items-center gap-3">
        <button @click="projectStore.fetchProjects()" class="p-3 glass rounded-xl text-secondary hover:text-accent-emerald transition-all">
          <RefreshCw class="w-5 h-5" :class="{ 'animate-spin': projectStore.isLoading }" />
        </button>
        <button @click="openAddForm" class="btn-primary flex items-center gap-2 bg-gradient-to-r from-accent-cyan to-accent-emerald">
          <Plus class="w-5 h-5" />
          Initialize Project
        </button>
      </div>
    </div>

    <!-- Stats Bar -->
    <div class="grid grid-cols-4 gap-4">
      <div class="glass-card p-4 flex items-center gap-4 border-l-2 border-l-accent-cyan">
        <div class="p-2 bg-accent-cyan/10 rounded-lg text-accent-cyan"><Layers class="w-5 h-5" /></div>
        <div><p class="text-[10px] text-secondary font-bold uppercase">Active Projects</p><p class="text-xl font-bold text-primary">{{ projectStore.projects.length }}</p></div>
      </div>
      <div class="glass-card p-4 flex items-center gap-4 border-l-2 border-l-orange-400">
        <div class="p-2 bg-orange-400/10 rounded-lg text-orange-400"><Calendar class="w-5 h-5" /></div>
        <div><p class="text-[10px] text-secondary font-bold uppercase">Expiring Soon</p><p class="text-xl font-bold text-primary">03</p></div>
      </div>
      <div class="glass-card p-4 flex items-center gap-4 border-l-2 border-l-accent-emerald text-accent-emerald">
        <div class="p-2 bg-accent-emerald/10 rounded-lg"><Users class="w-5 h-5" /></div>
        <div><p class="text-[10px] text-secondary font-bold uppercase">Total Team Size</p><p class="text-xl font-bold text-primary">12</p></div>
      </div>
      <div class="glass-card p-4 flex items-center gap-4 border-l-2 border-l-red-500 text-red-500">
        <div class="p-2 bg-red-500/10 rounded-lg font-black italic">!</div>
        <div><p class="text-[10px] text-secondary font-bold uppercase">Kritikal</p><p class="text-xl font-bold text-primary">01</p></div>
      </div>
    </div>

    <!-- Data Grid -->
    <div class="relative">
      <AppGrid 
        :rowData="projectStore.projects" 
        :columnDefs="columnDefs" 
        height="550px" 
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
