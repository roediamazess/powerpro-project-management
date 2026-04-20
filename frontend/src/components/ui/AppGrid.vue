<script setup lang="ts">
import { AgGridVue } from 'ag-grid-vue3'
import { 
  ModuleRegistry, 
  ClientSideRowModelModule, 
  RowAutoHeightModule,
  TextFilterModule,
  NumberFilterModule,
  QuickFilterModule,
  RowSelectionModule,
  ValidationModule 
} from 'ag-grid-community'

ModuleRegistry.registerModules([
  ClientSideRowModelModule, 
  RowAutoHeightModule,
  TextFilterModule,
  NumberFilterModule,
  QuickFilterModule,
  RowSelectionModule,
  ValidationModule
])

import { useUIStore } from '../../store/ui'
import { ref, watch } from 'vue'

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
const emit = defineEmits(['rowClicked', 'rowDoubleClicked'])

const gridTheme = 'ag-theme-alpine'

const defaultColDef = {
  sortable: true,
  filter: true,
  resizable: true,
  flex: 1,
  wrapText: true,
  autoHeight: true,
}

const gridApi = ref<any>(null)

const onGridReady = (params: any) => {
  gridApi.value = params.api
  if (props.quickFilterText) {
    gridApi.value.setGridOption('quickFilterText', props.quickFilterText)
  }
}

watch(() => props.quickFilterText, (newVal) => {
  if (gridApi.value) {
    gridApi.value.setGridOption('quickFilterText', newVal ?? '')
  }
}, { immediate: false })

const onRowClicked = (params: any) => {
  // Deselect all, then select clicked row
  params.api.deselectAll()
  params.node.setSelected(true)
  emit('rowClicked', params)
}

const onRowDoubleClicked = (params: any) => {
  emit('rowDoubleClicked', params)
}
</script>

<template>
  <div class="w-full flex flex-col gap-1" :style="{ height: props.height }">
    <div v-if="props.quickFilterText" class="text-[10px] font-bold text-accent-cyan uppercase tracking-widest px-1 pb-1">
      Searching: "{{ props.quickFilterText }}"
    </div>
    <div 
      :class="[gridTheme, uiStore.theme]"
      class="flex-1 rounded-2xl overflow-hidden border border-surface-200 dark:border-surface-800/50 dark:bg-surface-900"
    >
      <ag-grid-vue
        class="h-full w-full"
        :rowData="props.rowData"
        :columnDefs="props.columnDefs"
        :defaultColDef="defaultColDef"
        :animateRows="true"
        :suppressCellFocus="true"
        rowSelection="single"
        @grid-ready="onGridReady"
        @row-clicked="onRowClicked"
        @row-double-clicked="onRowDoubleClicked"
      />
    </div>
  </div>
</template>

<style>
/* ===== LIGHT MODE BASE ===== */
.ag-theme-alpine {
  --ag-background-color: #ffffff !important;
  --ag-header-background-color: #f8fafc;
  --ag-header-foreground-color: #64748b;
  --ag-foreground-color: #1e293b;
  --ag-border-color: #e2e8f0;
  --ag-row-hover-color: #e0f2fe;
  --ag-selected-row-background-color: #bfdbfe;
  --ag-odd-row-background-color: #fafafa;
  --ag-range-selection-border-color: transparent;
  --ag-header-column-separator-display: block;
  --ag-header-column-separator-height: 60%;
  --ag-header-column-separator-width: 1px;
  --ag-header-column-separator-color: #cbd5e1;
}

/* ===== DARK MODE BASE ===== */
.dark.ag-theme-alpine {
  --ag-background-color: #0f172a !important;
  --ag-header-background-color: #0f1f3d !important;
  --ag-header-foreground-color: #e2e8f0 !important;
  --ag-foreground-color: #f1f5f9;
  --ag-border-color: #1e293b;
  --ag-row-hover-color: #1e3a5f;
  --ag-selected-row-background-color: #1d4ed8;
  --ag-odd-row-background-color: #111827;
  --ag-control-panel-background-color: #0f172a;
  --ag-range-selection-border-color: transparent;
  --ag-header-column-separator-color: rgba(99,182,255,0.15);
  --ag-header-column-resize-handle-color: rgba(99,182,255,0.3);
}

