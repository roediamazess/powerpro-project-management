import { defineStore } from 'pinia'

export type ToastType = 'success' | 'error' | 'info' | 'warning'
export type Theme = 'light' | 'dark'

interface Toast {
  id: string
  message: string
  type: ToastType
  duration: number
}

interface UIState {
  toasts: Toast[]
  theme: Theme
}

export const useUIStore = defineStore('ui', {
  state: (): UIState => ({
    toasts: [],
    theme: (localStorage.getItem('theme') as Theme) || 'dark',
  }),

  actions: {
    toggleTheme() {
      this.theme = this.theme === 'dark' ? 'light' : 'dark'
      localStorage.setItem('theme', this.theme)
      this.syncTheme()
    },

    syncTheme() {
      if (this.theme === 'dark') {
        document.documentElement.classList.add('dark')
        document.documentElement.classList.remove('light')
      } else {
        document.documentElement.classList.add('light')
        document.documentElement.classList.remove('dark')
      }
    },

    showToast(message: string, type: ToastType = 'success', duration: number = 3000) {
      const id = Math.random().toString(36).substring(2, 9)
      const toast: Toast = { id, message, type, duration }
      
      this.toasts.push(toast)

      setTimeout(() => {
        this.removeToast(id)
      }, duration)
    },

    removeToast(id: string) {
      this.toasts = this.toasts.filter((t) => t.id !== id)
    },
  },
})
