<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Calendar as CalendarIcon, ChevronLeft, ChevronRight, X } from 'lucide-vue-next'

const props = defineProps<{
  modelValue: string | null | undefined
  label: string
  placeholder?: string
  disabled?: boolean
  minDate?: string | null
  maxDate?: string | null
}>()

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const viewDate = ref(new Date())

// Format dd Mmm yy (e.g., 20 Apr 26)
const monthsShort = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

const formattedDisplay = computed(() => {
  if (!props.modelValue) return props.placeholder || 'Select Date...'
  const d = new Date(props.modelValue)
  if (isNaN(d.getTime())) return props.placeholder || 'Select Date...'
  
  const day = String(d.getDate()).padStart(2, '0')
  const month = monthsShort[d.getMonth()]
  const year = String(d.getFullYear()).slice(-2)
  return `${day} ${month} ${year}`
})

const daysInMonth = computed(() => {
  const year = viewDate.value.getFullYear()
  const month = viewDate.value.getMonth()
  const firstDay = new Date(year, month, 1).getDay()
  const days = new Date(year, month + 1, 0).getDate()
  
  const daysArray = []
  // Padding from previous month
  for (let i = 0; i < firstDay; i++) {
    daysArray.push({ day: null, current: false })
  }
  // Current month days
    const todayIso = new Date().toLocaleDateString('en-CA')
    const normMin = props.minDate ? props.minDate.split('T')[0] : null
    const normMax = props.maxDate ? props.maxDate.split('T')[0] : null
    
    for (let i = 1; i <= days; i++) {
      const iso = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`
      daysArray.push({ 
        day: i, 
        iso, 
        current: true,
        selected: props.modelValue === iso,
        isToday: todayIso === iso,
        isDisabled: (normMin && iso < normMin) || (normMax && iso > normMax)
      })
    }
  return daysArray
})

const currentMonthLabel = computed(() => {
  return `${monthsShort[viewDate.value.getMonth()]} ${viewDate.value.getFullYear()}`
})

const changeMonth = (delta: number) => {
  const newDate = new Date(viewDate.value)
  newDate.setMonth(newDate.getMonth() + delta)
  viewDate.value = newDate
}

const selectDate = (iso: string) => {
  const normMin = props.minDate ? props.minDate.split('T')[0] : null
  const normMax = props.maxDate ? props.maxDate.split('T')[0] : null
  
  if (normMin && iso < normMin) return
  if (normMax && iso > normMax) return
  emit('update:modelValue', iso)
  isOpen.value = false
}

const open = () => {
  if (props.modelValue) {
    viewDate.value = new Date(props.modelValue)
  } else {
    viewDate.value = new Date()
  }
  isOpen.value = true
}
</script>

<template>
  <div class="relative">
    <!-- Trigger -->
    <div 
      @click="!disabled && open()"
      class="premium-input-field flex items-center justify-between group transition-all px-4 shadow-sm"
      :class="[
        disabled ? 'opacity-60 cursor-not-allowed bg-surface-500/10' : 'cursor-pointer hover:border-accent-emerald/20'
      ]"
    >
      <span :class="modelValue ? 'text-primary font-bold' : 'text-secondary'" class="font-medium">
        {{ formattedDisplay }}
      </span>
      <CalendarIcon v-if="!disabled" class="w-4 h-4 text-secondary group-hover:text-accent-emerald transition-colors" />
    </div>

    <!-- Popup Modal -->
    <Teleport to="body">
      <div v-if="isOpen" class="fixed inset-0 z-[80] flex items-center justify-center p-4">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-surface-950/40 backdrop-blur-sm animate-in fade-in duration-300" @click="isOpen = false"></div>
        
        <!-- Calendar Body -->
        <div class="relative w-full max-w-sm glass border border-white/10 shadow-2xl flex flex-col rounded-[24px] overflow-hidden animate-in zoom-in duration-200">
          <!-- Header -->
          <div class="p-6 border-b border-border-app bg-surface-500/5">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-[10px] font-black text-secondary uppercase tracking-widest">{{ label || 'Select Date' }}</h3>
              <button @click="isOpen = false" class="p-2 hover:bg-surface-500/10 rounded-lg text-secondary transition-colors">
                <X class="w-4 h-4" />
              </button>
            </div>

            <div class="flex items-center justify-between">
              <button @click="changeMonth(-1)" class="p-2 hover:bg-surface-500/10 rounded-xl text-secondary hover:text-primary transition-all">
                <ChevronLeft class="w-5 h-5" />
              </button>
              <span class="text-sm font-black text-primary uppercase tracking-tighter italic">{{ currentMonthLabel }}</span>
              <button @click="changeMonth(1)" class="p-2 hover:bg-surface-500/10 rounded-xl text-secondary hover:text-primary transition-all">
                <ChevronRight class="w-5 h-5" />
              </button>
            </div>
          </div>

          <!-- Calendar Grid -->
          <div class="p-4 bg-surface-500/5">
            <!-- Weekdays -->
            <div class="grid grid-cols-7 mb-2">
              <div v-for="d in ['Su','Mo','Tu','We','Th','Fr','Sa']" :key="d" class="text-center text-[10px] font-black text-secondary uppercase tracking-tighter py-2">
                {{ d }}
              </div>
            </div>

            <!-- Days -->
            <div class="grid grid-cols-7 gap-1">
              <div v-for="(dayObj, idx) in daysInMonth" :key="idx" class="aspect-square flex items-center justify-center">
                <button 
                   v-if="dayObj.day"
                   @click="selectDate(dayObj.iso!)"
                   class="w-full h-full rounded-xl text-xs font-bold transition-all flex flex-col items-center justify-center relative group"
                   :class="[
                     dayObj.selected ? 'bg-accent-emerald text-white shadow-lg shadow-accent-emerald/20 scale-105' : 'text-primary hover:bg-surface-500/10 hover:text-accent-emerald',
                     dayObj.isToday && !dayObj.selected ? 'text-accent-emerald ring-1 ring-accent-emerald/20 bg-accent-emerald/5' : '',
                     dayObj.isDisabled ? 'opacity-20 cursor-not-allowed grayscale pointer-events-none' : ''
                   ]"
                >
                  {{ dayObj.day }}
                  <div v-if="dayObj.isToday && !dayObj.selected" class="absolute bottom-1 w-1 h-1 bg-accent-emerald rounded-full"></div>
                </button>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="p-4 border-t border-border-app flex items-center justify-between bg-surface-500/5">
            <button @click="emit('update:modelValue', null); isOpen = false" class="text-[10px] font-bold text-secondary hover:text-red-400 transition-colors uppercase tracking-widest">
              Clear Date
            </button>
            <button 
              @click="selectDate(new Date().toLocaleDateString('en-CA'))" 
              class="text-[10px] font-bold text-accent-emerald hover:underline transition-colors uppercase tracking-widest disabled:opacity-20 disabled:no-underline"
              :disabled="(props.minDate && new Date().toLocaleDateString('en-CA') < props.minDate.split('T')[0]) || (props.maxDate && new Date().toLocaleDateString('en-CA') > props.maxDate.split('T')[0])"
            >
              Set Today
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
@reference "tailwindcss";
</style>
