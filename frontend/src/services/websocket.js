import { reactive } from 'vue'

export const store = reactive({
  currentTrack: null,
  progress: 0,
  isPlaying: false
})

export function initWebSocket(callback) {
    const ws = new WebSocket('ws://localhost:8000/ws/playback');

    ws.onopen = () => {
        console.log('WebSocket Connected');
        // Send initial message to start receiving updates
        ws.send('connect');
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('Received playback update:', data);
        if (data.type === 'playback_update') {
            callback(data.data);
        }
    };

    ws.onerror = (error) => {
        console.error('WebSocket Error:', error);
    };

    // Keep connection alive
    setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
            ws.send('ping');
        }
    }, 300);

    return ws;
}