<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { X, Plus, QrCode, FileText, Trash2, Loader2, Download, ExternalLink, Calendar, Clock, Users } from 'lucide-vue-next'
import QrcodeVue from 'qrcode.vue'
import apiClient from '../api/api-client'
import { useUIStore } from '../store/ui'

const props = defineProps<{
  projectId: string
  projectName: string
}>()

const emit = defineEmits(['close'])
const uiStore = useUIStore()

const sessions = ref<any[]>([])
const isLoading = ref(true)
const isCreating = ref(false)
const showQR = ref<string | null>(null)

const newSession = ref({
  topic: '',
  trainer_name: ''
})

const fetchSessions = async () => {
  isLoading.value = true
  try {
    const res = await apiClient.get(`/training/list/${props.projectId}`)
    sessions.value = res.data
  } catch (err) {
    uiStore.showToast('Failed to fetch training sessions', 'error')
  } finally {
    isLoading.value = false
  }
}

const createSession = async () => {
  if (!newSession.value.topic) return
  isCreating.value = true
  try {
    const res = await apiClient.post('/training/', {
      ...newSession.value,
      project_id: props.projectId
    })
    const sessionId = res.data.session_id
    newSession.value = { topic: '', trainer_name: '' }
    await fetchSessions()
    uiStore.showToast('Training session created successfully', 'success')
    
    // Auto show QR after creation
    showQR.value = sessionId
  } catch (err) {
    uiStore.showToast('Failed to create session', 'error')
  } finally {
    isCreating.value = false
  }
}