/* ===== DARK MODE ELEMENT OVERRIDES ===== */
.dark.ag-theme-alpine .ag-root-wrapper,
.dark.ag-theme-alpine .ag-header-viewport,
.dark.ag-theme-alpine .ag-body-viewport {
  background-color: #0f172a !important;
}

/* Row default bg — NO !important so ag-row-selected can win */
.dark.ag-theme-alpine .ag-row:not(.ag-row-selected):not(.ag-row-hover) {
  background-color: #0f172a;
}

.dark.ag-theme-alpine .ag-row {
  color: #f1f5f9 !important;
}

/* ===== SELECTED ROW — LIGHT ===== */
.ag-theme-alpine .ag-row-selected .ag-cell {
  background-color: #bfdbfe !important;
}

/* ===== SELECTED ROW — DARK ===== */
.dark.ag-theme-alpine .ag-row-selected {
  background-color: #1e3a5f !important;
}
.dark.ag-theme-alpine .ag-row-selected .ag-cell {
  background-color: #1e3a5f !important;
  color: #f1f5f9 !important;
}

/* ===== HOVER ROW — DARK ===== */
.dark.ag-theme-alpine .ag-row-hover:not(.ag-row-selected) {
  background-color: #162033 !important;
}
.dark.ag-theme-alpine .ag-row-hover:not(.ag-row-selected) .ag-cell {
  background-color: #162033 !important;
}

/* ===== HEADER ===== */
.dark.ag-theme-alpine .ag-header {
  background-color: #0f1f3d !important;
  border-bottom: 2px solid rgba(6, 182, 212, 0.3) !important;
}

.ag-theme-alpine .ag-header-cell-text,
.dark.ag-theme-alpine .ag-header-cell-text {
  font-weight: 700 !important;
  font-size: 11px !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
}

.dark.ag-theme-alpine .ag-header-cell-text {
  color: #e2e8f0 !important;
}

.dark.ag-theme-alpine .ag-icon {
  color: #64748b !important;
}

/* ===== REMOVE CELL FOCUS BLACK BOX ===== */
.ag-theme-alpine .ag-cell-focus,
.dark.ag-theme-alpine .ag-cell-focus {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

/* ===== ROW TRANSITION ===== */
.ag-theme-alpine .ag-row,
.dark.ag-theme-alpine .ag-row {
  transition: background-color 0.15s ease;
}

/* ===== MISC ===== */
.ag-root-wrapper { border: none !important; }

/* ===== VERTICAL COLUMN SEPARATORS ===== */
.ag-theme-alpine .ag-cell { border-right: 1px solid #e2e8f0 !important; }
.ag-theme-alpine .ag-header-cell { border-right: 1px solid #cbd5e1 !important; }
.dark.ag-theme-alpine .ag-cell { border-right: 1px solid rgba(30, 41, 59, 0.9) !important; }
.dark.ag-theme-alpine .ag-header-cell { border-right: 1px solid rgba(99, 182, 255, 0.12) !important; }

/* ===== FILTER POPUP ===== */
.ag-popup-editor, .ag-menu, .ag-filter-wrapper {
  background-color: var(--bg-card) !important;
  backdrop-filter: blur(16px) !important;
  border: 1px solid var(--border-app) !important;
  border-radius: 20px !important;
  box-shadow: 0 20px 50px rgba(0,0,0,0.3) !important;
  padding: 12px !important;
}

.ag-filter-body-wrapper { padding: 8px 0 !important; }

.ag-filter-wrapper input {
  padding-left: 36px !important;
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

.dark .ag-filter-wrapper input { color: white !important; }
</style>
