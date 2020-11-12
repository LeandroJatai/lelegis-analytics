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
</style>
