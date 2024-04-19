
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

createApp(App)
.use(router)//use the router
.mount('#app')//mount the app
