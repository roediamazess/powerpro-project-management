<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'
import { 
  LayoutDashboard, 
  Settings, 
  LogOut,
  Bell,
  Search,
  Hotel,
  Layers,
  Clock,
  ShieldCheck,
  Briefcase,
  Sun,
  Moon
} from 'lucide-vue-next'
import { useUIStore } from '../store/ui'

const uiStore = useUIStore()
const sidebarOpen = ref(true)
const authStore = useAuthStore()
const router = useRouter()
const isProfileMenuOpen = ref(false)

const navItems = [
  { name: 'Dashboard', icon: LayoutDashboard, to: { name: 'dashboard' } },
  { name: 'Partners', icon: Hotel, to: { name: 'partners' } },
  { name: 'Projects', icon: Layers, to: { name: 'projects' } },
  { name: 'Backlog Tasks', icon: Briefcase, to: { name: 'tasks' } },
  { name: 'Timeboxing', icon: Clock, to: { name: 'timeboxing' } },
  { name: 'Compliance', icon: ShieldCheck, to: { name: 'compliance' } },
  { name: 'System Settings', icon: Settings, to: { name: 'settings' } },
]

const handleLogout = async () => {
  await authStore.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="h-screen bg-bg-app flex flex-col relative overflow-hidden transition-colors duration-500">
    
    <!-- Floating Dynamic Dock (Option B) -->
    <nav class="fixed top-6 inset-x-0 mx-auto w-[96%] max-w-7xl glass rounded-full px-6 py-3 flex items-center justify-between z-50 shadow-[0_20px_50px_rgba(8,_146,_134,_0.05)] border border-white/5 backdrop-blur-xl transition-all duration-300">
      
      <!-- Brand Logo (Left) -->
      <div class="flex items-center h-10 w-auto">
        <img src="../assets/logo.svg" alt="PowerPro Logo" class="h-8 md:h-10 w-auto object-contain drop-shadow-lg hover:scale-105 transition-transform cursor-pointer" />
      </div>

      <!-- Center Navigation Links -->
      <div class="flex items-center gap-2 xl:gap-3 absolute left-1/2 -translate-x-1/2">
        <router-link 
          v-for="item in navItems" 
          :key="item.name"
          :to="item.to"
          class="flex flex-col items-center justify-center gap-1 px-4 py-2 rounded-2xl transition-all duration-200 group hover:bg-white/5"
          active-class="bg-accent-emerald/10 text-accent-emerald ring-1 ring-accent-emerald/20 shadow-inner"
        >
          <component :is="item.icon" class="w-5 h-5 opacity-70 group-hover:scale-110 group-hover:opacity-100 transition-all" />
          <span class="font-black text-[9px] uppercase tracking-widest whitespace-nowrap opacity-80 group-hover:opacity-100 transition-all">{{ item.name }}</span>
        </router-link>
      </div>

      <!-- Utilities & Profile (Right) -->
      <div class="flex items-center gap-4">

        <button 
          @click="uiStore.toggleTheme"
          class="p-2 rounded-full hover:bg-surface-500/10 text-surface-400 hover:text-accent-cyan transition-all hover:scale-110 active:scale-95"
          title="Toggle Theme"
        >
          <Sun v-if="uiStore.theme === 'dark'" class="w-4 h-4" />
          <Moon v-else class="w-4 h-4" />
        </button>

        <button class="relative p-2 rounded-full hover:bg-surface-500/10 text-surface-400 hover:text-accent-emerald transition-all hover:scale-110">
          <Bell class="w-4 h-4" />
          <span class="absolute top-1 right-1 w-2 h-2 bg-accent-emerald rounded-full border border-surface-950"></span>
        </button>
        
        <!-- Profile Dropdown System -->
        <div v-if="isProfileMenuOpen" @click="isProfileMenuOpen = false" class="fixed inset-0 z-40 bg-transparent"></div>
        <div class="relative z-50">
          
          <!-- Profile Pill (Trigger) -->
          <div @click="isProfileMenuOpen = !isProfileMenuOpen" class="flex items-center gap-3 pl-3 pr-2 py-1.5 rounded-full glass border cursor-pointer transition-all group" :class="isProfileMenuOpen ? 'border-accent-emerald/50 bg-accent-emerald/10 shadow-[0_0_15px_rgba(16,185,129,0.15)]' : 'border-white/5 hover:border-accent-emerald/40 hover:bg-accent-emerald/5'">
            <div class="text-right hidden sm:block">
              <p class="text-xs font-bold transition-colors" :class="isProfileMenuOpen ? 'text-accent-emerald' : 'text-primary group-hover:text-accent-emerald'">{{ authStore.user?.fullname?.split(' ')[0] || 'User' }}</p>
              <p class="text-[9px] font-black text-surface-400 uppercase tracking-widest">{{ authStore.user?.role_id }}</p>
            </div>
            <div class="w-8 h-8 rounded-full bg-gradient-to-br from-accent-cyan/20 to-accent-emerald/20 border border-accent-emerald/20 flex items-center justify-center text-xs font-bold text-accent-emerald shadow-lg group-hover:scale-105 transition-transform">
              {{ (authStore.user?.fullname || 'U').charAt(0) }}
            </div>
          </div>
          
          <!-- Dropdown Menu -->
          <transition 
            enter-active-class="transition duration-200 ease-out" 
            enter-from-class="transform scale-95 opacity-0 -translate-y-2" 
            enter-to-class="transform scale-100 opacity-100 translate-y-0" 
            leave-active-class="transition duration-75 ease-in" 
            leave-from-class="transform scale-100 opacity-100 translate-y-0" 
            leave-to-class="transform scale-95 opacity-0 -translate-y-2"
          >
            <div v-if="isProfileMenuOpen" class="absolute right-0 mt-3 w-56 rounded-2xl glass border border-white/10 shadow-2xl bg-surface-900/90 backdrop-blur-2xl overflow-hidden py-1">
              <div class="px-4 py-3 border-b border-white/5">
                <p class="text-sm font-bold text-primary">{{ authStore.user?.fullname || 'System User' }}</p>
                <p class="text-[10px] font-medium text-surface-400">{{ authStore.user?.email || 'admin@powerpro.com' }}</p>
              </div>
              <div class="py-1">
                <button @click="router.push({name: 'settings'}); isProfileMenuOpen = false" class="w-full flex items-center gap-3 px-4 py-2.5 text-xs font-bold text-surface-300 hover:text-accent-cyan hover:bg-surface-500/10 transition-colors">
                  <Settings class="w-4 h-4 opacity-70" />
                  System Settings
                </button>
                <button @click="handleLogout" class="w-full flex items-center gap-3 px-4 py-2.5 text-xs font-bold text-red-400 hover:text-red-300 hover:bg-red-500/10 transition-colors">
                  <LogOut class="w-4 h-4 opacity-70" />
                  Sign Out
                </button>
              </div>
            </div>
          </transition>
        </div>
      </div>

    </nav>

    <!-- Content Workspace -->
    <main class="flex-1 flex flex-col w-full max-w-[1400px] mx-auto pt-[104px] pb-6 px-4 sm:px-6 lg:px-8 overflow-hidden relative z-10 transition-colors duration-300">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

  </div>
</template>
