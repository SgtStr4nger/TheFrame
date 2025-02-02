<template>
  <div class="player-container">
    <div v-if="currentTrack">
      <h2>{{ currentTrack.title }}</h2>
      <p>{{ currentTrack.artist }}</p>
      <img :src="currentTrack.album_art" alt="Album Art">
    </div>
    <div v-else>
      <p>Loading...</p>
      <button @click="fetchPlaybackState">Refresh</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import { initWebSocket } from '../services/websocket';

export default {
  setup() {
    const currentTrack = ref(null);
    let wsConnection = null;

    onMounted(() => {
      wsConnection = initWebSocket((data) => {
        console.log('Updating track data:', data);
        currentTrack.value = data.track;
      });
    });

    onUnmounted(() => {
      if (wsConnection) {
        wsConnection.close();
      }
    });

    return {
      currentTrack
    };
  }
}
</script>