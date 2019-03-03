<template>
  <div class="country-view">
    <div class="inner-list">
      <div class="empty-list" v-if="pesquisas.length === 0 && init">
          Não foram encontradas Dados no LeLegis Analytics!
      </div>
      <div class="empty-list" v-if="!init">
          Carregando listagem...
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

import Resources from '@/resources'

export default {
  name: 'CountryView',
  components: {
  },
  data () {
    return {
      utils: Resources.Utils,
      init: false,
      pesquisas: [],
      pagination: []
    }
  },
  created () {
    let _this = this
    _this
      .utils
      .getPesquisa()
      .then(response => {
        _this.init = true
        _this.pesquisas = []
        _this.$nextTick()
          .then(function () {
            _this.pesquisas = response.data.results
            _this.pagination = response.data.pagination
          })
      })
      .catch((response) => {
        _this.init = true
        _this.sendMessage({
          alert: 'danger',
          message: 'Não foi possível recuperar dados...',
          time: 5 })
      })
  }
}
</script>
