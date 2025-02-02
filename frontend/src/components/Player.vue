<template>
  <div class="player-container">
    <Artwork :src="currentTrack.album_art" />
    <div class="track-info">
      <h2 class="track-title">{{ currentTrack.title }}</h2>
      <p class="track-artist">{{ currentTrack.artist }}</p>
    </div>
    <Progress :duration="currentTrack.duration" :progress="progress" />
    <div class="controls">
      <button @click="togglePlay">
        <span class="material-icons">{{ isPlaying ? 'pause' : 'play_arrow' }}</span>
      </button>
    </div>
  </div>
</template>

<script>
import Artwork from './Artwork.vue'
import Progress from './Progress.vue'

export default {
  components: { Artwork, Progress },
  data() {
    return {
      currentTrack: {
        title: 'Loading...',
        artist: '',
        album_art: '',
        duration: 0
      },
      progress: 0,
      isPlaying: false
    }
  },
  mounted() {
    this.$watch(
      () => this.$store,
      (newState) => {
        this.currentTrack = newState.currentTrack || this.currentTrack
        this.progress = newState.progress
        this.isPlaying = newState.isPlaying
      },
      { deep: true, immediate: true }
    )
  },
  methods: {
    togglePlay() {
      // Implement play/pause control
    }
  }
}
</script>
