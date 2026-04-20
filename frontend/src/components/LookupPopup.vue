<script setup lang="ts">
import { ref, computed } from 'vue'
import { Check, Search, ChevronRight, X } from 'lucide-vue-next'

const props = defineProps<{
  modelValue: string | number | null | undefined
  options: Array<{ id: string | number; name: string }>
  label: string
  placeholder?: string
}>()

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const searchQuery = ref('')

const selectedName = computed(() => {
  const option = props.options.find(o => o.id === props.modelValue)
  return option ? option.name : props.placeholder || 'Select...'
})

const filteredOptions = computed(() => {
  if (!searchQuery.value) return props.options
  return props.options.filter(o => 
    o.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const select = (id: string | number) => {
  emit('update:modelValue', id)
  isOpen.value = false
  searchQuery.value = ''
}

const open = () => {
  isOpen.value = true
  searchQuery.value = ''
}
</script>

<template>
  <div class="relative">
    <!-- Trigger -->
    <div 
      @click="open"
      class="premium-input-field cursor-pointer flex items-center justify-between group hover:border-accent-emerald/20 transition-all shadow-sm"
    >
      <span :class="modelValue ? 'text-primary font-bold' : 'text-secondary'">
        {{ selectedName }}
      </span>
      <ChevronRight class="w-4 h-4 text-secondary group-hover:text-primary transition-colors" />
    </div>

    <!-- Popup Modal (Teleported to body for absolute stacking) -->
    <Teleport to="body">
      <div v-if="isOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-surface-950/40 backdrop-blur-sm animate-in fade-in duration-300" @click="isOpen = false"></div>
        
        <!-- content -->
        <div class="relative w-full max-w-md glass border border-white/10 shadow-2xl flex flex-col rounded-[24px] overflow-hidden animate-in zoom-in duration-200">
          <!-- Header -->
          <div class="p-6 border-b border-border-app bg-surface-500/5">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-[10px] font-black text-secondary uppercase tracking-widest">{{ label || 'Select Option' }}</h3>
              <button @click="isOpen = false" class="p-2 hover:bg-surface-500/10 rounded-lg text-secondary transition-colors">
                <X class="w-4 h-4" />
              </button>
            </div>
            
            <div class="relative group">
              <div class="absolute left-4 top-1/2 -translate-y-1/2 flex items-center pointer-events-none z-10">
                <Search class="w-4 h-4 text-secondary group-focus-within:text-accent-emerald transition-colors" />
              </div>
              <input 
                v-model="searchQuery"
                type="text" 
                class="premium-input-field text-sm py-2 !bg-surface-500/5 focus:!bg-card shadow-inner"
                style="padding-left: 3.5rem !important;"
                placeholder="Search options..."
                autoFocus
              >
            </div>
          </div>

          <!-- List -->
          <div class="flex-1 max-h-[400px] overflow-y-auto p-2 custom-scrollbar">
            <div 
              v-for="opt in filteredOptions" 
              :key="opt.id"
              @click="select(opt.id)"
              class="flex items-center justify-between px-4 py-3 rounded-xl cursor-pointer hover:bg-surface-500/10 transition-colors group"
            >
              <span class="text-sm font-medium transition-colors" :class="modelValue === opt.id ? 'text-accent-emerald bg-accent-emerald/5 px-2 py-0.5 rounded-lg' : 'text-primary group-hover:text-accent-emerald'">
                {{ opt.name }}
              </span>
              <Check v-if="modelValue === opt.id" class="w-4 h-4 text-accent-emerald" />
            </div>

            <div v-if="filteredOptions.length === 0" class="py-12 text-center">
              <p class="text-xs text-surface-600 uppercase tracking-widest">No matching options</p>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
@reference "tailwindcss";

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  @apply bg-white/5 rounded-full;
}
</style>
