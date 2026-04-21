<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useComplianceStore } from '../store/compliance'
import { useAuthStore } from '../store/auth'
import { useSettingsStore } from '../store/settings'
import LookupManager from './settings/LookupManager.vue'
import UserManager from './settings/UserManager.vue'
import { 
  Database, FileText, Plus, 
  Trash2, ShieldAlert, Users,
  MapPin, Globe, Layers, Activity,
  Settings2, Briefcase
} from 'lucide-vue-next'

const complianceStore = useComplianceStore()
const authStore = useAuthStore()
const settingsStore = useSettingsStore()

const activeTab = ref('partner_config')
const activePartnerSubTab = ref('areas')
const activeProjectSubTab = ref('types')
const activeUserSubTab = ref('users')

onMounted(() => {
  complianceStore.fetchForms()
  settingsStore.fetchPartnerLookups()
  settingsStore.fetchProjectLookups()
  settingsStore.fetchUserLookups()
  settingsStore.fetchUsers()
})

const isAdmin = () => authStore.user?.role_id === 'ADMIN'

const partnerConfigTabs = [
  { id: 'areas', label: 'Primary Areas', icon: Globe },
  { id: 'sub_areas', label: 'Sub Areas', icon: MapPin },
  { id: 'groups', label: 'Partner Groups', icon: Layers },
  { id: 'types', label: 'Partner Types', icon: Users },
  { id: 'statuses', label: 'Status States', icon: Activity },
  { id: 'versions', label: 'System Versions', icon: Settings2 },
  { id: 'imp_types', label: 'Implementation', icon: Database },
]

const projectConfigTabs = [
  { id: 'types', label: 'Project Types', icon: Briefcase },
  { id: 'statuses', label: 'Status States', icon: Activity },
  { id: 'arrangements', label: 'Arrangements', icon: Layers },
  { id: 'assignments', label: 'Assignments', icon: Users },
  { id: 'information', label: 'Information', icon: FileText },
]

const userManagementTabs = [
  { id: 'users', label: 'Users', icon: Users },
  { id: 'roles', label: 'Roles', icon: ShieldAlert },
  { id: 'tiers', icon: Award, label: 'Tiers' }
]

import { Award } from 'lucide-vue-next'
</script>

