<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useComplianceStore } from '../store/compliance'
import AppGrid from '../components/ui/AppGrid.vue'
import { ShieldCheck, Plus, RefreshCw, BarChart3, AlertCircle } from 'lucide-vue-next'

import { exportToCSV, printToPDF } from '../utils/exporter'

const complianceStore = useComplianceStore()
const searchQuery = ref('')

const handleExportCSV = () => {
  exportToCSV(complianceStore.entries, 'compliance_audit_history')
}

const columnDefs = [
  { 
    headerName: 'Audit Form', field: 'form.name', sortable: true, filter: true,
    cellRenderer: (params: any) => `
      <div class="flex items-center gap-2">
        <span class="font-bold text-white">${params.value}</span>
      </div>
    `
  },
  {
    headerName: 'Score', field: 'compliance_percent', width: 140,
    cellRenderer: (params: any) => {
      const val = params.value || 0
      const color = val < 50 ? 'text-red-500 bg-red-500/10' : val < 85 ? 'text-orange-400 bg-orange-400/10' : 'text-accent-emerald bg-accent-emerald/10'
      return `
        <div class="flex items-center gap-2">
          <div class="w-12 bg-surface-800 h-1.5 rounded-full overflow-hidden">
            <div class="h-full rounded-full ${val < 50 ? 'bg-red-500' : val < 85 ? 'bg-orange-400' : 'bg-accent-emerald'}" style="width: ${val}%"></div>
          </div>
          <span class="px-2 py-0.5 rounded text-[10px] font-black ${color}">${val.toFixed(1)}%</span>
        </div>
      `
    }
  },
  { headerName: 'Status', field: 'status', width: 100 },
  {
    headerName: '% Improvement', field: 'improvement_percent', width: 140,
    cellRenderer: (params: any) => {
      const val = params.value || 0
      if (!params.data.baseline_id) return `<span class="text-surface-600 text-[10px] font-bold uppercase tracking-widest">—</span>`
      const isPos = val > 0
      const isNeg = val < 0
      const color = isPos ? 'text-accent-emerald bg-accent-emerald/10' : isNeg ? 'text-red-500 bg-red-500/10' : 'text-surface-400 bg-surface-400/10'
      const icon = isPos ? '↑' : isNeg ? '↓' : '→'
      return `
        <div class="flex items-center gap-2">
          <span class="px-2 py-0.5 rounded text-[10px] font-black ${color}">${icon} ${isPos ? '+' : ''}${val.toFixed(1)}%</span>
        </div>
      `
    }
  },
  { 
    headerName: 'Baseline Ref', field: 'baseline_id', width: 120,
    cellRenderer: (params: any) => params.value ? `<span class="text-[10px] font-bold text-accent-cyan flex items-center gap-1"><History class="w-3 h-3"/> LINKED</span>` : `<span class="text-surface-600">—</span>`
  },
  { 
    headerName: 'Audit Date', field: 'created_at', width: 160,
    cellRenderer: (params: any) => `<span class="text-xs text-surface-500">${new Date(params.value).toLocaleDateString()}</span>`
  }
]

onMounted(() => {
  complianceStore.fetchEntries()
})
</script>

<template>
  <div class="space-y-8" v-auto-animate>
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-white tracking-tight italic">Quality & <span class="text-accent-emerald">Compliance</span></h1>
        <p class="text-surface-400 mt-1">Field inspections, HSE audits, and technical compliance monitoring.</p>
      </div>
      <div class="flex items-center gap-3">
        <button @click="handleExportCSV" class="p-3 glass rounded-xl text-surface-400 hover:text-accent-cyan transition-all" title="Export to CSV">
          <BarChart3 class="w-5 h-5" />
        </button>
        <button @click="printToPDF" class="p-3 glass rounded-xl text-surface-400 hover:text-accent-cyan transition-all" title="Print to PDF">
          <RefreshCw class="w-5 h-5" />
        </button>
        <button @click="complianceStore.fetchEntries()" class="p-3 glass rounded-xl text-surface-400 hover:text-accent-emerald transition-all">
          <RefreshCw class="w-5 h-5" :class="{ 'animate-spin': complianceStore.isLoading }" />
        </button>
        <router-link :to="{ name: 'compliance-new' }" class="btn-primary !w-auto px-8 flex items-center justify-center bg-gradient-to-r from-accent-emerald to-emerald-600 border-none shadow-lg shadow-accent-emerald/20">
          New Inspection
        </router-link>
      </div>
    </div>

    <!-- Summary Widgets -->
    <div class="grid grid-cols-4 gap-4">
      <div class="glass-card p-6 border-l-2 border-l-accent-emerald">
        <p class="text-xs font-black text-surface-500 uppercase flex items-center gap-2">
          <ShieldCheck class="w-4 h-4 text-accent-emerald" /> Avg Compliance
        </p>
        <h3 class="text-3xl font-black text-white mt-2 italic">94.2%</h3>
      </div>
      <div class="glass-card p-6 border-l-2 border-l-accent-cyan">
        <p class="text-xs font-black text-surface-500 uppercase flex items-center gap-2">
          <BarChart3 class="w-4 h-4 text-accent-cyan" /> Audits This Month
        </p>
        <h3 class="text-3xl font-black text-white mt-2 italic">128</h3>
      </div>
      <div class="glass-card p-6 border-l-2 border-l-red-500 bg-red-500/5">
        <p class="text-xs font-black text-red-500 uppercase flex items-center gap-2">
          <AlertCircle class="w-4 h-4" /> Violations Detected
        </p>
        <h3 class="text-3xl font-black text-white mt-2 italic">03</h3>
      </div>
       <div class="glass-card p-6 border-l-2 border-l-surface-600">
        <p class="text-xs font-black text-surface-500 uppercase text-surface-600">Reports Pending</p>
        <h3 class="text-3xl font-black text-white mt-2 italic">05</h3>
      </div>
    </div>

    <!-- Search & Filter Tab -->
    <div class="glass-card flex items-center gap-6 py-4">
      <div class="relative flex-1">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-surface-500" />
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Filter audit reports by hotel name, form type, or score..."
          class="w-full bg-surface-900/30 border border-surface-800/50 rounded-xl py-2 pl-10 pr-4 text-sm focus:outline-none focus:border-accent-emerald/50"
        />
      </div>
      <div class="flex items-center gap-3">
        <span class="text-xs text-surface-500 font-black tracking-widest uppercase">Live Global Monitoring</span>
      </div>
    </div>

    <!-- Data Grid -->
    <div class="relative">
      <AppGrid 
        :rowData="complianceStore.entries" 
        :columnDefs="columnDefs" 
        :quickFilterText="searchQuery"
        height="500px" 
      />
      
      <div v-if="complianceStore.isLoading" class="absolute inset-0 glass flex items-center justify-center z-10 rounded-2xl">
        <RefreshCw class="w-10 h-10 text-accent-emerald animate-spin" />
      </div>
    </div>
  </div>
</template>
