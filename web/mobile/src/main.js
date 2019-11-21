import Vue from 'vue'
import App from './App'
import router from './router'
import store from './plugins/store'
import Ionic from '@ionic/vue'
import '@ionic/core/css/ionic.bundle.css'

Vue.use(Ionic)
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
