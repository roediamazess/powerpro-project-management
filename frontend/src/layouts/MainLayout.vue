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

const navItems = [
  { name: 'Dashboard', icon: LayoutDashboard, to: { name: 'dashboard' } },
  { name: 'Partners', icon: Hotel, to: { name: 'partners' } },
  { name: 'Projects', icon: Layers, to: { name: 'projects' } },
  { name: 'Backlog Tasks', icon: Briefcase, to: { name: 'tasks' } },
  { name: 'Timeboxing', icon: Clock, to: { name: 'timeboxing' } },
  { name: 'Compliance', icon: ShieldCheck, to: { name: 'compliance' } },
]

const handleLogout = async () => {
  await authStore.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="h-screen flex overflow-hidden">
    <!-- Sidebar -->
    <aside 
      class="w-64 glass border-r border-border-app flex flex-col z-20 transition-all duration-300"
      :class="{ 'w-20': !sidebarOpen }"
    >
      <div class="p-6 flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-accent-cyan to-accent-emerald shadow-lg shadow-accent-emerald/30 flex items-center justify-center">
          <span class="font-bold text-white">P</span>
        </div>
        <span v-if="sidebarOpen" class="font-bold text-xl tracking-tight italic">Power<span class="text-accent-emerald">Pro</span></span>
      </div>

      <nav v-auto-animate class="flex-1 px-4 space-y-2 mt-4">
        <router-link 
          v-for="item in navItems" 
          :key="item.name"
          :to="item.to"
          class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group hover:bg-accent-emerald/5"
          active-class="bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20 shadow-inner"
        >
          <component :is="item.icon" class="w-5 h-5 group-hover:scale-110 transition-transform" />
          <span v-if="sidebarOpen" class="font-medium">{{ item.name }}</span>
        </router-link>
        
        <div class="pt-4 border-t border-border-app my-4"></div>

        <router-link :to="{ name: 'settings' }" class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group hover:bg-white/5" active-class="bg-accent-cyan/10 text-accent-cyan border border-accent-cyan/20 shadow-inner">
          <Settings class="w-5 h-5 group-hover:scale-110 transition-transform" />
          <span v-if="sidebarOpen" class="font-medium">System Settings</span>
        </router-link>
      </nav>

      <div class="p-4 border-t border-border-app">
        <button @click="handleLogout" class="flex items-center gap-3 px-4 py-3 w-full rounded-xl hover:bg-red-500/10 text-surface-400 hover:text-red-400 transition-all">
          <LogOut class="w-5 h-5" />
          <span v-if="sidebarOpen" class="font-medium">Sign Out</span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col min-w-0 transition-colors duration-300 overflow-hidden">
      <!-- Header -->
      <header class="h-16 glass sticky top-0 z-10 px-8 flex items-center justify-between border-b border-border-app">
        <div class="flex items-center gap-4 flex-1">
          <div class="relative w-96 max-w-md">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-surface-500" />
            <input 
              :value="uiStore.globalSearch"
              @input="uiStore.setGlobalSearch(($event.target as HTMLInputElement).value)"
              type="text" 
              placeholder="Search data..."
              class="w-full bg-surface-500/5 border border-border-app rounded-full py-2 pl-10 pr-4 text-sm focus:outline-none focus:border-accent-emerald/50 focus:ring-1 focus:ring-accent-emerald/50 transition-all"
            />
          </div>
        </div>

        <div class="flex items-center gap-6">
          <button 
            @click="uiStore.toggleTheme"
            class="p-2 rounded-xl hover:bg-surface-500/10 text-surface-500 transition-all hover:scale-110 active:scale-95"
            title="Toggle Theme"
          >
            <Sun v-if="uiStore.theme === 'dark'" class="w-5 h-5" />
            <Moon v-else class="w-5 h-5" />
          </button>

          <button class="relative text-surface-500 hover:text-accent-emerald transition-colors">
            <Bell class="w-5 h-5" />
            <span class="absolute -top-1 -right-1 w-2 h-2 bg-accent-emerald rounded-full"></span>
          </button>
          
          <div class="flex items-center gap-3 pl-6 border-l border-border-app">
            <div class="text-right">
              <p class="text-sm font-bold">{{ authStore.user?.fullname || 'User' }}</p>
              <p class="text-[10px] font-black text-accent-emerald uppercase tracking-widest">{{ authStore.user?.role_id }}</p>
            </div>
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-accent-cyan/10 to-accent-emerald/10 border border-accent-emerald/20 flex items-center justify-center text-xs font-bold text-accent-emerald shadow-lg">
              {{ (authStore.user?.fullname || 'U').charAt(0) }}
            </div>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <div class="flex-1 overflow-auto p-8">
        <router-view />
      </div>
    </main>
  </div>
</template>
