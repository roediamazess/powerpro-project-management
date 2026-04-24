import { defineStore } from 'pinia'
import apiClient from '../api/api-client'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    lookups: {
      types: [] as any[],
      statuses: [] as any[],
      groups: [] as any[],
      areas: [] as any[],
      sub_areas: [] as any[],
      versions: [] as any[],
      imp_types: [] as any[],
      server_info: [] as any[]
    },
    projectLookups: {
      types: [] as any[],
      statuses: [] as any[],
      arrangements: [] as any[],
      assignments: [] as any[],
      information: [] as any[]
    },
    userLookups: {
      roles: [] as any[],
      tiers: [] as any[]
    },
    users: [] as any[],
    isLoading: false,
    error: null as string | null
  }),

  actions: {
    async fetchUserLookups() {
      this.isLoading = true
      try {
        const res = await apiClient.get('/lookups/user')
        console.log('Fetched User Lookups:', res.data)
        this.userLookups = res.data
      } catch (err) {
        this.error = 'Failed to fetch user settings data'
      } finally {
        this.isLoading = false
      }
    },

    async fetchUsers() {
      this.isLoading = true
      try {
        const res = await apiClient.get('/users/')
        this.users = res.data
      } catch (err) {
        this.error = 'Failed to fetch users'
      } finally {
        this.isLoading = false
      }
    },
    async fetchPartnerLookups() {
      this.isLoading = true
      try {
        const res = await apiClient.get('/lookups/partner')
        this.lookups = res.data
      } catch (err) {
        this.error = 'Failed to fetch partner settings data'
      } finally {
        this.isLoading = false
      }
    },

    async fetchProjectLookups() {
      this.isLoading = true
      try {
        const res = await apiClient.get('/lookups/project')
        this.projectLookups = res.data
      } catch (err) {
        this.error = 'Failed to fetch project settings data'
      } finally {
        this.isLoading = false
      }
    },

    async saveLookup(endpoint: string, payload: any, isEdit: boolean) {
      if (isEdit) {
        await apiClient.put(`/lookups/${endpoint}/${payload.id}`, payload)
      } else {
        await apiClient.post(`/lookups/${endpoint}`, payload)
      }
      
      // Auto-refresh the relevant dataset
      if (endpoint.startsWith('project-')) {
        await this.fetchProjectLookups()
      } else if (endpoint === 'roles' || endpoint === 'tiers') {
        await this.fetchUserLookups()
      } else {
        await this.fetchPartnerLookups()
      }
    }
  }
})
