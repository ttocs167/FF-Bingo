// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'

Vue.config.productionTip = false

Vue.use(Vuetify)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  vuetify: new Vuetify({
    theme: { dark: true,
      themes: {
        dark: {
          primary: '#3d3d3d',
          secondary: '#e8e8e8',
          accent: '#e64b40',
          error: '#cf2144',
          info: '#388cd6',
          success: '#53e04f',
          warning: '#e3b656'
        }
      }
    }
  }),
  components: { App },
  template: '<App/>'
})
