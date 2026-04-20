import { defineStore } from 'pinia'
import apiClient from '../api/api-client'

export interface ComplianceForm {
  form_id: string
  form_code: string
  name: string
  items: any[]
}

export interface ComplianceEntry {
  entry_id: string
  partner_id: string
  form: { name: string }
  compliance_percent: number
  status: string
  created_at: string
}

interface ComplianceState {
  forms: ComplianceForm[]
  entries: ComplianceEntry[]
  isLoading: boolean
}

export const useComplianceStore = defineStore('compliance', {
  state: (): ComplianceState => ({
    forms: [],
    entries: [],
    isLoading: false,
  }),

  actions: {
    async fetchForms() {
      const response = await apiClient.get('/compliance/forms')
      this.forms = response.data
    },

    async fetchEntries() {
      this.isLoading = true
      try {
        const response = await apiClient.get('/compliance/entries')
        this.entries = response.data
      } finally {
        this.isLoading = false
      }
    },

    async submitEntry(payload: any) {
      const response = await apiClient.post('/compliance/entries', payload)
      this.entries.unshift(response.data)
      return response.data
    }
  }
})
