<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { X, Save, RefreshCw, AlertCircle, Clock, Calendar, CheckCircle2 } from 'lucide-vue-next'
import { useTimeboxStore } from '../store/timebox'
import { useProjectStore } from '../store/project'
import { useTaskStore } from '../store/task'
import { useAuthStore } from '../store/auth'
import LookupPopup from '../components/LookupPopup.vue'

const props = defineProps<{
  timebox?: any
}>()

const emit = defineEmits(['close', 'success'])
const timeboxStore = useTimeboxStore()
const projectStore = useProjectStore()
const taskStore = useTaskStore()
const authStore = useAuthStore()

const formData = ref({
  activity_name: '',
  description: '',
  user_id: authStore.user?.user_id || '',
  start_time: '',
  end_time: '',
  project_id: '',
  task_id: '',
  color_code: 'cyan',
  is_completed: false
})

onMounted(() => {
  projectStore.fetchProjects()
  taskStore.fetchTasks()

  if (props.timebox) {
    formData.value = { ...props.timebox }
  }
})

const isSubmitting = ref(false)
const error = ref('')

const handleSubmit = async () => {
  if (!formData.value.activity_name || !formData.value.start_time || !formData.value.end_time) {
    error.value = 'Activity name and schedule are required.'
    return
  }

  isSubmitting.value = true
  error.value = ''
  try {
    if (props.timebox?.timebox_id) {
      await timeboxStore.updateTimebox(props.timebox.timebox_id, formData.value)
    } else {
      await timeboxStore.createTimebox(formData.value)
    }
    emit('success')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to sync schedule.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-[80] flex items-center justify-center p-4 sm:p-6 overflow-hidden">
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-surface-950/40 backdrop-blur-md" @click="emit('close')"></div>

      <!-- Panel -->
      <div v-auto-animate class="relative w-full max-w-4xl max-h-[90vh] glass border border-white/10 shadow-2xl flex flex-col rounded-[32px] overflow-hidden animate-in fade-in zoom-in duration-300">
        <!-- Header -->
        <div class="p-8 border-b border-border-app bg-surface-500/5 flex flex-col gap-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 rounded-2xl bg-accent-emerald/10 border border-accent-emerald/20 flex items-center justify-center text-accent-emerald shadow-lg">
                <Calendar class="w-7 h-7" />
              </div>
              <div>
                <h2 class="text-2xl font-bold text-primary tracking-tight italic">
                  {{ props.timebox ? 'Modify Schedule' : 'Allocate Focus Block' }}
                </h2>
                <p class="text-[10px] text-secondary font-black tracking-widest uppercase mt-0.5">Timeboxing Module v2.1</p>
              </div>
            </div>
            <button @click="emit('close')" class="p-2 hover:bg-surface-500/10 rounded-xl text-secondary transition-all">
              <X class="w-6 h-6" />
            </button>
          </div>
        </div>

        <!-- Content -->
        <div v-auto-animate class="flex-1 overflow-y-auto p-8 custom-scrollbar">
          <div v-if="error" class="bg-red-500/10 border border-red-500/20 p-4 rounded-xl text-red-400 text-sm mb-6 flex items-center gap-3">
            <AlertCircle class="w-5 h-5 flex-shrink-0" />
            {{ error }}
          </div>

          <div class="space-y-10">
            <!-- Primary Details -->
            <section class="space-y-6">
              <div class="flex items-center gap-4">
                <div class="h-px flex-1 bg-gradient-to-r from-transparent to-surface-800"></div>
                <h3 class="text-[10px] font-black text-surface-500 uppercase tracking-[0.2em]">Activity Definition</h3>
                <div class="h-px flex-1 bg-gradient-to-l from-transparent to-surface-800"></div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="space-y-2 md:col-span-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-widest pl-1">Activity Name</label>
                  <input v-model="formData.activity_name" type="text" class="w-full bg-surface-900/50 border border-white/5 rounded-2xl py-4 px-5 text-white focus:border-accent-emerald/50 focus:bg-surface-900 outline-none transition-all" placeholder="e.g. Deep Work: Database Optimization">
                </div>
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-widest pl-1">Color Category</label>
                  <div class="flex items-center gap-3 p-1 animate-in slide-in-from-left duration-500">
                    <button @click="formData.color_code = 'cyan'" class="w-10 h-10 rounded-full bg-accent-cyan border-4 transition-all" :class="formData.color_code === 'cyan' ? 'border-white/40 scale-110 shadow-lg shadow-accent-cyan/20' : 'border-transparent opacity-40 hover:opacity-100'"></button>
                    <button @click="formData.color_code = 'emerald'" class="w-10 h-10 rounded-full bg-accent-emerald border-4 transition-all" :class="formData.color_code === 'emerald' ? 'border-white/40 scale-110 shadow-lg shadow-accent-emerald/20' : 'border-transparent opacity-40 hover:opacity-100'"></button>
                    <button @click="formData.color_code = 'orange'" class="w-10 h-10 rounded-full bg-orange-400 border-4 transition-all" :class="formData.color_code === 'orange' ? 'border-white/40 scale-110 shadow-lg shadow-orange-400/20' : 'border-transparent opacity-40 hover:opacity-100'"></button>
                  </div>
                </div>
                <div class="flex items-end gap-3 pb-2">
                  <button @click="formData.is_completed = !formData.is_completed" class="flex items-center gap-2 group cursor-pointer">
                    <div class="w-6 h-6 rounded-lg border-2 border-surface-700 flex items-center justify-center transition-all" :class="formData.is_completed ? 'bg-accent-emerald border-accent-emerald shadow-lg shadow-accent-emerald/20' : 'group-hover:border-accent-emerald/50'">
                      <CheckCircle2 v-if="formData.is_completed" class="w-4 h-4 text-surface-950" />
                    </div>
                    <span class="text-sm font-bold transition-all" :class="formData.is_completed ? 'text-accent-emerald' : 'text-surface-500 group-hover:text-surface-300'">Mark as Finalized</span>
                  </button>
                </div>
              </div>
            </section>

            <!-- Timeline Section -->
            <section class="space-y-6">
              <div class="flex items-center gap-4">
                <div class="h-px flex-1 bg-gradient-to-r from-transparent to-surface-800"></div>
                <h3 class="text-[10px] font-black text-surface-500 uppercase tracking-[0.2em]">Execution Period</h3>
                <div class="h-px flex-1 bg-gradient-to-l from-transparent to-surface-800"></div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-widest pl-1 flex items-center gap-2">
                    <Clock class="w-3 h-3" /> Start Timestamp
                  </label>
                  <input v-model="formData.start_time" type="datetime-local" class="w-full bg-surface-900/50 border border-white/5 rounded-2xl py-4 px-5 text-white outline-none focus:border-accent-emerald/50 transition-all">
                </div>
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-widest pl-1 flex items-center gap-2">
                    <Clock class="w-3 h-3" /> End Timestamp
                  </label>
                  <input v-model="formData.end_time" type="datetime-local" class="w-full bg-surface-900/50 border border-white/5 rounded-2xl py-4 px-5 text-white outline-none focus:border-accent-emerald/50 transition-all">
                </div>
              </div>
            </section>

             <!-- Linkage Section -->
            <section class="space-y-6">
              <div class="flex items-center gap-4">
                <div class="h-px flex-1 bg-gradient-to-r from-transparent to-surface-800"></div>
                <h3 class="text-[10px] font-black text-surface-500 uppercase tracking-[0.2em]">Strategic Context</h3>
                <div class="h-px flex-1 bg-gradient-to-l from-transparent to-surface-800"></div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-widest pl-1">Link to Project</label>
                  <LookupPopup 
                    v-model="formData.project_id" 
                    :options="[{id: '', name: 'Miscellaneous / Internal'}, ...projectStore.projects.map(p => ({id: p.project_id, name: p.name}))]" 
                    label="Linked Project"
                  />
                </div>
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-widest pl-1">Link to Backlog Task</label>
                  <LookupPopup 
                    v-model="formData.task_id" 
                    :options="[{id: '', name: 'No Linked Task'}, ...taskStore.tasks.map(t => ({id: t.task_id, name: t.description}))]" 
                    label="Linked Backlog Task"
                  />
                </div>
              </div>
            </section>
          </div>
        </div>

        <!-- Footer Action Bar (RIGHT ALIGNED) -->
        <div class="p-8 border-t border-white/5 bg-surface-950/40 flex flex-row gap-4 items-center justify-end">
          <button @click="handleSubmit" :disabled="isSubmitting" class="w-auto px-12 h-14 btn-primary bg-gradient-to-r from-accent-emerald to-accent-cyan shadow-xl shadow-accent-emerald/20 flex items-center justify-center gap-3 active:scale-95 transition-all">
            <Save v-if="!isSubmitting" class="w-5 h-5" />
            <RefreshCw v-else class="w-5 h-5 animate-spin" />
            <span class="text-sm font-bold uppercase tracking-widest">
              {{ props.timebox ? 'Commit' : 'Schedule' }}
            </span>
          </button>

          <button @click="emit('close')" class="w-auto px-12 h-14 glass text-white text-sm font-bold rounded-2xl hover:bg-white/5 border border-white/10 hover:border-white/20 transition-all uppercase tracking-widest">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

