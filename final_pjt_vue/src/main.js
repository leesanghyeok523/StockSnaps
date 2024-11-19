import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia()) // Pinia 사용
app.use(router) // Vue Router 사용

app.mount('#app')
