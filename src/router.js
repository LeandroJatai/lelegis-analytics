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
          path: '/pesquisa',
          name: 'pesquisa_view',
          component: () => import('@/views/PesquisaView.vue')
        }
      ]
    }
  ]
})
