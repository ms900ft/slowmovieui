import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'

import {
  router
} from './router'

import vuetify from './plugins/vuetify';

Vue.config.productionTip = false
let BaseUrl = location.protocol

if (process.env.NODE_ENV === 'development') {
  BaseUrl = 'http://slowmovie:8888'
}

axios.defaults.baseURL = BaseUrl
Vue.prototype.$baseURL = BaseUrl

new Vue({
  //vuetify,
  render: h => h(App),

  //store,
  router,

  vuetify,

  icons: {
    iconfont: 'mdi' // default - only for display purposes
  }
}).$mount('#app')