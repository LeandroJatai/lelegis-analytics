import Vue from 'vue'
import Router from 'vue-router'
import AppLayout from '@/layouts/AppLayout'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: AppLayout,
      children: [
        {
          path: '/',
          name: 'resumo_grafico_view',
          component: () => import('@/views/ResumoGraficoView.vue')
        },
        {
          path: '/about',
          name: 'about',
          // route level code-splitting
          // this generates a separate chunk (about.[hash].js) for this route
          // which is lazy-loaded when the route is visited.
          component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
        }
      ]
    }
  ]
})
