import Vue from 'vue'
import Vuex from 'vuex'
import BootstrapVue from 'bootstrap-vue'

import VuexStore from './store'

import axios from 'axios'

import { sync } from 'vuex-router-sync'
import { loadProgressBar } from 'axios-progress-bar'
import 'axios-progress-bar/dist/nprogress.css'

import router from './router'

import App from './App'

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

Vue.use(Vuex)
Vue.use(BootstrapVue)

loadProgressBar()

Vue.config.productionTip = false

const store = new Vuex.Store(VuexStore)
sync(store, router)

// com runtimeCompiler = true
/* new Vue({ // eslint-disable-line 
  router,
  store,
  el: '#app',
  components: { App },
  template: '<App/>'
}) */

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
