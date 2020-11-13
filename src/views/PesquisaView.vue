<template>
  <div class="pequisa-view">
    <div class="inner-list">
      <b-container fluid>
        <b-row>
          <b-col md="12">
            <h4 class="empty-list">
                Em construção...
            </h4>
          </b-col>
        </b-row>
      </b-container>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

import Resources from '@/resources'

export default {
  name: 'ResumoGraficoView',
  components: {
  },
  data () {
    return {
      utils: Resources.Utils
    }
  },
  mounted () {
  }
}
</script>

<style lang="sass">

.pequisa-view
  text-align: center

  .empty-list
    padding: 2rem 1rem

  .inner-list
    position: relative

</style>
