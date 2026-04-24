import { defineStore } from 'pinia'
import apiClient from '../api/api-client'

export interface Partner {
  partner_id: string
  name: string
  partner_cnc: string
  type_id: string
  status_id: string
  stars: number
  rooms: number
  outlets: number
  address: string
  area_id?: string
  sub_area_id?: string
  last_visit_at?: string
  last_visit_type?: string
  last_project?: string
  last_project_type?: string
  version_id?: string
  imp_type_id?: string
  server_information_id?: string
  server_information_detail?: string
  system_live_at?: string
  contacts: any[]
  updated_at: string
}

interface PartnerState {
  partners: Partner[]
  lookups: {
    types: any[]
    statuses: any[]
    groups: any[]
    areas: any[]
    sub_areas: any[]
    versions: any[]
    imp_types: any[]
    server_info: any[]
  }
  isLoading: boolean
  error: string | null
}

export const usePartnerStore = defineStore('partner', {
  state: (): PartnerState => ({
    partners: [],
    lookups: {
      types: [],
      statuses: [],
      groups: [],
      areas: [],
      sub_areas: [],
      versions: [],
      imp_types: [],
      server_info: [],
    },
    isLoading: false,
    error: null,
  }),

  actions: {
    async fetchPartners() {
      this.isLoading = true
      try {
        const response = await apiClient.get('/partners/')
        this.partners = response.data
      } catch (err: any) {
        this.error = 'Gagal memuat data partner.'
      } finally {
        this.isLoading = false
      }
    },

    async fetchLookups() {
      try {
        const response = await apiClient.get('/lookups/partner')
        this.lookups = response.data
      } catch (err: any) {
        console.error('Failed to fetch lookups', err)
      }
    },

    async createPartner(payload: any) {
      try {
        const response = await apiClient.post('/partners/', payload)
        this.partners.unshift(response.data)
        return response.data
      } catch (err: any) {
        throw err
      }
    },

    async updatePartner(id: string, payload: any) {
      try {
        const response = await apiClient.patch(`/partners/${id}`, payload)
        const index = this.partners.findIndex(p => p.partner_id === id)
        if (index !== -1) this.partners[index] = response.data
        return response.data
      } catch (err: any) {
        throw err
      }
    },

    async deletePartner(id: string) {
      try {
        await apiClient.delete(`/partners/${id}`)
        this.partners = this.partners.filter(p => p.partner_id !== id)
      } catch (err: any) {
        throw err
      }
    }
  }
})
