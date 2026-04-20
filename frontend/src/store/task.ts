import { defineStore } from 'pinia'
import apiClient from '../api/api-client'

export interface Task {
  task_id: string
  task_no: string
  description: string
  status_id: string
  priority_id: string
  project?: { name: string }
  due_date: string
}

interface TaskState {
  tasks: Task[]
  isLoading: boolean
}

export const useTaskStore = defineStore('task', {
  state: (): TaskState => ({
    tasks: [],
    isLoading: false,
  }),

  actions: {
    async fetchTasks() {
      this.isLoading = true
      try {
        const response = await apiClient.get('/tasks/')
        this.tasks = response.data
      } finally {
        this.isLoading = false
      }
    },

    async createTask(payload: any) {
      const response = await apiClient.post('/tasks/', payload)
      this.tasks.unshift(response.data)
      return response.data
    },

    async updateTask(id: string, payload: any) {
      const response = await apiClient.patch(`/tasks/${id}`, payload)
      const index = this.tasks.findIndex(t => t.task_id === id)
      if (index !== -1) this.tasks[index] = response.data
      return response.data
    }
  }
})
