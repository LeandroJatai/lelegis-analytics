
import Vue from 'vue'
import App from './App.vue'

import router from './router'
import store from './store'

import { sync } from 'vuex-router-sync'

import './registerServiceWorker'

import axios from 'axios'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

loadProgressBar()

Vue.config.productionTip = false

sync(store, router)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
