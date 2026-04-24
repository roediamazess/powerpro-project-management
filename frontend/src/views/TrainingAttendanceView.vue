<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { CheckCircle, AlertCircle, Loader2, User, Building2, Briefcase } from 'lucide-vue-next'
import apiClient from '../api/api-client'

const route = useRoute()
const sessionId = route.params.id as string

const session = ref<any>(null)
const isLoading = ref(true)
const isSubmitting = ref(false)
const isSuccess = ref(false)
const errorMsg = ref('')

const formData = ref({
  fullname: '',
  department: '',
  position: ''
})

onMounted(async () => {
  try {
    const res = await apiClient.get(`/training/session/${sessionId}`)
    session.value = res.data
    
    // Check if already submitted (Fingerprint via LocalStorage)
    const submitted = localStorage.getItem(`training_sub_${sessionId}`)
    if (submitted) {
      isSuccess.value = true
    }
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || 'Training session not found or expired.'
  } finally {
    isLoading.value = false
  }
})

const submitAttendance = async () => {
  if (!formData.value.fullname) return
  
  isSubmitting.value = true
  errorMsg.value = ''
  
  try {
    // Basic fingerprint: simple random ID if not exists
    let deviceId = localStorage.getItem('pp_device_id')
    if (!deviceId) {
      deviceId = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15)
      localStorage.setItem('pp_device_id', deviceId)
    }

    await apiClient.post('/training/submit', {
      ...formData.value,
      session_id: sessionId,
      device_id: deviceId
    })
    
    localStorage.setItem(`training_sub_${sessionId}`, 'true')
    isSuccess.value = true
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || 'Failed to submit attendance.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-[#020617] text-white flex flex-col items-center justify-center p-6 relative overflow-hidden">
    <!-- Background Glows -->
    <div class="absolute -top-40 -left-40 w-96 h-96 bg-accent-cyan/10 rounded-full blur-[120px] pointer-events-none"></div>
    <div class="absolute -bottom-40 -right-40 w-96 h-96 bg-accent-emerald/10 rounded-full blur-[120px] pointer-events-none"></div>

    <!-- Background Logo Watermark -->
    <div class="absolute inset-0 flex items-center justify-center opacity-[0.03] pointer-events-none">
      <img src="/logo_qr.svg" alt="Watermark" class="w-[120%] max-w-none grayscale rotate-[-15deg]" />
    </div>

    <div class="w-full max-w-md glass-card p-8 relative z-10 border border-white/5 shadow-2xl rounded-[32px]">
      <div v-if="isLoading" class="flex flex-col items-center justify-center py-12 gap-4">
        <Loader2 class="w-12 h-12 text-accent-cyan animate-spin" />
        <p class="text-secondary font-bold tracking-widest uppercase text-xs">Memuat Sesi Training...</p>
      </div>

      <div v-else-if="errorMsg && !isSuccess" class="text-center py-8">
        <div class="w-20 h-20 bg-red-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
          <AlertCircle class="w-10 h-10 text-red-400" />
        </div>
        <h2 class="text-2xl font-bold mb-4">Sesi Tidak Tersedia</h2>
        <p class="text-secondary text-sm mb-8 leading-relaxed">{{ errorMsg }}</p>
        <button @click="window.location.reload()" class="btn-secondary w-full">Coba Lagi</button>
      </div>

      <div v-else-if="isSuccess" class="text-center py-8">
        <div class="w-20 h-20 bg-accent-emerald/10 rounded-full flex items-center justify-center mx-auto mb-6">
          <CheckCircle class="w-10 h-10 text-accent-emerald" />
        </div>
        <h2 class="text-2xl font-bold mb-2">Terima Kasih!</h2>
        <p class="text-secondary text-sm mb-6">Absensi Anda telah berhasil tercatat untuk sesi training ini.</p>
        
        <div class="p-4 rounded-2xl bg-white/5 border border-white/5 text-left mb-6">
          <p class="text-[10px] text-surface-500 uppercase font-black tracking-widest mb-1">Materi Training</p>
          <p class="text-sm font-bold text-accent-cyan">{{ session?.topic }}</p>
        </div>
        
        <p class="text-[10px] text-surface-500 italic">PowerPro Operational Record System</p>
      </div>

      <div v-else>
        <div class="mb-8 text-center">
          <div class="w-24 h-24 flex items-center justify-center mx-auto mb-6 p-2">
            <img src="/logo_qr.svg" alt="PowerPro Logo" class="w-full h-full object-contain drop-shadow-xl" />
          </div>
          <h1 class="text-2xl font-bold italic">Training <span class="text-accent-cyan">Attendance</span></h1>
          <p class="text-secondary text-[10px] uppercase tracking-[0.3em] mt-2 font-black border-t border-white/5 pt-2 inline-block">{{ session?.partner_name }}</p>
        </div>

        <div class="space-y-6">
          <div class="p-4 rounded-2xl bg-accent-emerald/5 border border-accent-emerald/10 mb-6">
            <p class="text-[10px] text-accent-emerald uppercase font-black tracking-widest mb-1">Topik Training</p>
            <p class="text-sm font-bold">{{ session?.topic }}</p>
          </div>

          <div class="space-y-4">
            <div class="space-y-1.5">
              <label class="text-[10px] font-black text-secondary uppercase tracking-widest ml-1">Nama Lengkap</label>
              <div class="relative">
                <User class="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-surface-500" />
                <input 
                  v-model="formData.fullname"
                  type="text" 
                  placeholder="Masukkan nama Anda..."
                  class="w-full bg-surface-500/5 border border-white/10 rounded-2xl py-3.5 pl-12 pr-4 text-sm focus:outline-none focus:border-accent-cyan/50 focus:bg-surface-900 transition-all"
                />
              </div>
            </div>

            <div class="space-y-2">
              <label class="text-[10px] font-black text-white/40 uppercase tracking-[0.2em] ml-1">Departemen</label>
              <div class="relative group">
                <Building2 class="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-white/20 group-focus-within:text-accent-cyan transition-colors pointer-events-none" />
                <select 
                  v-model="formData.department"
                  class="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-sm text-white focus:outline-none focus:border-accent-cyan/50 focus:bg-white/[0.08] transition-all appearance-none cursor-pointer"
                  required
                >
                  <option value="" disabled selected class="bg-surface-900 text-white/40">Pilih Departemen...</option>
                  <option value="Food & Beverage" class="bg-surface-900 text-white">Food & Beverage</option>
                  <option value="Kitchen" class="bg-surface-900 text-white">Kitchen</option>
                  <option value="Spa & Wellness" class="bg-surface-900 text-white">Spa & Wellness</option>
                  <option value="Front Office" class="bg-surface-900 text-white">Front Office</option>
                  <option value="Housekeeping" class="bg-surface-900 text-white">Housekeeping</option>
                  <option value="Engineering" class="bg-surface-900 text-white">Engineering</option>
                  <option value="Sales & Marketing" class="bg-surface-900 text-white">Sales & Marketing</option>
                  <option value="IT / EDP" class="bg-surface-900 text-white">IT / EDP</option>
                  <option value="Accounting" class="bg-surface-900 text-white">Accounting</option>
                  <option value="Executive Office" class="bg-surface-900 text-white">Executive Office</option>
                  <option value="Human Resources" class="bg-surface-900 text-white">Human Resources</option>
                  <option value="Others" class="bg-surface-900 text-white">Others</option>
                </select>
                <!-- Custom Arrow -->
                <div class="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-white/20 group-focus-within:text-accent-cyan">
                  <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20"><path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" /></svg>
                </div>
              </div>
            </div>

            <div class="space-y-1.5">
              <label class="text-[10px] font-black text-secondary uppercase tracking-widest ml-1">Jabatan</label>
              <div class="relative">
                <Briefcase class="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-surface-500" />
                <input 
                  v-model="formData.position"
                  type="text" 
                  placeholder="Misal: Manager, Staff..."
                  class="w-full bg-surface-500/5 border border-white/10 rounded-2xl py-3.5 pl-12 pr-4 text-sm focus:outline-none focus:border-accent-cyan/50 focus:bg-surface-900 transition-all"
                />
              </div>
            </div>
          </div>

          <button 
            @click="submitAttendance"
            :disabled="!formData.fullname || isSubmitting"
            class="btn-primary w-full py-4 mt-4 flex items-center justify-center gap-3 bg-gradient-to-r from-accent-cyan to-accent-emerald border-none shadow-lg shadow-accent-cyan/20 active:scale-95 transition-all disabled:opacity-50"
          >
            <Loader2 v-if="isSubmitting" class="w-5 h-5 animate-spin" />
            <span v-else class="font-bold tracking-widest uppercase text-xs">Submit Absensi</span>
          </button>
        </div>
      </div>
    </div>
    
    <p class="mt-8 text-[10px] text-surface-600 font-black tracking-widest uppercase">Powered by PowerPro AI System</p>
  </div>
</template>

<style scoped>
.glass-card {
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(40px);
}
</style>
