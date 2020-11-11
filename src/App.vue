<template>
  <div id="app">
    <message></message>
    <router-view></router-view>
  </div>

</template>

<script>
import Message from '@/components/utils/message/Message'
export default {
  components: {
    Message
  },
  mounted: function () {
    // this.sendMessage({ alert: 'success', message: 'montou app', time: 5 })
  }
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