<template>
  <div class="space-y-8" v-auto-animate>
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-white tracking-tight italic text-shadow-glow">System <span class="text-accent-cyan">Settings</span></h1>
        <p class="text-surface-400 mt-1 font-medium">Industrial lookup management and global configuration hub.</p>
      </div>
      <div v-if="!isAdmin()" class="flex items-center gap-2 px-4 py-2 bg-red-500/10 border border-red-500/30 rounded-xl text-red-500 text-xs font-black uppercase">
        <ShieldAlert class="w-4 h-4" /> Restricted Access
      </div>
    </div>

    <div class="grid grid-cols-[250px_1fr] gap-8">
      <!-- Sidebar Tabs -->
      <div class="space-y-2">
        <div class="px-4 py-2 text-[10px] font-black text-surface-500 uppercase tracking-[0.2em] mb-2">Metadata Control</div>
        
        <button 
          @click="activeTab = 'partner_config'"
          class="w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-bold text-sm"
          :class="activeTab === 'partner_config' ? 'bg-accent-emerald text-surface-950 shadow-lg shadow-accent-emerald/20' : 'text-surface-400 hover:bg-white/5'"
        >
          <Users class="w-4 h-4" /> Partner Config
        </button>

        <button 
          @click="activeTab = 'project_config'"
          class="w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-bold text-sm"
          :class="activeTab === 'project_config' ? 'bg-accent-emerald text-surface-950 shadow-lg shadow-accent-emerald/20' : 'text-surface-400 hover:bg-white/5'"
        >
          <Briefcase class="w-4 h-4" /> Project Config
        </button>

        <button 
          @click="activeTab = 'user_config'"
          class="w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-bold text-sm"
          :class="activeTab === 'user_config' ? 'bg-accent-emerald text-surface-950 shadow-lg shadow-accent-emerald/20' : 'text-surface-400 hover:bg-white/5'"
        >
          <Users class="w-4 h-4" /> User Management
        </button>

        <button 
          @click="activeTab = 'forms'"
          class="w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-bold text-sm"
          :class="activeTab === 'forms' ? 'bg-accent-cyan text-surface-950 shadow-lg shadow-accent-cyan/20' : 'text-surface-400 hover:bg-white/5'"
        >
          <FileText class="w-4 h-4" /> Compliance Templates
        </button>

        <button 
          @click="activeTab = 'items'"
          class="w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-bold text-sm"
          :class="activeTab === 'items' ? 'bg-accent-cyan text-surface-950 shadow-lg shadow-accent-cyan/20' : 'text-surface-400 hover:bg-white/5'"
        >
          <Database class="w-4 h-4" /> Shared Audit Items
        </button>
      </div>

      <!-- Main Content Area -->
      <div class="glass-card min-h-[600px] flex flex-col p-0 overflow-hidden">
        <!-- Partner Config Hub -->
        <div v-if="activeTab === 'partner_config'" class="flex flex-col flex-1" v-auto-animate>
          <div class="p-6 border-b border-white/5 bg-surface-950/20">
             <div class="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
                <button 
                  v-for="sub in partnerConfigTabs" :key="sub.id"
                  @click="activePartnerSubTab = sub.id"
                  class="flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all whitespace-nowrap active:scale-95"
                  :class="activePartnerSubTab === sub.id ? 'bg-white/10 text-white ring-1 ring-white/10 shadow-lg' : 'text-surface-500 hover:text-surface-300'"
                >
                  <component :is="sub.icon" class="w-3.5 h-3.5" />
                  {{ sub.label }}
                </button>
             </div>
          </div>

          <div class="p-8 flex-1">
             <LookupManager v-if="activePartnerSubTab === 'areas'" title="Primary Areas" subtitle="Regional classification for partner hotels." :items="settingsStore.lookups.areas" endpoint="partner-areas" />
             <LookupManager v-if="activePartnerSubTab === 'groups'" title="Partner Groups" subtitle="Ownership clusters and management chains." :items="settingsStore.lookups.groups" endpoint="partner-groups" />
             <LookupManager v-if="activePartnerSubTab === 'types'" title="Partner Types" subtitle="Classification of business units (Hotel, Resort, etc.)" :items="settingsStore.lookups.types" endpoint="partner-types" />
             <LookupManager v-if="activePartnerSubTab === 'statuses'" title="Status States" subtitle="Operational lifecycle statuses." :items="settingsStore.lookups.statuses" endpoint="partner-statuses" />
             <LookupManager v-if="activePartnerSubTab === 'versions'" title="System Versions" subtitle="Active PowerPro software versions." :items="settingsStore.lookups.versions" endpoint="partner-versions" />
             <LookupManager v-if="activePartnerSubTab === 'imp_types'" title="Implementation" subtitle="Types of implementation projects." :items="settingsStore.lookups.imp_types" endpoint="partner-imp-types" />
             
             <LookupManager 
               v-if="activePartnerSubTab === 'sub_areas'" 
               title="Sub Areas" 
               subtitle="Specific district or local zone within an area." 
               :items="settingsStore.lookups.sub_areas" 
               endpoint="partner-sub-areas"
               :extraFields="[{ label: 'Parent Area', key: 'area_id' }]"
               :extraData="settingsStore.lookups.areas"
             />
          </div>
        </div>

        <!-- Project Config Hub -->
        <div v-else-if="activeTab === 'project_config'" class="flex flex-col flex-1" v-auto-animate>
          <div class="p-6 border-b border-white/5 bg-surface-950/20">
             <div class="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
                <button 
                  v-for="sub in projectConfigTabs" :key="sub.id"
                  @click="activeProjectSubTab = sub.id"
                  class="flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all whitespace-nowrap active:scale-95"
                  :class="activeProjectSubTab === sub.id ? 'bg-white/10 text-white ring-1 ring-white/10 shadow-lg' : 'text-surface-500 hover:text-surface-300'"
                >
                  <component :is="sub.icon" class="w-3.5 h-3.5" />
                  {{ sub.label }}
                </button>
             </div>
          </div>

          <div class="p-8 flex-1">
             <LookupManager v-if="activeProjectSubTab === 'types'" title="Project Types" subtitle="Classification of implementation or projects." :items="settingsStore.projectLookups.types" endpoint="project-types" />
             <LookupManager v-if="activeProjectSubTab === 'statuses'" title="Status States" subtitle="Project lifecycle tracking statuses." :items="settingsStore.projectLookups.statuses" endpoint="project-statuses" />
             <LookupManager v-if="activeProjectSubTab === 'arrangements'" title="Arrangement Models" subtitle="Working methods (Remote, On-site, etc.)" :items="settingsStore.projectLookups.arrangements" endpoint="project-arrangements" />
             <LookupManager v-if="activeProjectSubTab === 'assignments'" title="Assignment Roles" subtitle="Contractual relation roles." :items="settingsStore.projectLookups.assignments" endpoint="project-assignments" />
             <LookupManager v-if="activeProjectSubTab === 'information'" title="Project Information" subtitle="Additional metadata for project context." :items="settingsStore.projectLookups.information" endpoint="project-information" />
          </div>
        </div>

        <!-- User Management Hub -->
        <div v-else-if="activeTab === 'user_config'" class="flex flex-col flex-1" v-auto-animate>
          <div class="p-6 border-b border-white/5 bg-surface-950/20">
             <div class="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
                <button 
                  v-for="sub in userManagementTabs" :key="sub.id"
                  @click="activeUserSubTab = sub.id"
                  class="flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all whitespace-nowrap active:scale-95"
                  :class="activeUserSubTab === sub.id ? 'bg-white/10 text-white ring-1 ring-white/10 shadow-lg' : 'text-surface-500 hover:text-surface-300'"
                >
                  <component :is="sub.icon" class="w-3.5 h-3.5" />
                  {{ sub.label }}
                </button>
             </div>
          </div>

          <div class="p-8 flex-1">
             <UserManager 
               v-if="activeUserSubTab === 'users'" 
               :users="settingsStore.users" 
               :roles="settingsStore.userLookups.roles" 
               :tiers="settingsStore.userLookups.tiers" 
             />
             <LookupManager v-if="activeUserSubTab === 'roles'" title="User Roles" subtitle="Security permission hierarchies." :items="settingsStore.userLookups.roles" endpoint="roles" />
             <LookupManager v-if="activeUserSubTab === 'tiers'" title="Seniority Tiers" subtitle="Employee level and access depth." :items="settingsStore.userLookups.tiers" endpoint="tiers" />
          </div>
        </div>

        <!-- Compliance Forms -->
        <div v-else-if="activeTab === 'forms'" class="p-8 space-y-6" v-auto-animate>
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-bold text-white italic">Compliance Forms</h2>
            <button v-if="isAdmin()" class="btn-primary py-2 px-4 text-xs bg-accent-cyan hover:bg-cyan-400 border-none text-surface-950 flex items-center gap-2">
              <Plus class="w-4 h-4" /> Build Template
            </button>
          </div>

          <div class="grid grid-cols-1 gap-3">
             <div v-for="form in complianceStore.forms" :key="form.form_id" class="p-4 bg-surface-900/50 border border-white/5 rounded-2xl flex items-center justify-between group hover:border-accent-cyan/30 transition-all cursor-pointer">
                <div class="flex items-center gap-4">
                   <div class="w-10 h-10 rounded-xl bg-accent-cyan/10 flex items-center justify-center text-accent-cyan group-hover:scale-110 transition-transform">
                     <FileText class="w-5 h-5" />
                   </div>
                   <div>
                     <p class="font-bold text-white group-hover:text-accent-cyan transition-colors">{{ form.name }}</p>
                     <p class="text-[10px] text-surface-500 font-black uppercase tracking-widest">{{ form.form_code }} • {{ form.items?.length || 0 }} Items</p>
                   </div>
                </div>
                <div class="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button class="p-2.5 hover:bg-white/5 rounded-xl text-surface-400 hover:text-accent-cyan transition-all"><Plus class="w-4 h-4" /></button>
                  <button class="p-2.5 hover:bg-white/5 rounded-xl text-surface-400 hover:text-red-500 transition-all"><Trash2 class="w-4 h-4" /></button>
                </div>
             </div>
          </div>
        </div>

        <!-- Shared Audit Items -->
        <div v-else class="flex flex-col items-center justify-center py-20 text-center space-y-4">
           <div class="w-20 h-20 rounded-full bg-surface-900 flex items-center justify-center text-surface-700 shadow-xl border border-white/5">
             <Database class="w-10 h-10" />
           </div>
           <p class="text-surface-500 font-medium max-w-xs italic">Shared audit library management is coming in next release. Currently managed via SEED.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.scrollbar-none::-webkit-scrollbar { display: none; }
.scrollbar-none { -ms-overflow-style: none; scrollbar-width: none; }
.text-shadow-glow { text-shadow: 0 0 20px rgba(34, 211, 238, 0.3); }
</style>
