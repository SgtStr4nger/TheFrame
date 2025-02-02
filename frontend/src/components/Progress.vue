<template>
  <div class="progress-container">
    <div class="progress-bar" :style="{ width: progressPercentage + '%' }"></div>
    <div class="time-display">
      <span>{{ formattedProgress }}</span>
      <span>{{ formattedDuration }}</span>
    </div>
  </div>
</template>

<script>
import { gsap } from 'gsap'

export default {
  props: ['duration', 'progress'],
  computed: {
    progressPercentage() {
      return ((this.progress / this.duration) * 100) || 0
    },
    formattedProgress() {
      return this.formatTime(this.progress)
    },
    formattedDuration() {
      return this.formatTime(this.duration)
    }
  },
  watch: {
    progress: {
      handler(newVal) {
        gsap.to('.progress-bar', {
          duration: 1,
          width: `${this.progressPercentage}%`,
          ease: 'linear'
        })
      },
      immediate: true
    }
  },
  methods: {
    formatTime(seconds) {
      const mins = Math.floor(seconds / 60)
      const secs = Math.floor(seconds % 60)
      return `${mins}:${secs.toString().padStart(2, '0')}`
    }
  }
}
</script>
