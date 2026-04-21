<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useTimeboxStore } from '../store/timebox'
import type { Timebox } from '../store/timebox'
import TimeboxFormView from './TimeboxFormView.vue'
import { useAuthStore } from '../store/auth'
import { 
  Clock, Plus, ChevronLeft, ChevronRight, 
  User, GripVertical 
} from 'lucide-vue-next'

const timeboxStore = useTimeboxStore()
const authStore = useAuthStore()

// State for Modal
const isFormOpen = ref(false)
const selectedTimebox = ref<any>(null)

// State for Manager visibility
const selectedUserId = ref('')
const users = ref<any[]>([
  { user_id: '1', fullname: 'Field Officer A', role: 'OFFICER' },
  { user_id: '2', fullname: 'Field Officer B', role: 'OFFICER' }
])

const isManager = computed(() => ['ADMIN', 'MANAGER'].includes(authStore.user?.role_id || ''))

onMounted(() => {
  timeboxStore.fetchTimeboxes()
})

const openAddForm = () => {
  selectedTimebox.value = null
  isFormOpen.value = true
}

const handleFormSuccess = () => {
  isFormOpen.value = false
  timeboxStore.fetchTimeboxes(selectedUserId.value || undefined)
}

const isViewingOthers = computed(() => !!selectedUserId.value && selectedUserId.value !== authStore.user?.user_id)

const switchUser = (id: string) => {
  selectedUserId.value = id
  timeboxStore.fetchTimeboxes(id)
}

// Calendar Logic
const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
const timeSlots = Array.from({ length: 10 }, (_, i) => `${8 + i}:00`)

// Drag and Drop State
const draggingBlock = ref<Timebox | null>(null)

const onDragStart = (box: Timebox) => {
  if (isViewingOthers.value) return
  draggingBlock.value = box
}

const onDrop = (day: string, slot: string) => {
  if (!draggingBlock.value || isViewingOthers.value) return
  
  // Logical update: Move block to new day/time
  console.log(`Moving ${draggingBlock.value.activity_name} to ${day} ${slot}`)
  // Here we would calculate new start/end times and call timeboxStore.updateTimebox
  
  draggingBlock.value = null
}
</script>

