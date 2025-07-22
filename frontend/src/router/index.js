import { createRouter, createWebHistory } from 'vue-router'
import CreateAccount from '@/views/_CreateAccount.vue' // Testing View
import HomeView from '@/views/HomeView.vue'
import AdminView from '@/views/AdminView.vue'
import EditAccountsView from '@/views/admin/EditAccountsView.vue'
import EditItemsView from '@/views/admin/EditItemsView.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
        },
        {
            path: '/admin',
            name: 'admin',
            component: AdminView,
            children: [
                { path: 'edit-accounts', component: EditAccountsView },
                { path: 'edit-items', component: EditItemsView }
            ]
        }
    ]
})

export default router