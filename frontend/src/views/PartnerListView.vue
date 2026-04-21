<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { usePartnerStore } from '../store/partner'
import { useUIStore } from '../store/ui'
import { storeToRefs } from 'pinia'
import AppGrid from '../components/ui/AppGrid.vue'
import PartnerFormView from './PartnerFormView.vue'
import { RefreshCw, Search } from 'lucide-vue-next'

const currentSearch = ref('')

const partnerStore = usePartnerStore()
const isFormOpen = ref(false)
const selectedPartner = ref<any>(null)
const selectedTab = ref('ALL')
const gridResultCount = ref(0)

const STATUSTABS = [
  { id: 'ACTIVE', name: 'Active', statuses: ['ACTIVE'], color: 'text-accent-emerald' },
  { id: 'FREEZE', name: 'Freeze', statuses: ['FREEZE'], color: 'text-orange-400' },
  { id: 'INACTIVE', name: 'Inactive', statuses: ['INACTIVE'], color: 'text-red-400' },
  { id: 'ALL', name: 'All', statuses: [], color: 'text-primary' }
]

const filteredItems = computed(() => {
  let items = partnerStore.partners

  // Status Filter
  const activeTab = STATUSTABS.find(t => t.id === selectedTab.value)
  if (activeTab && activeTab.statuses.length > 0) {
    items = items.filter((p: any) => activeTab.statuses.includes(p.status_id))
  }

  return items
})

const columnDefs = [
  { 
    headerName: 'CNC ID', 
    field: 'partner_cnc', 
    width: 100, 
    pinned: 'left',
    cellRenderer: (params: any) => `<span class="font-black text-accent-cyan tracking-widest">${params.value || '-'}</span>`
  },
  { 
    headerName: 'Partner Name', 
    field: 'name', 
    minWidth: 250, 
    flex: 2,
    cellRenderer: (params: any) => `<span class="font-bold text-primary">${params.value}</span>`
  },
  { 
    headerName: 'Stars', 
    field: 'stars', 
    width: 100,
    cellRenderer: (params: any) => {
      const stars = parseInt(params.value) || 0
      return `<div class="text-amber-400 font-bold">${'★'.repeat(stars)}${'☆'.repeat(5 - stars)}</div>`
    }
  },
  { headerName: 'Room', field: 'rooms', width: 90 },
  { headerName: 'Outlet', field: 'outlets', width: 90 },
  { 
    headerName: 'System Version', 
    field: 'version_id', 
    width: 140,
    cellRenderer: (params: any) => {
      const version = partnerStore.lookups.versions.find(v => v.id === params.value)
      return `<span class="px-2 py-0.5 rounded-lg bg-surface-500/10 text-[10px] font-black text-secondary uppercase">${version?.name || params.value || '-'}</span>`
    }
  },
  { 
    headerName: 'System Type', 
    field: 'imp_type_id', 
    width: 140,
    cellRenderer: (params: any) => {
      const type = partnerStore.lookups.imp_types.find(t => t.id === params.value)
      return `<span class="text-accent-emerald font-bold">${type?.name || params.value || '-'}</span>`
    }
  },
  { 
    headerName: 'Group', 
    field: 'group_id', 
    width: 180,
    cellRenderer: (params: any) => {
      if (!params.value) return '<span class="text-secondary">-</span>'
      const val = params.value.toString().trim().toUpperCase()
      const group = partnerStore.lookups.groups.find((g: any) => g.id.toString().toUpperCase() === val)
      const label = group ? group.name : params.value
      return `<span class="font-semibold text-primary">${label}</span>`
    }
  },
]

onMounted(async () => {
  await partnerStore.fetchLookups()  // Fetch lookups first so cellRenderers can map IDs to Names
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


</script>

<template>
  <div class="h-full flex flex-col space-y-4 pb-2" v-auto-animate>
    <!-- Header -->
    <div class="flex-none flex items-center justify-between">
      <div class="flex items-center gap-3">
        <button @click="openAddForm" class="btn-primary !w-auto px-8 flex items-center gap-2 bg-gradient-to-r from-accent-emerald to-accent-cyan border-none shadow-lg shadow-accent-cyan/10">
          Add Partner
        </button>
        <button @click="partnerStore.fetchPartners()" class="p-3 glass rounded-xl text-secondary hover:text-accent-cyan transition-all">
          <RefreshCw class="w-5 h-5" :class="{ 'animate-spin': partnerStore.isLoading }" />
        </button>
        
        <!-- Local Search -->
        <div class="relative group ml-2">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-surface-500 group-focus-within:text-accent-cyan transition-colors z-10" />
          <input 
            v-model="currentSearch"
            type="text" 
            placeholder="Search partners..."
            class="w-48 xl:w-64 bg-surface-500/5 hover:bg-surface-500/10 border border-border-app hover:border-white/10 rounded-xl py-2 pl-9 pr-4 text-sm font-medium focus:outline-none focus:border-accent-cyan/50 focus:ring-1 focus:ring-accent-cyan/50 focus:bg-bg-card transition-all shadow-inner relative"
          />
        </div>
      </div>
      <div class="text-right">
        <h1 class="text-3xl font-bold text-primary tracking-tight italic">Partner <span class="text-accent-cyan">Database</span></h1>
        <p class="text-secondary mt-1">Management of hotels, resorts, and operational partners.</p>
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
            {{ gridResultCount }}
          </span>
        </span>
      </button>
    </div>

    <!-- Data Grid -->
    <div class="flex-1 min-h-0 relative">
      <AppGrid 
        :rowData="filteredItems" 
        :columnDefs="columnDefs" 
        :quickFilterText="currentSearch"
        height="100%" 
        @row-double-clicked="onRowDoubleClicked"
        @filterChanged="(count) => gridResultCount = count"
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
