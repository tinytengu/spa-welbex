import Vue from 'vue'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'

import App from './App'

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  components: { App },
  template: '<App/>'
})
