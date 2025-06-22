import { createRouter, createWebHistory } from 'vue-router'
import CreateAccount from '../views/CreateAccount.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: CreateAccount,
    }
  ],
})

export default router