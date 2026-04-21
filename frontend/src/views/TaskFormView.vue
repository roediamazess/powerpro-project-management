<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { X, Save, RefreshCw, AlertCircle, ClipboardList, Clock, Shield } from 'lucide-vue-next'
import { useTaskStore } from '../store/task'
import { useProjectStore } from '../store/project'
import { usePartnerStore } from '../store/partner'
import LookupPopup from '../components/LookupPopup.vue'
import DatePickerPopup from '../components/DatePickerPopup.vue'
import apiClient from '../api/api-client'

const props = defineProps<{
  task?: any
}>()

const emit = defineEmits(['close', 'success'])
const taskStore = useTaskStore()
const projectStore = useProjectStore()
const partnerStore = usePartnerStore()

const currentTab = ref('general')
const users = ref<any[]>([])
const formData = ref({
  description: '',
  project_id: '',
  partner_id: '',
  priority_id: 'MEDIUM',
  status_id: 'OPEN',
  dept_id: 'OPERATIONS',
  assignee_id: '',
  due_date: ''
})

const priorityOptions = [
  { id: 'LOW', name: 'Low Priority' },
  { id: 'MEDIUM', name: 'Medium Priority' },
  { id: 'HIGH', name: 'High / Urgent' }
]

const statusOptions = [
  { id: 'OPEN', name: 'Open Backlog' },
  { id: 'IN_PROGRESS', name: 'In Progress' },
  { id: 'COMPLETED', name: 'Completed' },
  { id: 'CANCELLED', name: 'Cancelled' }
]

const deptOptions = [
  { id: 'OPERATIONS', name: 'Operations' },
  { id: 'IT_TECH', name: 'IT & Technical' },
  { id: 'LOGISTICS', name: 'Logistics' },
  { id: 'ADMIN', name: 'Administration' }
]

onMounted(async () => {
  projectStore.fetchProjects()
  partnerStore.fetchPartners()
  
  try {
    const res = await apiClient.get('/api/v1/users')
    users.value = res.data
  } catch (e) {
    users.value = []
  }

  if (props.task) {
    formData.value = { ...props.task }
  }
})

const isSubmitting = ref(false)
const error = ref('')

const handleSubmit = async () => {
  if (!formData.value.description) {
    error.value = 'Description is required.'
    return
  }

  isSubmitting.value = true
  error.value = ''
  try {
    if (props.task?.task_id) {
      await taskStore.updateTask(props.task.task_id, formData.value)
    } else {
      await taskStore.createTask(formData.value)
    }
    emit('success')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to save task.'
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
              <div class="w-12 h-12 rounded-2xl bg-accent-cyan/10 border border-accent-cyan/20 flex items-center justify-center text-accent-cyan shadow-lg">
                <ClipboardList class="w-7 h-7" />
              </div>
              <div>
                <h2 class="text-2xl font-bold text-primary tracking-tight italic">
                  {{ props.task ? 'Modify Backlog' : 'New Operational Task' }}
                </h2>
                <p class="text-[10px] text-secondary font-black tracking-widest uppercase mt-0.5">Task Module v2.1</p>
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
            <!-- Description Section -->
            <section class="space-y-6">
              <div class="flex items-center gap-4">
                <div class="h-px flex-1 bg-gradient-to-r from-transparent to-border-app"></div>
                <h3 class="text-[10px] font-black text-secondary uppercase tracking-[0.2em]">Objective & Details</h3>
                <div class="h-px flex-1 bg-gradient-to-l from-transparent to-border-app"></div>
              </div>

              <div class="space-y-4">
                <div class="space-y-2">
                  <label class="text-[10px] font-black text-secondary uppercase tracking-widest pl-1">Task Description</label>
                  <textarea v-model="formData.description" rows="3" class="premium-input-field resize-none" placeholder="Enter detailed task objective..."></textarea>
                </div>
              </div>
            </section>

            <!-- Classification Section -->
            <section class="space-y-6">
              <div class="flex items-center gap-4">
                <div class="h-px flex-1 bg-gradient-to-r from-transparent to-surface-800"></div>
                <h3 class="text-[10px] font-black text-surface-500 uppercase tracking-[0.2em]">Classification & Priority</h3>
                <div class="h-px flex-1 bg-gradient-to-l from-transparent to-surface-800"></div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-widest pl-1">Priority</label>
                  <LookupPopup 
                    v-model="formData.priority_id" 
                    :options="priorityOptions" 
                    label="Task Priority"
                  />
                </div>
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-widest pl-1">Status</label>
                  <LookupPopup 
                    v-model="formData.status_id" 
                    :options="statusOptions" 
                    label="Task Status"
                  />
                </div>
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-widest pl-1">Department</label>
                  <LookupPopup 
                    v-model="formData.dept_id" 
                    :options="deptOptions" 
                    label="Department"
                  />
                </div>
              </div>
            </section>

            <!-- Links Section -->
            <section class="space-y-6">
              <div class="flex items-center gap-4">
                <div class="h-px flex-1 bg-gradient-to-r from-transparent to-surface-800"></div>
                <h3 class="text-[10px] font-black text-surface-500 uppercase tracking-[0.2em]">Context & Ownership</h3>
                <div class="h-px flex-1 bg-gradient-to-l from-transparent to-surface-800"></div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-widest pl-1">Linked Project</label>
                  <LookupPopup 
                    v-model="formData.project_id" 
                    :options="[{id: '', name: 'No Linked Project'}, ...projectStore.projects.map(p => ({id: p.project_id, name: p.name}))]" 
                    label="Linked Project"
                  />
                </div>
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-widest pl-1">Assignee</label>
                  <LookupPopup 
                    v-model="formData.assignee_id" 
                    :options="[{id: '', name: 'Unassigned'}, ...users.map(u => ({id: u.user_id, name: u.fullname}))]" 
                    label="Field Assignee"
                  />
                </div>
                <div class="space-y-2">
                  <label class="text-xs font-bold text-surface-400 uppercase tracking-widest flex items-center gap-2">
                    <Clock class="w-3 h-3" /> Due Date
                  </label>
                  <DatePickerPopup 
                    v-model="formData.due_date" 
                    label="Due Date"
                  />
                </div>
              </div>
            </section>
          </div>
        </div>

        <!-- Footer Action Bar (RIGHT ALIGNED) -->
        <div class="p-8 border-t border-border-app bg-surface-500/5 flex flex-row gap-4 items-center justify-end">
          <button @click="handleSubmit" :disabled="isSubmitting" class="w-auto px-12 h-14 btn-primary bg-gradient-to-r from-accent-emerald to-accent-cyan shadow-xl shadow-accent-emerald/20 flex items-center justify-center gap-3 active:scale-95 transition-all">
            <Save v-if="!isSubmitting" class="w-5 h-5" />
            <RefreshCw v-else class="w-5 h-5 animate-spin" />
            <span class="text-sm font-bold uppercase tracking-widest">
              {{ props.task ? 'Save' : 'Create' }}
            </span>
          </button>

          <button @click="emit('close')" class="w-auto px-12 h-14 glass text-primary text-sm font-bold rounded-2xl hover:bg-surface-500/5 border border-border-app transition-all uppercase tracking-widest">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

