<template>
  <div class="lelegis-view">
    <div class="inner-list">
      <b-container fluid>
        <b-row>
          <b-col v-for="(item, key) in pesquisas" :key="key+1">
            <PesquisaPais :pesquisa="item"></PesquisaPais>
          </b-col>
        </b-row>
      </b-container>
      <h4 class="empty-list" v-if="pesquisas.length === 0 && init">
          Não foram encontradas dados no LeLegis Analytics!
      </h4>
      <h4 class="empty-list" v-if="!init">
          Carregando Informações...
      </h4>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

import Resources from '@/resources'
import PesquisaPais from '@/components/PesquisaPais'

export default {
  name: 'LelegisView',
  components: {
    PesquisaPais
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

<style lang="sass">

.lelegis-view
  .empty-list
    padding: 2rem 1rem

  .inner-list
    padding: 3rem 0;

</style>
