import { reactive } from 'vue'

export const store = reactive({
  currentTrack: null,
  progress: 0,
  isPlaying: false
})

export function initWebSocket(callback) {
  const ws = new WebSocket(`ws://${window.location.host}/ws/playback`)

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.type === 'playback_update') {
      Object.assign(store, {
        currentTrack: data.data.track,
        progress: data.data.progress,
        isPlaying: data.data.is_playing
      })
    }
  }

  ws.onopen = () => {
    ws.send(JSON.stringify({ type: 'connection_init' }))
    callback(store)
  }
}
