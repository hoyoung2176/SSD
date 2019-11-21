<template>
  <ion-gird>
    <ion-item>
      <ion-label position="floating">대화창</ion-label>
      <ion-textarea rows="6" cols="20" readonly="readonly"></ion-textarea>
    </ion-item>
    <ion-item>
      <ion-col size="10">
        <ion-input :value="chatText" @input="chatText = $event.target.value" name="chatText"></ion-input>
      </ion-col>
      <ion-col size="2">
        <ion-button @click="SendMsg">
          <ion-icon name="mic"></ion-icon>
        </ion-button>
      </ion-col>
    </ion-item>
  </ion-gird>
</template>

<script>
export default {
  name: 'ChatBox',
  data () {
    return {
      chatText: ''
    }
  },
  props: ['socket'],
  mounted () {
    this.getMessage()
  },
  methods: {
    getMessage () {
      this.socket.on('DoorMsg', data => {
        this.chatText = data
      })
    },
    SendMsg () {
      this.socket.emit('MobileMsg', this.chatText)
      this.chatText = ''
    }
  }
}
</script>