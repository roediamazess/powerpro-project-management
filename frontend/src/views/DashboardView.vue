<script setup lang="ts">
import { Plus, TrendingUp, Clock, AlertCircle } from 'lucide-vue-next'

const stats = [
  { name: 'Active Projects', value: '12', trend: '+2', icon: TrendingUp, color: 'text-accent-emerald' },
  { name: 'Tasks Due Today', value: '08', trend: '-1', icon: Clock, color: 'text-orange-400' },
  { name: 'Compliance Alerts', value: '02', trend: '0', icon: AlertCircle, color: 'text-red-400' },
]
</script>

<template>
  <div class="space-y-8">
    <!-- Header Page -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-white tracking-tight italic">Dashboard <span class="text-accent-cyan">Overview</span></h1>
        <p class="text-surface-400 mt-1">Sistem Kontrol Operasional & Kepatuhan Proyek <span class="text-accent-emerald">The PowerPro</span>.</p>
      </div>
      <button class="btn-primary flex items-center gap-2 bg-gradient-to-r from-accent-emerald to-accent-cyan hover:opacity-90 border-none shadow-accent-emerald/20">
        <Plus class="w-5 h-5" />
        New Project
      </button>
    </div>

    <!-- Stats Grid -->
    <div v-auto-animate class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-for="stat in stats" :key="stat.name" class="glass-card flex items-center justify-between group hover:border-accent-cyan/30 transition-all duration-300">
        <div>
          <p class="text-sm font-medium text-surface-500">{{ stat.name }}</p>
          <p class="text-4xl font-bold text-white mt-1">{{ stat.value }}</p>
          <p class="text-xs font-medium mt-2 flex items-center gap-1" :class="stat.value !== '02' ? 'text-green-400' : 'text-red-400'">
            {{ stat.trend }} since last week
          </p>
        </div>
        <div class="w-14 h-14 rounded-2xl bg-surface-800/50 flex items-center justify-center group-hover:bg-brand-500/10 transition-colors">
          <component :is="stat.icon" class="w-7 h-7" :class="stat.color" />
        </div>
      </div>
    </div>

    <!-- Recent Activity Placeholder -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="glass-card">
        <h3 class="text-lg font-bold text-white mb-6">Recent Projects</h3>
        <div class="space-y-6">
          <div v-for="i in 3" :key="i" class="flex items-center gap-4 p-4 rounded-xl border border-surface-800/30 hover:bg-white/5 transition-colors cursor-pointer">
            <div class="w-12 h-12 rounded-lg bg-surface-800 flex items-center justify-center font-bold text-accent-emerald group-hover:scale-110 transition-transform">
              H-{{ i }}
            </div>
            <div class="flex-1">
              <p class="font-bold text-white group-hover:text-accent-cyan transition-colors">Grand Mulia Hotel - Phase {{ i }}</p>
              <div class="flex items-center gap-3 mt-1 text-xs text-surface-500">
                <span class="flex items-center gap-1"><Clock class="w-3 h-3" /> 2 days left</span>
                <span class="px-2 py-0.5 rounded-full bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20">In Progress</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="glass-card flex flex-col items-center justify-center text-center py-12 group hover:border-accent-cyan/30 transition-all">
        <div class="w-20 h-20 rounded-full bg-accent-cyan/10 flex items-center justify-center text-accent-cyan mb-4 group-hover:scale-110 transition-transform shadow-lg shadow-accent-cyan/10">
          <TrendingUp class="w-10 h-10" />
        </div>
        <h3 class="text-xl font-bold text-white italic">Performance <span class="text-accent-emerald">Analytics</span></h3>
        <p class="text-surface-400 mt-2 max-w-xs">Data analitik KPI partner sedang disinkronisasi otomatis oleh <span class="text-accent-cyan font-medium">PowerPro AI</span>...</p>
      </div>
    </div>
  </div>
</template>
