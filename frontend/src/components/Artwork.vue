<template>
  <div class="artwork">
    <!-- Your artwork content here -->
  </div>
</template>

<script>
export default {
  name: 'Artwork',
  props: {
    src: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.artwork {
  /* Your styles here */
}
</style>
