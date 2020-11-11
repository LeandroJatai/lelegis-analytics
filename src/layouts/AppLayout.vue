<template>
  <div>
    <Header></Header>
    <main>
      <router-view/>
    </main>
  </div>
</template>
<script>
export default {
  name: 'AppLayout',
  components: {
    Header: () => import('./fragments/Header')
  }
}
</script>
<style lang="scss">
main {
  background-color: #f0f0f0;

}
</style>
