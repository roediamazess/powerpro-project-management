<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useTaskStore } from '../store/task'
import TaskFormView from './TaskFormView.vue'
import { CheckCircle2, Circle, Clock, AlertTriangle, Plus, Search, Filter } from 'lucide-vue-next'

const taskStore = useTaskStore()
const isFormOpen = ref(false)
const selectedTask = ref<any>(null)
const searchQuery = ref('')

onMounted(() => {
  taskStore.fetchTasks()
})

const openAddForm = () => {
  selectedTask.value = null
  isFormOpen.value = true
}

const handleFormSuccess = () => {
  isFormOpen.value = false
  taskStore.fetchTasks()
}

const getPriorityColor = (id: string) => {
  const colors: any = { HIGH: 'text-red-400', MEDIUM: 'text-orange-400', LOW: 'text-accent-cyan' }
  return colors[id] || 'text-surface-500'
}
</script>

<template>
  <div class="space-y-8" v-auto-animate>
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-primary tracking-tight italic">Operations <span class="text-accent-cyan">Backlog</span></h1>
        <p class="text-secondary mt-1">Management of specific tasks and deliverables across all projects.</p>
      </div>
      <button @click="openAddForm" class="btn-primary flex items-center gap-2 bg-gradient-to-r from-accent-emerald to-accent-cyan border-none shadow-lg shadow-accent-cyan/10">
        <Plus class="w-5 h-5" />
        New Task
      </button>
    </div>

    <!-- Filters -->
    <div class="glass-card flex items-center gap-4 py-3">
      <div class="relative flex-1 group">
        <div class="absolute left-4 top-1/2 -translate-y-1/2 flex items-center pointer-events-none z-10">
          <Search class="w-4 h-4 text-secondary group-focus-within:text-accent-cyan transition-colors" />
        </div>
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="Filter tasks by description or project..."
          class="w-full bg-surface-500/5 border border-border-app rounded-xl py-2 pr-4 text-sm text-primary outline-none focus:border-accent-cyan/50 focus:bg-card transition-all shadow-inner"
          style="padding-left: 3.5rem !important;"
        />
      </div>
      <button class="px-4 py-2 glass rounded-lg text-xs font-bold flex items-center gap-2 text-secondary hover:text-primary transition-all">
        <Filter class="w-4 h-4" /> ALL DEPARTMENTS
      </button>
    </div>

    <!-- Task List -->
    <div class="grid grid-cols-1 gap-3">
      <div v-for="task in taskStore.tasks" :key="task.task_id" class="glass-card flex items-center gap-6 group hover:border-accent-cyan/30 transition-all">
        <button class="text-surface-600 hover:text-accent-emerald transition-colors">
          <Circle v-if="task.status_id !== 'COMPLETED'" class="w-6 h-6" />
          <CheckCircle2 v-else class="w-6 h-6 text-accent-emerald" />
        </button>

        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-3">
            <h3 class="font-bold text-primary truncate group-hover:text-accent-cyan transition-colors">{{ task.description }}</h3>
            <span v-if="task.priority_id === 'HIGH'" class="flex items-center gap-1 text-[10px] font-black bg-red-500/10 text-red-500 px-2 py-0.5 rounded border border-red-500/20">
              <AlertTriangle class="w-3 h-3" /> URGENT
            </span>
          </div>
          <div class="flex items-center gap-4 mt-1">
            <span class="text-xs text-secondary flex items-center gap-1">
              <span class="w-2 h-2 rounded-full bg-accent-cyan/40"></span> 
              {{ task.project?.name || 'Unassigned' }}
            </span>
            <span class="text-xs text-surface-600 flex items-center gap-1">
              <Clock class="w-3 h-3" /> {{ task.due_date ? new Date(task.due_date).toLocaleDateString() : 'No due date' }}
            </span>
          </div>
        </div>

        <div class="flex items-center gap-4 px-4 border-l border-surface-800/50">
           <div class="text-right">
             <p class="text-[10px] font-bold text-surface-500 uppercase tracking-tighter">Priority</p>
             <p class="text-xs font-black italic" :class="getPriorityColor(task.priority_id)">{{ task.priority_id }}</p>
           </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="taskStore.tasks.length === 0 && !taskStore.isLoading" class="py-20 text-center glass-card border-dashed">
        <p class="text-surface-500">No active tasks found in the backlog.</p>
      </div>
    </div>

    <!-- Modal Form Integration -->
    <TaskFormView
      v-if="isFormOpen"
      :task="selectedTask"
      @close="isFormOpen = false"
      @success="handleFormSuccess"
    />
  </div>
</template>
