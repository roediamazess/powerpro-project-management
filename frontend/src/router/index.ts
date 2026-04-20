import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('../layouts/MainLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'dashboard',
          component: () => import('../views/DashboardView.vue'),
        },
        {
          path: 'projects',
          name: 'projects',
          component: () => import('../views/ProjectListView.vue'),
        },
        {
          path: 'tasks',
          name: 'tasks',
          component: () => import('../views/TaskListView.vue'),
        },
        {
          path: 'timeboxing',
          name: 'timeboxing',
          component: () => import('../views/TimeboxingView.vue'),
        },
        {
          path: 'partners',
          name: 'partners',
          component: () => import('../views/PartnerListView.vue'),
        },
        {
          path: 'compliance',
          name: 'compliance',
          component: () => import('../views/ComplianceListView.vue'),
        },
        {
          path: 'compliance/new',
          name: 'compliance-new',
          component: () => import('../views/ComplianceFormView.vue'),
        },
        {
          path: 'settings',
          name: 'settings',
          component: () => import('../views/SettingsView.vue'),
        }
      ]
    },
    {
      path: '/auth',
      children: [
        {
          path: 'login',
          name: 'login',
          component: () => import('../views/LoginView.vue')
        }
      ]
    }
  ]
})

router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()
  
  // Optionally fetch user if not already authenticated but session might exist
  if (!authStore.isAuthenticated && to.name !== 'login') {
    await authStore.fetchMe()
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
  } else if (to.name === 'login' && authStore.isAuthenticated) {
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router
