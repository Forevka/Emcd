import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Admin/Dashboard.vue';
import FAQ from '../views/Admin/FAQ.vue';
import Broadcast from '../views/Admin/Broadcast.vue';
import FAQLangEdit from '../views/Admin/FAQLangEdit.vue';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import(/* webpackChunkName: "about" */ '../views/Admin.vue'),
    children: [
      { path: '', component: Dashboard },
      { path: 'faq', component: FAQ },
      { path: 'faq/:langId', component: FAQLangEdit },
      { path: 'broadcast', component: Broadcast },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
