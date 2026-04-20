import { defineStore } from 'pinia'
import apiClient from '../api/api-client'

export interface Timebox {
  timebox_id: string
  activity_name: string
  start_time: string
  end_time: string
  color_code: string
  is_completed: boolean
  task_id?: string
}

interface TimeboxState {
  timeboxes: Timebox[]
  isLoading: boolean
}

export const useTimeboxStore = defineStore('timebox', {
  state: (): TimeboxState => ({
    timeboxes: [],
    isLoading: false,
  }),

  actions: {
    async fetchTimeboxes(userId?: string) {
      this.isLoading = true
      try {
        const url = userId ? `/timeboxing/?user_id=${userId}` : '/timeboxing/'
        const response = await apiClient.get(url)
        this.timeboxes = response.data
      } finally {
        this.isLoading = false
      }
    },

    async createTimebox(payload: any) {
      const response = await apiClient.post('/timeboxing/', payload)
      this.timeboxes.push(response.data)
      return response.data
    },

    async toggleComplete(id: string, is_completed: boolean) {
      const response = await apiClient.patch(`/timeboxing/${id}`, { is_completed })
      const index = this.timeboxes.findIndex(t => t.timebox_id === id)
      if (index !== -1) this.timeboxes[index] = response.data
    }
  }
})
