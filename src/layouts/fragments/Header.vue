<template>
  <header :class="[scrollY === 0 ? 'header-top' : '']" >
    <div class="logo">
      <img alt="LeLegis Analytics" src="@/assets/logo.svg">
    </div>

    <div class="nav">
      <router-link :to="{name: 'resumo_grafico_view'}">Resumo Gráfico</router-link>
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

      const h = document.getElementsByTagName('header')[0]
      if (window.scrollY === 0) {
        h.classList.remove('header-mini')
        // console.log('topo', window.scrollY)
      } else if (window.scrollY > 220 && window.scrollY < 300) {
        if (h.classList.contains('header-mini') || h.classList.contains('header-top')) {
          h.classList.remove('header-top')
          h.classList.remove('header-mini')
        }
        // console.log('meio', window.scrollY)
      } else if (window.scrollY > 400) {
        if (!h.classList.contains('header-mini')) {
          h.classList.add('header-mini')
          h.classList.remove('header-top')
          // console.log('fim', window.scrollY)
        }
      } else {
        // console.log('limbo', window.scrollY)
      }
    }
  },
  created () {
    window.addEventListener('scroll', this.handleScroll, { passive: true })
  },
  destroyed () {
    // window.removeEventListener('scroll', this.handleScroll)
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

    width: 100%;
    top: 0;
    grid-template-columns: 1fr 2fr;
    grid-template-rows: $heightHeader;

    & ~ main {
      transition: 0.5s all;
    }
    &.header-top ~ main {
      transition: 0.5s all;
    }

    &.header-top {

      position: relative;
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
