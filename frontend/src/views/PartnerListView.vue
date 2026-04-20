<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { usePartnerStore } from '../store/partner'
import AppGrid from '../components/ui/AppGrid.vue'
import PartnerFormView from './PartnerFormView.vue'
import { Search, Filter, RefreshCw } from 'lucide-vue-next'

const partnerStore = usePartnerStore()
const isFormOpen = ref(false)
const selectedPartner = ref<any>(null)
const searchQuery = ref('')

const columnDefs = [
  { 
    headerName: 'Partner Name', field: 'name', sortable: true, filter: true, pinned: 'left',
    cellRenderer: (params: any) => `
      <div style="display: flex; flex-direction: column; justify-content: center; height: 100%; padding: 8px 0;">
        <div style="font-weight: 700; color: var(--text-primary); line-height: 1.2;">${params.value}</div>
        <div style="font-size: 10px; font-weight: 800; color: #0ea5e9; text-transform: uppercase; margin-top: 4px; letter-spacing: 0.05em;">
          ${params.data.partner_cnc || 'NO CNC'}
        </div>
      </div>
    `,
    autoHeight: true
  },
  { headerName: 'Type', field: 'type_id', width: 120 },
  { 
    headerName: 'Status', field: 'status_id', 
    cellRenderer: (params: any) => {
      const colors: any = { ACTIVE: 'text-accent-emerald bg-accent-emerald/10', INACTIVE: 'text-orange-400 bg-orange-400/10' }
      const color = colors[params.value] || 'text-secondary bg-surface-500/10'
      return `<span class="px-2 py-1 rounded-full text-xs font-bold ${color}">${params.value}</span>`
    }
  },
  { headerName: 'Rooms', field: 'rooms', width: 100 },
  { headerName: 'Stars', field: 'stars', width: 100 },
  { headerName: 'Address', field: 'address', flex: 2, minWidth: 250 },
  { 
    headerName: 'Last Visit', field: 'last_visit_at', 
    valueFormatter: (params: any) => params.value ? new Date(params.value).toLocaleDateString() : '-'
  },
  { 
    headerName: 'Last Project', field: 'last_project', 
    valueFormatter: (params: any) => params.value ? new Date(params.value).toLocaleDateString() : '-'
  },
  { 
    headerName: 'Last Updated', field: 'updated_at', 
    valueFormatter: (params: any) => new Date(params.value).toLocaleDateString() 
  },
  {
    headerName: 'Actions',
    width: 100,
    cellRenderer: () => `
      <button class="p-2 hover:bg-surface-500/10 rounded-lg text-secondary hover:text-primary transition-all">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"/><circle cx="12" cy="5" r="1"/><circle cx="12" cy="19" r="1"/></svg>
      </button>
    `
  }
]

onMounted(() => {
  partnerStore.fetchPartners()
})

const openAddForm = () => {
  selectedPartner.value = null
  isFormOpen.value = true
}

const handleFormSuccess = () => {
  isFormOpen.value = false
  partnerStore.fetchPartners()
}

const onRowDoubleClicked = (params: any) => {
  selectedPartner.value = params.data
  isFormOpen.value = true
}

const onCellClicked = (params: any) => {
  if (params.colDef.headerName === 'Actions') {
    selectedPartner.value = params.data
    isFormOpen.value = true
  }
}
</script>

<template>
  <div class="space-y-8" v-auto-animate>
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-primary tracking-tight italic">Partner <span class="text-accent-cyan">Database</span></h1>
        <p class="text-secondary mt-1">Management of hotels, resorts, and operational partners.</p>
      </div>
      <div class="flex items-center gap-3">
        <button @click="partnerStore.fetchPartners()" class="p-3 glass rounded-xl text-secondary hover:text-accent-cyan transition-all">
          <RefreshCw class="w-5 h-5" :class="{ 'animate-spin': partnerStore.isLoading }" />
        </button>
        <button @click="openAddForm" class="btn-primary !w-auto px-8 flex items-center gap-2 bg-gradient-to-r from-accent-emerald to-accent-cyan">
          Add Partner
        </button>
      </div>
    </div>

    <!-- Filters placeholder -->
    <div class="glass-card flex items-center gap-6 py-4">
      <div class="relative flex-1 group">
        <div class="absolute left-4 top-1/2 -translate-y-1/2 flex items-center pointer-events-none z-10">
          <Search class="w-4 h-4 text-secondary group-focus-within:text-accent-cyan transition-colors" />
        </div>
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Quick search partners by name, CNC, or address..."
          class="w-full bg-surface-500/5 border border-border-app rounded-xl py-2 pr-4 text-sm focus:outline-none focus:border-accent-cyan/50 focus:bg-card transition-all shadow-inner"
          style="padding-left: 3.5rem !important;"
        />
      </div>
      <div class="flex items-center gap-3">
        <button class="px-4 py-2 glass rounded-lg text-sm flex items-center gap-2 hover:border-border-app group text-secondary hover:text-primary">
          <Filter class="w-4 h-4" /> Filter
        </button>
        <div class="h-8 w-px bg-border-app"></div>
        <span class="text-xs text-secondary font-black tracking-widest uppercase">Live View</span>
      </div>
    </div>

    <!-- Data Grid -->
    <div class="relative">
      <AppGrid 
        :rowData="partnerStore.partners" 
        :columnDefs="columnDefs" 
        :quickFilterText="searchQuery"
        height="600px" 
        @row-double-clicked="onRowDoubleClicked"
        @cell-clicked="onCellClicked"
      />
      
      <!-- Loading Overlay -->
      <div v-if="partnerStore.isLoading" class="absolute inset-0 glass flex items-center justify-center z-10 rounded-2xl">
        <RefreshCw class="w-10 h-10 text-accent-cyan animate-spin" />
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
