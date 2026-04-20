import { defineStore } from 'pinia'
import apiClient from '../api/api-client'

interface User {
  user_id: string
  username: string
  fullname: string
  email: string
  role_id: string
}

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    isAuthenticated: false,
    isLoading: false,
  }),

  actions: {
    async login(payload: FormData) {
      this.isLoading = true
      try {
        // We use query params style for OAuth2 standard compatibility in FastAPI
        const response = await apiClient.post('/login', payload, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        })
        this.user = response.data.user
        this.isAuthenticated = true
        return response.data
      } catch (error) {
        this.isAuthenticated = false
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async logout() {
      try {
        await apiClient.post('/logout')
      } finally {
        this.user = null
        this.isAuthenticated = false
      }
    },

    async fetchMe() {
      try {
        const response = await apiClient.get('/me')
        this.user = response.data
        this.isAuthenticated = true
      } catch (error) {
        this.user = null
        this.isAuthenticated = false
      }
    }
  }
})
