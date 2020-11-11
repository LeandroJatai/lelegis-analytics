<template>
  <div class="resumo-grafico-view">
    <div class="inner-list">
      <b-container fluid>
        <b-row>
          <b-col md="12" v-for="(item, key) in pesquisas" :key="key+1">
            <ResumoPais :pesquisa="item"></ResumoPais>
          </b-col>
        </b-row>
      </b-container>
      <h4 class="empty-list" v-if="pesquisas && pesquisas.length === 0 && init">
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
import ResumoPais from '@/components/ResumoPais'

export default {
  name: 'ResumoGraficoView',
  components: {
    ResumoPais
  },
  data () {
    return {
      utils: Resources.Utils,
      init: false,
      pesquisas: [],
      pagination: []
    }
  },
  mounted () {
    const t = this
    t
      .utils
      .getPesquisa()
      .then(response => {
        t.$set(t, 'pesquisas', [])
        t.init = true
        t.$nextTick()
          .then(function () {
            t.$set(t, 'pesquisas', response.data.results)
            t.$set(t, 'pagination', response.data.pagination)
          })
      })
      .catch((response) => {
        t.init = true
        t.sendMessage({
          alert: 'danger',
          message: 'Não foi possível recuperar dados...',
          time: 5
        })
      })
  }
}
</script>

<style lang="sass">

.lelegis-view
  .empty-list
    padding: 2rem 1rem

  .inner-list
    position: relative

</style>
