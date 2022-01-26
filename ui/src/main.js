//import { createApp } from 'vue'
import { createApp } from 'vue/dist/vue.esm-bundler.js'
import App from './App.vue'
import router from './router'

import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

createApp(App).use(router).mount('#app')
