<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { usePartnerStore } from '../store/partner'
import { useUIStore } from '../store/ui'
import { storeToRefs } from 'pinia'
import AppGrid from '../components/ui/AppGrid.vue'
import PartnerFormView from './PartnerFormView.vue'
import { RefreshCw } from 'lucide-vue-next'

const uiStore = useUIStore()
const { globalSearch } = storeToRefs(uiStore)
const currentSearch = computed(() => globalSearch.value)

const partnerStore = usePartnerStore()
const isFormOpen = ref(false)
const selectedPartner = ref<any>(null)

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



    <!-- Data Grid -->
    <div class="relative">
      <div v-if="uiStore.globalSearch" class="mb-2 text-xs font-bold text-accent-cyan animate-pulse uppercase tracking-widest">
        FILTERED BY: "{{ uiStore.globalSearch }}"
      </div>
      <AppGrid 
        :rowData="partnerStore.partners" 
        :columnDefs="columnDefs" 
        :quickFilterText="currentSearch"
        height="600px" 
        @row-double-clicked="onRowDoubleClicked"
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
