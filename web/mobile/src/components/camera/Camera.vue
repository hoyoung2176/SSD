<template>
  <ion-card height="300" width="200">
    <img :src="video" />
  </ion-card>
</template>

<script>
export default {
  name: 'Camera',
  data () {
    return {
      video: null
    }
  },
  props: ['socket'],
  mounted () {
    this.WatchVideo()
  },
  methods: {
    WatchVideo () {
      this.socket.on('Image', data => {
        this.video = data
      })
    }
  }
}
</script>