const exportPDF = async (sessionId: string) => {
  try {
    const res = await apiClient.get(`/training/export/${sessionId}`, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `Attendance_${props.projectName.replace(/\s+/g, '_')}.pdf`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (err) {
    uiStore.showToast('Failed to export PDF', 'error')
  }
}

const getPublicUrl = (sessionId: string) => {
  const host = window.location.origin
  return `${host}/t/${sessionId}`
}

onMounted(fetchSessions)
</script>

<template>
  <div class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6">
    <div class="absolute inset-0 bg-surface-950/80 backdrop-blur-md" @click="emit('close')"></div>
    
    <div class="relative w-full max-w-4xl bg-surface-900 border border-white/10 rounded-[32px] shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
      <!-- Header -->
      <div class="px-8 py-6 border-b border-white/5 flex items-center justify-between bg-white/[0.02]">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 rounded-2xl bg-accent-cyan/10 flex items-center justify-center text-accent-cyan border border-accent-cyan/20">
            <QrCode class="w-6 h-6" />
          </div>
          <div>
            <h2 class="text-xl font-bold text-white italic">Training <span class="text-accent-cyan">Management</span></h2>
            <p class="text-[10px] text-surface-400 uppercase font-black tracking-widest">{{ props.projectName }}</p>
          </div>
        </div>
        <button @click="emit('close')" class="p-2 rounded-xl hover:bg-white/5 text-surface-400 transition-colors">
          <X class="w-6 h-6" />
        </button>
      </div>

      <div class="flex-1 overflow-hidden flex flex-col md:flex-row">
        <!-- Sidebar: Create New -->
        <div class="w-full md:w-80 border-r border-white/5 p-6 bg-white/[0.01]">
          <h3 class="text-xs font-black text-secondary uppercase tracking-widest mb-6 flex items-center gap-2">
            <Plus class="w-3 h-3" /> New Session
          </h3>
          
          <div class="space-y-4">
            <div class="space-y-1.5">
              <label class="text-[10px] font-black text-surface-500 uppercase tracking-widest ml-1">Training Topic</label>
              <input 
                v-model="newSession.topic"
                type="text" 
                placeholder="e.g. Front Office Ops"
                class="w-full bg-surface-500/5 border border-white/10 rounded-xl py-2.5 px-4 text-xs focus:outline-none focus:border-accent-cyan/50 transition-all"
              />
            </div>
            
            <div class="space-y-1.5">
              <label class="text-[10px] font-black text-surface-500 uppercase tracking-widest ml-1">Trainer Name</label>
              <input 
                v-model="newSession.trainer_name"
                type="text" 
                placeholder="e.g. John Doe"
                class="w-full bg-surface-500/5 border border-white/10 rounded-xl py-2.5 px-4 text-xs focus:outline-none focus:border-accent-cyan/50 transition-all"
              />
            </div>

            <button 
              @click="createSession"
              :disabled="!newSession.topic || isCreating"
              class="btn-primary w-full py-3 flex items-center justify-center gap-2 bg-gradient-to-r from-accent-cyan to-accent-emerald border-none shadow-lg shadow-accent-cyan/20 active:scale-95 transition-all disabled:opacity-50 mt-4"
            >
              <Loader2 v-if="isCreating" class="w-4 h-4 animate-spin" />
              <span class="font-bold tracking-widest uppercase text-[10px]">Generate Session</span>
            </button>
          </div>

          <div class="mt-8 p-4 rounded-2xl bg-accent-cyan/5 border border-accent-cyan/10">
            <p class="text-[10px] text-accent-cyan font-bold leading-relaxed italic">
              "Generating a session will create a unique QR code valid for 24 hours for participants to scan."
            </p>
          </div>
        </div>

        <!-- Main Content: Session List -->
        <div class="flex-1 flex flex-col p-6 overflow-hidden">
          <h3 class="text-xs font-black text-secondary uppercase tracking-widest mb-6">Recent Sessions</h3>
          
          <div v-if="isLoading" class="flex-1 flex items-center justify-center">
            <Loader2 class="w-8 h-8 text-accent-cyan animate-spin" />
          </div>

          <div v-else-if="sessions.length === 0" class="flex-1 flex flex-col items-center justify-center text-surface-500">
            <Calendar class="w-12 h-12 mb-4 opacity-20" />
            <p class="text-sm font-medium italic">No training sessions found for this project.</p>
          </div>

          <div v-else class="flex-1 overflow-y-auto custom-scrollbar space-y-4 pr-2">
            <div v-for="session in sessions" :key="session.session_id" class="p-5 rounded-2xl bg-white/[0.02] border border-white/5 hover:bg-white/[0.04] transition-all group relative overflow-hidden">
              <div class="flex items-center justify-between relative z-10">
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-3 mb-1">
                    <h4 class="font-bold text-white group-hover:text-accent-cyan transition-colors truncate">{{ session.topic }}</h4>
                    <span class="px-2 py-0.5 rounded-md bg-accent-cyan/10 text-accent-cyan text-[9px] font-black uppercase tracking-tighter border border-accent-cyan/20">
                      {{ session.trainer_name || 'No Trainer' }}
                    </span>
                  </div>
                  <div class="flex items-center gap-4 text-[10px] text-surface-500 font-bold uppercase tracking-widest">
                    <span class="flex items-center gap-1.5"><Calendar class="w-3 h-3 text-accent-cyan" /> {{ new Date(session.created_at).toLocaleDateString('id-ID', { day: '2-digit', month: 'short', year: 'numeric' }) }}</span>
                    <span class="flex items-center gap-1.5"><Clock class="w-3 h-3 text-accent-cyan" /> {{ new Date(session.created_at).toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }) }}</span>
                    <span class="flex items-center gap-1.5" :class="new Date() > new Date(session.expires_at) ? 'text-red-400' : 'text-accent-emerald'">
                      <div class="w-1.5 h-1.5 rounded-full" :class="new Date() > new Date(session.expires_at) ? 'bg-red-400' : 'bg-accent-emerald animate-pulse'"></div>
                      {{ new Date() > new Date(session.expires_at) ? 'EXPIRED' : 'ACTIVE' }}
                    </span>
                  </div>
                </div>

                <div class="flex items-center gap-2">
                  <button @click="showQR = session.session_id" class="p-2.5 rounded-xl bg-accent-cyan/10 text-accent-cyan hover:bg-accent-cyan/20 transition-all shadow-lg shadow-accent-cyan/5" title="Show QR Code">
                    <QrCode class="w-4 h-4" />
                  </button>
                  <button @click="exportPDF(session.session_id)" class="p-2.5 rounded-xl bg-white/5 text-white hover:bg-white/10 transition-all border border-white/5" title="Export PDF">
                    <FileText class="w-4 h-4" />
                  </button>
                  <a :href="getPublicUrl(session.session_id)" target="_blank" class="p-2.5 rounded-xl bg-white/5 text-white hover:bg-white/10 transition-all border border-white/5" title="Open Public Link">
                    <ExternalLink class="w-4 h-4" />
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- QR Code Modal Overlay -->
    <transition enter-active-class="transition duration-300 ease-out" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100" leave-active-class="transition duration-200 ease-in" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
      <div v-if="showQR" class="fixed inset-0 z-[110] flex items-center justify-center p-6">
        <div class="absolute inset-0 bg-surface-950/90 backdrop-blur-xl" @click="showQR = null"></div>
        <div class="relative w-full max-w-sm bg-white p-8 rounded-[40px] flex flex-col items-center text-surface-950 shadow-[0_0_100px_rgba(8,146,134,0.3)]">
          <h4 class="text-sm font-black uppercase tracking-[0.3em] mb-8 text-surface-400">Scan to Attend</h4>
          
          <div class="relative p-2 bg-white rounded-[44px] border-[8px] border-accent-cyan/5 mb-8 shadow-2xl overflow-hidden group">
            <!-- Branded Background Logo -->
            <div class="absolute inset-0 flex items-center justify-center opacity-90 p-4">
              <img src="/logo_qr.svg" alt="QR Background" class="w-full h-full object-contain rounded-[32px]" />
            </div>
            
            <!-- Glass Overlay for QR Contrast -->
            <div class="absolute inset-0 bg-white/20 backdrop-blur-[2px]"></div>

            <!-- QR Dots Overlaid -->
            <div class="relative z-10">
              <qrcode-vue 
                :value="getPublicUrl(showQR)" 
                :size="260" 
                level="Q" 
                render-as="canvas"
                foreground="#020617" 
                background="rgba(255,255,255,0)"
              />
            </div>
          </div>
          
          <p class="text-[10px] font-bold text-center text-surface-400 uppercase tracking-widest mb-8 leading-relaxed">
            Please share this QR with the participants.<br/>This link is active for 24 hours.
          </p>
          
          <button @click="showQR = null" class="w-full py-4 bg-surface-950 text-white rounded-2xl font-black text-xs uppercase tracking-widest active:scale-95 transition-all">
            Close QR Code
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.1);
}
</style>
