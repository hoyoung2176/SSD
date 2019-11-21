import Vue from 'vue'
import { IonicVueRouter } from '@ionic/vue'
import Index from '@/views/index.vue'

Vue.use(IonicVueRouter)

const routes = [
  {
    path: '/',
    name: 'Index',
    component: Index
  }
]

const router = new IonicVueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
