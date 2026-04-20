<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { Lock, Mail, ShieldCheck, Loader2, ArrowRight, Activity, Wifi, Sun, Moon } from 'lucide-vue-next'
import { useUIStore } from '../store/ui'

const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUIStore()

const username = ref('')
const password = ref('')
const error = ref('')
const isSubmitting = ref(false)
const uptime = ref('99.98%')

// Pulse animation for uptime
onMounted(() => {
  setInterval(() => {
    const random = Math.random()
    if (random > 0.95) {
      uptime.value = (99.9 + (Math.random() * 0.09)).toFixed(2) + '%'
    }
  }, 3000)
})

const handleLogin = async () => {
  if (!username.value || !password.value) return
  
  isSubmitting.value = true
  error.value = ''
  
  try {
    const formData = new FormData()
    formData.append('username', username.value)
    formData.append('password', password.value)
    
    await authStore.login(formData)
    router.push({ name: 'dashboard' })
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'System authentication failed. Verify credentials.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex flex-col items-center justify-center p-6 relative overflow-hidden transition-colors duration-500 selection:bg-accent-emerald/30">
    <!-- Premium Mesh Background -->
    <div class="mesh-blob mesh-1"></div>
    <div class="mesh-blob mesh-2"></div>
    <div class="mesh-blob mesh-3"></div>

    <!-- Top Status Bar -->
    <div class="fixed top-6 left-0 right-0 px-6 flex justify-between items-center z-50 pointer-events-auto">
      <div class="flex items-center gap-3 bg-surface-500/5 backdrop-blur-xl px-4 py-2 rounded-full border border-border-app opacity-40 hover:opacity-100 transition-opacity">
        <Activity class="w-4 h-4 text-accent-emerald animate-pulse" />
        <span class="text-[10px] font-mono tracking-widest text-surface-500 uppercase">System Integrity: Nominal</span>
      </div>

      <div class="flex items-center gap-2">
        <div class="hidden md:flex items-center gap-3 bg-surface-500/5 backdrop-blur-xl px-4 py-2 rounded-full border border-border-app opacity-40">
          <Wifi class="w-4 h-4 text-accent-cyan" />
          <span class="text-[10px] font-mono tracking-widest text-surface-500 uppercase">SLA Uptime: {{ uptime }}</span>
        </div>
        
        <button 
          @click="uiStore.toggleTheme"
          class="p-2.5 rounded-full bg-surface-500/5 backdrop-blur-xl border border-border-app text-surface-500 hover:text-accent-emerald transition-all hover:scale-110 active:scale-95"
          title="Toggle Theme"
        >
          <Sun v-if="uiStore.theme === 'dark'" class="w-4 h-4" />
          <Moon v-else class="w-4 h-4" />
        </button>
      </div>
    </div>

    <div v-auto-animate class="w-full max-w-[440px] relative z-10">
      <!-- High-End Branding -->
      <div class="text-center mb-12">
        <div class="inline-flex items-center justify-center p-4 rounded-3xl bg-surface-500/5 border border-border-app shadow-2xl glow-emerald mb-8 group transition-all duration-500 hover:scale-110">
          <ShieldCheck class="w-12 h-12 text-accent-emerald group-hover:text-accent-cyan transition-colors duration-500" />
        </div>
        <h1 class="text-5xl font-bold tracking-tighter mb-3">
          Power<span class="text-gradient">Pro</span>
        </h1>
        <p class="text-surface-500 font-medium tracking-[0.2em] text-[11px] uppercase">
          Autonomous Operational Intelligence
        </p>
      </div>

      <!-- Login Panel -->
      <div class="glass-card">
        <div class="flex items-center gap-3 mb-10">
          <div class="w-1.5 h-6 bg-accent-emerald rounded-full"></div>
          <h2 class="text-2xl font-semibold tracking-tight">Login Credentials</h2>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-8">
          <!-- Email Field -->
          <div class="input-group">
            <Mail class="input-icon" />
            <input 
              v-model="username"
              type="text" 
              id="username"
              placeholder=" "
              class="premium-input"
              required
            />
            <label for="username" class="input-label">Professional Email Address</label>
          </div>

          <!-- Password Field -->
          <div class="input-group">
            <Lock class="input-icon" />
            <input 
              v-model="password"
              type="password" 
              id="password"
              placeholder=" "
              class="premium-input"
              required
            />
            <label for="password" class="input-label">Security Protocol Key</label>
          </div>

          <!-- Error Alert -->
          <Transition
            enter-active-class="transition duration-300 ease-out"
            enter-from-class="transform -translate-y-2 opacity-0"
            enter-to-class="transform translate-y-0 opacity-100"
            leave-active-class="transition duration-200 ease-in"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
          >
            <div v-if="error" class="bg-red-500/5 border border-red-500/20 rounded-2xl p-4 flex items-center gap-3 text-red-400 text-sm">
              <span class="flex-1">{{ error }}</span>
            </div>
          </Transition>

          <button 
            type="submit" 
            :disabled="isSubmitting"
            class="btn-primary"
          >
            <div v-if="isSubmitting" class="flex items-center justify-center gap-2">
              <Loader2 class="w-5 h-5 animate-spin" />
              <span>Verifying Token...</span>
            </div>
            <div v-else class="flex items-center justify-center gap-2">
              <span>Authorize Session</span>
              <ArrowRight class="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </div>
          </button>
        </form>

        <div class="mt-12 text-center pt-8 border-t border-border-app">
          <p class="text-[10px] font-medium tracking-widest text-surface-500 uppercase leading-relaxed">
            Authorized Audit Loop Active <br/>
            <span class="text-surface-400">Protected by PowerPro Security Layer v4.0.2</span>
          </p>
        </div>
      </div>

      <!-- Footer Help -->
      <div class="mt-8 text-center">
        <button class="text-xs text-surface-600 hover:text-accent-cyan transition-colors font-medium">
          Request System Access Elevation
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Scoped styles for micro-animations */
input:focus {
  @apply shadow-[0_0_20px_rgba(16,185,129,0.05)];
}
</style>