<template>
  <div class="space-y-8" v-auto-animate>
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-white tracking-tight italic">
          <span v-if="isViewingOthers">{{ users.find(u => u.user_id === selectedUserId)?.fullname }}'s</span>
          <span v-else>Personal</span>
          <span class="text-accent-emerald ml-2">Timeboxing</span>
        </h1>
        <p class="text-surface-400 mt-1">
          <span v-if="isViewingOthers">Monitoring team availability and schedule allocation.</span>
          <span v-else>Schedule your deep work blocks and allocate time for specific tasks.</span>
        </p>
      </div>

      <div class="flex items-center gap-4">
        <!-- Manager User Selector -->
        <div v-if="isManager" class="flex items-center gap-3 glass border border-border-app rounded-xl px-4 py-2 ring-1 ring-accent-emerald/20">
          <User class="w-4 h-4 text-accent-emerald" />
          <select 
            @change="(e) => switchUser((e.target as HTMLSelectElement).value)"
            class="bg-transparent text-sm font-bold text-primary outline-none cursor-pointer"
          >
            <option value="">My Calendar</option>
            <option v-for="u in users" :key="u.user_id" :value="u.user_id">{{ u.fullname }}</option>
          </select>
        </div>

        <div class="flex items-center gap-1 glass border border-border-app rounded-xl p-1 shadow-inner">
          <button class="p-2 hover:bg-surface-500/10 rounded-lg text-secondary transition-colors"><ChevronLeft class="w-4 h-4" /></button>
          <span class="px-4 text-xs font-black text-primary tracking-widest">APR 19 - 25</span>
          <button class="p-2 hover:bg-surface-500/10 rounded-lg text-secondary transition-colors"><ChevronRight class="w-4 h-4" /></button>
        </div>
        <button @click="openAddForm" v-if="!isViewingOthers" class="btn-primary !w-auto px-8 flex items-center justify-center bg-gradient-to-r from-accent-cyan to-accent-emerald border-none shadow-lg shadow-accent-emerald/10">
          Schedule Task
        </button>
      </div>
    </div>

    <!-- Interactive Grid -->
    <div class="glass-card shadow-2xl p-0 overflow-hidden group/calendar">
      <!-- Grid Header -->
      <div class="grid grid-cols-[100px_repeat(5,1fr)] border-b border-border-app" :style="{ backgroundColor: 'var(--bg-card)' }">
        <div class="p-4 border-r border-border-app"></div>
        <div v-for="day in days" :key="day" class="p-4 text-center border-r border-border-app last:border-r-0">
          <p class="text-[10px] font-black text-secondary uppercase tracking-[0.2em] mb-1">Weekday</p>
          <p class="text-sm font-bold text-primary">{{ day }}</p>
        </div>
      </div>

      <!-- Time Slots Grid -->
      <div class="grid grid-cols-[100px_repeat(5,1fr)] h-[700px] relative">
        <!-- Time Labels -->
        <div class="border-r border-border-app" :style="{ backgroundColor: 'var(--bg-card)' }">
          <div v-for="slot in timeSlots" :key="slot" class="h-[70px] flex items-center justify-center border-b border-border-app last:border-0 relative">
            <span class="text-[10px] font-black text-secondary tracking-tighter">{{ slot }}</span>
            <div class="absolute -right-1 top-0 w-2 h-2 rounded-full bg-border-app translate-x-1/2"></div>
          </div>
        </div>

        <!-- Working Area -->
        <div 
          v-for="day in days" :key="day" 
          class="relative border-r border-border-app last:border-r-0"
          @dragover.prevent
          @drop="onDrop(day, 'dynamic-slot')"
        >
          <!-- Grid Lines -->
          <div v-for="slot in timeSlots" :key="slot" class="h-[70px] border-b border-border-app last:border-0 hover:bg-accent-emerald/[0.03] transition-colors"></div>

          <!-- Dynamic Blocks (Mock data integrated into interactive UI) -->
          <div 
            v-if="day === 'Monday'"
            draggable="true"
            @dragstart="onDragStart({ activity_name: 'Server Infra Audit', user_id: '1', start_time: new Date(), end_time: new Date(), partner_id: '1' } as any)"
            class="absolute inset-x-2 top-[70px] h-[140px] z-10 p-4 rounded-2xl bg-gradient-to-br from-accent-cyan/20 to-accent-cyan/5 border border-accent-cyan/30 shadow-xl shadow-accent-cyan/5 group/block cursor-grab active:cursor-grabbing transform hover:scale-[1.02] transition-all"
          >
            <div class="flex items-center justify-between mb-2">
              <span class="px-2 py-0.5 rounded-full bg-accent-cyan/20 text-accent-cyan text-[8px] font-black tracking-widest uppercase ring-1 ring-accent-cyan/30">Strategic</span>
              <GripVertical class="w-3 h-3 text-accent-cyan/40 opacity-0 group-hover/block:opacity-100 transition-opacity" />
            </div>
            <h4 class="font-bold text-white leading-tight">Server Infra Audit - Phase 1</h4>
            <div class="flex items-center gap-2 mt-3 text-[10px] text-surface-500 font-medium">
               <Clock class="w-3 h-3" /> 09:00 - 11:00
            </div>
            
            <div class="absolute -bottom-1 -right-1 w-2 h-2 bg-accent-cyan rounded-full animate-ping"></div>
          </div>

           <div 
            v-if="day === 'Wednesday'"
            draggable="true"
            class="absolute inset-x-2 top-[210px] h-[70px] z-10 p-4 rounded-2xl bg-gradient-to-br from-accent-emerald/20 to-accent-emerald/5 border border-accent-emerald/30 shadow-xl shadow-accent-emerald/5 group/block cursor-grab active:cursor-grabbing transform hover:scale-[1.02] transition-all"
          >
            <div class="flex items-center justify-between mb-1">
              <span class="px-2 py-0.5 rounded-full bg-accent-emerald/20 text-accent-emerald text-[8px] font-black tracking-widest uppercase">Routine</span>
            </div>
            <h4 class="font-bold text-white leading-tight truncate">Sync Manager</h4>
          </div>
        </div>
      </div>
    </div>

    <!-- Tooltip / Legend -->
    <div class="flex items-center justify-between px-6 py-4 glass-card border border-white/5 bg-white/[0.02]">
      <div class="flex items-center gap-8">
        <div class="flex items-center gap-2">
          <div class="w-3 h-3 rounded-full bg-accent-cyan shadow-lg shadow-accent-cyan/40"></div>
          <span class="text-xs font-bold text-surface-400 uppercase tracking-widest">High Focus Block</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-3 h-3 rounded-full bg-accent-emerald shadow-lg shadow-accent-emerald/40"></div>
          <span class="text-xs font-bold text-surface-400 uppercase tracking-widest">Normal Task Block</span>
        </div>
        <div class="flex items-center gap-2 opacity-50">
          <div class="w-3 h-3 rounded-full bg-orange-400"></div>
          <span class="text-xs font-bold text-surface-400 uppercase tracking-widest">Conflict Detected</span>
        </div>
      </div>
      <p class="text-[10px] text-secondary font-bold italic">Drag blocks to reschedule. All changes are logged to Audit System.</p>
    </div>

    <!-- Modal Form Integration -->
    <TimeboxFormView
      v-if="isFormOpen"
      :timebox="selectedTimebox"
      @close="isFormOpen = false"
      @success="handleFormSuccess"
    />
  </div>
</template>

<style scoped>
.glass-card:hover ::-webkit-scrollbar-thumb {
  background: rgba(16, 185, 129, 0.2);
}
</style>
