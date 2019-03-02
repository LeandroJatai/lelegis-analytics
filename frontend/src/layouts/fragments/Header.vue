<template>
  <header :class="[scrollY === 0 ? 'topo-header' : '']"   v-on:scroll.native="handleScroll">
    <div class="logo">
      <img alt="LeLegis Analytics" src="@/assets/logo.svg">
    </div>

    <div class="nav">
      <router-link :to="{name: 'country_view'}">País</router-link>
      <router-link :to="{name: 'about'}">Regiões</router-link>
      <router-link :to="{name: 'about'}">Estados</router-link>
    </div>

  </header>
</template>
<script>
export default {
  name: 'Header',
  data () {
    return {
      scrollY: 0
    }
  },
  methods: {
    handleScroll (event) {
      this.scrollY = window.scrollY
    }
  },
  created () {
    window.addEventListener('scroll', this.handleScroll)
  },
  destroyed () {
    window.removeEventListener('scroll', this.handleScroll)
  }
}
</script>
<style lang="scss">
  $heightHeader: 120px;
  header {
    transition: 0.5s all;
    background-color: white;
    border-bottom: 1px solid #aaa;

    display: grid;
    position: fixed;

    width: 100%;
    top: 0;
    grid-template-columns: 1fr 2fr;
    grid-template-rows: $heightHeader;

    & ~ main {
      margin-top: $heightHeader;
      transition: 0.5s all;
    }
    &.topo-header ~ main {
      transition: 0.5s all;
      margin-top: $heightHeader * 2.208333333;
    }

    &.topo-header {
      transition: 0.5s all;
      padding: $heightHeader * 0.2 $heightHeader * 0.2 0;

      grid-template-columns: auto;
      grid-template-rows: $heightHeader * 1.5 auto;
      .nav {
        justify-content: center;
        a {
          line-height: $heightHeader * 0.5;
        }
      }
    }

    .logo {
      height: 100%;
      img {
        height: 100%;
        padding: 10px;
      }
    }

    .nav {
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: left;
      a {
        padding: 0 1rem;
        font-weight: bold;
        font-size: 120%;
        color: #2c3e50;
        &.router-link-exact-active {
          color: #42b983;
        }
      }
    }
  }

@media screen and (max-width: 767px) {
  header {
    .logo {
      img {
        padding: 20px 10px;
      }
    }
  }

}
</style>
