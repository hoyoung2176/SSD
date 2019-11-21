<template>
  <ion-tabs>
    <ion-tab tab="camera" :routes="'Index'">
      <Camera :socket="socket" />
      <ChatBox :socket="socket" />
    </ion-tab>

    <ion-tab tab="settings"></ion-tab>

    <ion-header>
      <ion-toolbar>
        <ion-title>SmartDoor</ion-title>
      </ion-toolbar>
    </ion-header>
    
    <template slot="bottom">
      <ion-tab-bar>
        <ion-tab-button tab="camera" :to="{ name: 'Index' }">
          <ion-icon name="camera"></ion-icon>
          <ion-label>카메라</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="settings" @click="go">
          <ion-icon name="settings"></ion-icon>
          <ion-label>환경설정</ion-label>
        </ion-tab-button>
      </ion-tab-bar>
    </template>
  </ion-tabs>
</template>

<script>
// import caxios from "@/plugins/corsaxios";
import Camera from '@/components/camera/Camera.vue'
import ChatBox from '@/components/chat/ChatBox.vue'
import io from 'socket.io-client'

export default {
  name: 'Index',
  data () {
    return {
      Server: this.$store.state.server,
      socket: ''
    }
  },
  components: {
    Camera,
    ChatBox
  },
  created () {
    this.ConnectSocket()
  },
  methods: {
    ConnectSocket () {
      this.socket = io(this.Server)
    },
    /* eslint-disable */
    urlBase64ToUint8Array(base64String) {
      const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
      const base64 = (base64String + padding)
        .replace(/\-/g, "+")
        .replace(/_/g, "/");
      const rawData = window.atob(base64);
      return Uint8Array.from([...rawData].map(char => char.charCodeAt(0)));
    },
    /* eslint-disable */

    pushNotification() {
      navigator.serviceWorker.register("service-worker.js");

      navigator.serviceWorker.ready
        .then(function(registration) {
          return registration.pushManager
            .getSubscription()
            .then(async function(subscription) {
              if (subscription) {
                return subscription;
              }

              const response = await fetch(
                "http://192.168.31.55:3000/vapidPublicKey"
              );
              const vapidPublicKey = await response.text();
              const convertedVapidKey = this.urlBase64ToUint8Array(
                vapidPublicKey
              );

              return registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: convertedVapidKey
              });
            });
        })
        .then(function(subscription) {
          fetch("http://192.168.31.55:3000/register", {
            method: "post",
            headers: {
              "Content-type": "application/json"
            },
            body: JSON.stringify({
              subscription: subscription
            })
          });

          fetch("http://192.168.31.55:3000/sendNotification", {
            method: "post",
            headers: {
              "Content-type": "application/json"
            },
            body: JSON.stringify({
              subscription: subscription
            })
          });
        });
    }
  }
};
</script>