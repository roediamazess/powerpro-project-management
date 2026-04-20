<script setup lang="ts">
import { AgGridVue } from 'ag-grid-vue3'
import { 
  ModuleRegistry, 
  ClientSideRowModelModule, 
  RowAutoHeightModule,
  TextFilterModule,
  NumberFilterModule,
  ValidationModule 
} from 'ag-grid-community'

ModuleRegistry.registerModules([
  ClientSideRowModelModule, 
  RowAutoHeightModule,
  TextFilterModule,
  NumberFilterModule,
  ValidationModule
])

import { useUIStore } from '../../store/ui'
import { computed } from 'vue'

interface Props {
  rowData: any[]
  columnDefs: any[]
  height?: string
  quickFilterText?: string
}

const props = withDefaults(defineProps<Props>(), {
  height: '500px',
  quickFilterText: ''
})

const uiStore = useUIStore()
const emit = defineEmits(['rowClicked', 'rowDoubleClicked', 'cellClicked'])

const onRowClicked = (params: any) => emit('rowClicked', params)
const onRowDoubleClicked = (params: any) => emit('rowDoubleClicked', params)
const onCellClicked = (params: any) => emit('cellClicked', params)

const gridTheme = 'ag-theme-alpine' // We use the same base theme and override variables via CSS

const defaultColDef = {
  sortable: true,
  filter: true,
  resizable: true,
  flex: 1,
}
</script>

<template>
  <div :class="[gridTheme, uiStore.theme, 'w-full rounded-2xl overflow-hidden border border-surface-200 dark:border-surface-800/50 dark:bg-surface-900']" :style="{ height: props.height }">
    <ag-grid-vue
      class="h-full w-full"
      :rowData="props.rowData"
      :columnDefs="props.columnDefs"
      :defaultColDef="defaultColDef"
      :quickFilterText="props.quickFilterText"
      :animateRows="true"
      :rowHeight="64"
      @row-clicked="onRowClicked"
      @row-double-clicked="onRowDoubleClicked"
      @cell-clicked="onCellClicked"
    />
  </div>
</template>

<style>
/* Base Grid Styling (Light Mode) */
.ag-theme-alpine {
  --ag-background-color: #ffffff !important;
  --ag-header-background-color: #f8fafc;
  --ag-header-foreground-color: #64748b;
  --ag-foreground-color: #1e293b;
  --ag-border-color: #e2e8f0;
  --ag-row-hover-color: #f1f5f9;
  --ag-selected-row-background-color: #f1f5f9;
  --ag-odd-row-background-color: #fafafa;
}

/* Dark Mode Overrides */
.dark.ag-theme-alpine {
  --ag-background-color: #0f172a !important; 
  --ag-header-background-color: #1e293b;
  --ag-header-foreground-color: #94a3b8;
  --ag-foreground-color: #f1f5f9;
  --ag-border-color: #1e293b;
  --ag-row-hover-color: #1e293b;
  --ag-selected-row-background-color: #1e293b;
  --ag-odd-row-background-color: #111827;
  --ag-control-panel-background-color: #0f172a;
}

.dark.ag-theme-alpine .ag-root-wrapper,
.dark.ag-theme-alpine .ag-header-viewport,
.dark.ag-theme-alpine .ag-body-viewport,
.dark.ag-theme-alpine .ag-row,
.dark.ag-theme-alpine .ag-cell {
  background-color: #0f172a !important;
  color: #f1f5f9 !important;
}

.dark.ag-theme-alpine .ag-header {
  background-color: #1e293b !important;
}

.ag-root-wrapper {
  border: none !important;
}

/* AG Grid Filter/Popup Customization */
.ag-popup-editor, .ag-menu, .ag-filter-wrapper {
  background-color: var(--bg-card) !important;
  backdrop-filter: blur(16px) !important;
  border: 1px solid var(--border-app) !important;
  border-radius: 20px !important;
  box-shadow: 0 20px 50px rgba(0,0,0,0.3) !important;
  padding: 12px !important;
}

.ag-filter-body-wrapper {
  padding: 8px 0 !important;
}

/* Fix for the overlapping search icon and placeholder */
.ag-filter-wrapper input {
  padding-left: 36px !important; /* Move only the text to the right */
  width: 100% !important;
  background-color: rgba(255, 255, 255, 0.03) !important;
  border: 1px solid var(--border-app) !important;
  border-radius: 12px !important;
  height: 42px !important;
  transition: all 0.2s ease !important;
  box-sizing: border-box !important;
}

.ag-filter-wrapper input:focus {
  border-color: var(--color-accent-emerald) !important;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.1) !important;
  outline: none !important;
}

.dark .ag-filter-wrapper input {
  color: white !important;
}
</style>
