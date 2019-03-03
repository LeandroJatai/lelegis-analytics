<template>
  <div>
    <h1>{{pesquisa.title}}</h1>
    <small>{{pesquisa.description}}</small>

    <pie-chart :data="dataPais" :colors="['#00b', '#b00']"></pie-chart>

    <h4>Total de Endereços Analisados: {{pesquisa.ping_true.pais.total + pesquisa.ping_false.pais.total}}</h4>
  </div>
</template>
<script>
import Resources from '@/resources'

export default {
  name: 'PesquisaPais',
  props: ['pesquisa'],
  data () {
    return {
      utils: Resources.Utils,
      init: false,
      childs: []
    }
  },
  computed: {
    dataPais: function () {
      // [['Blueberry', 44], ['Strawberry', 23]]
      return [
        ['Acessivel', this.pesquisa.ping_true.pais.total],
        ['Sem Acesso', this.pesquisa.ping_false.pais.total]
      ]
    }
  },

  mounted () {
    let _this = this

    _.each(_this.pesquisa.childs, function (value) {
      _this
        .utils
        .getPesquisa(value)
        .then(response => {
          _this.$nextTick()
            .then(function () {
              _this.childs.push(response.data)
            })
        })
        .catch((response) => {
          _this.sendMessage({
            alert: 'danger',
            message: 'Não foi possível recuperar dados...',
            time: 5 })
        })
    })
  }
}
</script>
