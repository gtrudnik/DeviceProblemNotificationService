import { createApp } from 'vue'
import App from './App.vue'
import router from './router/router';

const app = createApp(App)
app.config.globalProperties.$urlServer = 'http://127.0.0.1:8000';
app.use(router)
app.mount('#app')