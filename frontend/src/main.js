import { createApp } from 'vue'
import App from './components/Player.vue'
import { initWebSocket } from './services/websocket'

const app = createApp(App)
app.mount('#app')

// Initialize WebSocket connection
initWebSocket(store => {
  app.config.globalProperties.$store = store
})
