<script setup lang="ts">
import { onMounted } from 'vue'
import AppToast from './components/ui/AppToast.vue'
import { useUIStore } from './store/ui'

const uiStore = useUIStore()

onMounted(() => {
  uiStore.syncTheme()
})
</script>

<template>
  <AppToast />
  <router-view />
</template>
