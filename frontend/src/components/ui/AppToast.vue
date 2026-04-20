<script setup lang="ts">
import { useUIStore } from '../../store/ui'
import { CheckCircle2, AlertCircle, Info, X, AlertTriangle } from 'lucide-vue-next'

const uiStore = useUIStore()

const getIcon = (type: string) => {
  switch (type) {
    case 'success': return CheckCircle2
    case 'error': return AlertCircle
    case 'warning': return AlertTriangle
    default: return Info
  }
}

const getColorClass = (type: string) => {
  switch (type) {
    case 'success': return 'border-accent-emerald text-accent-emerald bg-accent-emerald/10'
    case 'error': return 'border-red-500 text-red-500 bg-red-500/10'
    case 'warning': return 'border-orange-400 text-orange-400 bg-orange-400/10'
    default: return 'border-accent-cyan text-accent-cyan bg-accent-cyan/10'
  }
}
</script>

<template>
  <div class="fixed inset-0 pointer-events-none z-[100] flex items-center justify-center p-6">
    <div class="flex flex-col gap-4 w-full max-w-sm" v-auto-animate>
      <div 
        v-for="toast in uiStore.toasts" 
        :key="toast.id"
        class="pointer-events-auto glass-card border-l-4 shadow-2xl flex items-center gap-4 p-4 animate-in fade-in zoom-in slide-in-from-bottom-4 duration-300"
        :class="getColorClass(toast.type)"
      >
        <component :is="getIcon(toast.type)" class="w-6 h-6 shrink-0" />
        <p class="flex-1 font-bold text-sm text-white">{{ toast.message }}</p>
        <button 
          @click="uiStore.removeToast(toast.id)"
          class="p-1 hover:bg-white/10 rounded transition-colors"
        >
          <X class="w-4 h-4 text-white/50" />
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.glass-card {
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(20px);
}
</style>
