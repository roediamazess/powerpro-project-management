import { defineStore } from 'pinia'
import apiClient from '../api/api-client'

export interface Project {
  project_id: string
  name: string
  partner: { partner_id: string; name: string }
  status_id: string
  start_date: string
  end_date: string
  total_days: number
  point_percent: number
  pics: any[]
}

interface ProjectState {
  projects: Project[]
  isLoading: boolean
  error: string | null
}

export const useProjectStore = defineStore('project', {
  state: (): ProjectState => ({
    projects: [],
    isLoading: false,
    error: null,
  }),

  actions: {
    async fetchProjects() {
      this.isLoading = true
      try {
        const response = await apiClient.get('/projects/')
        this.projects = response.data
      } catch (err: any) {
        this.error = 'Gagal memuat data proyek.'
      } finally {
        this.isLoading = false
      }
    },

    async createProject(payload: any) {
      try {
        const response = await apiClient.post('/projects/', payload)
        this.projects.unshift(response.data)
        return response.data
      } catch (err: any) {
        throw err
      }
    },

    async updateProject(id: string, payload: any) {
      try {
        const response = await apiClient.patch(`/projects/${id}`, payload)
        const index = this.projects.findIndex(p => p.project_id === id)
        if (index !== -1) this.projects[index] = response.data
        return response.data
      } catch (err: any) {
        throw err
      }
    },

    async deleteProject(id: string) {
      try {
        await apiClient.delete(`/projects/${id}`)
        this.projects = this.projects.filter(p => p.project_id !== id)
      } catch (err: any) {
        throw err
      }
    }
  }
})
