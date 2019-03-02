<template>
  <div>
    <Header></Header>
    <main>
      <router-view/>
    </main>
  </div>
</template>
<script>
import Header from './fragments/Header'
export default {
  name: 'AppLayout',
  components: {
    Header
  }
}
</script>
<style lang="scss">
</style>
