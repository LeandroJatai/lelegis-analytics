<template>
  <div class="pesquisa-container">
    <div class="resumo-pais">
      <div class="bloco-view">
        <h3 :pk="pesquisa.id">{{pesquisa.title}}</h3>
        <h4>Resumo no País</h4>
        <h5>Total de Endereços Analisados: {{getTotalEnderecoAnalisado}}</h5>
        <small>{{pesquisa.description}}</small>
        <br><small><small>/{{pesquisa.action_view}}</small></small>
        <pie-chart :data="dataPais" :colors="colors"></pie-chart>
        <!--b-table :items="dataPaisTable" /-->
      </div>
      <b-row>
        <b-col md="6" v-for="(tc, key) in tipo_classificacao" :key="`pt${pesquisa.id}${key+1}`">
          <div class="bloco-view">
            <h5>Resumo por {{tc.descr}} dos {{pesquisa.EXEC.pais.ping_true.has_entries}} municípios {{pesquisa.action_view === '' ? 'acessíveis' : 'com registros'}}</h5>
            <small>{{pesquisa.title}}</small>

            <br><small><small>{{pesquisa.description}}</small></small>
            <br><small><small>/{{pesquisa.action_view}}</small></small>
            <pie-chart :data="getData('ping_true', tc.type)" :colors="colors"></pie-chart>
          </div>
        </b-col>
        <template v-if="pesquisa.action_view">
          <b-col md="6"  v-for="(tc, key) in tipo_classificacao" :key="`pf${pesquisa.id}${key+1}`">
            <div class="bloco-view">

            <h5>Resumo por {{tc.descr}} dos {{getTotalEnderecoAnalisado - pesquisa.EXEC.pais.ping_true.has_entries - pesquisa.EXEC.pais.ping_false.has_entries}} municípios sem registros</h5>

             <small>{{pesquisa.title}}</small>
              <br><small><small>{{pesquisa.description}}</small></small>
              <br><small><small>/{{pesquisa.action_view}}</small></small>
              <pie-chart :data="getData('ping_false', tc.type)" :colors="colors"></pie-chart>
            </div>
          </b-col>
        </template>
      </b-row>
    </div>
    <div class="resumo-pais" v-if="false">

    </div>

    <ResumoGraficoRecursive :pesquisa="item" :pesquisa_parent="pesquisa" v-for="(item, key) in childs" :key="key+1"></ResumoGraficoRecursive>

  </div>
</template>
<script>
import Resources from '@/resources'

export default {
  name: 'ResumoGraficoRecursive',
  props: ['pesquisa', 'pesquisa_parent'],
  data () {
    return {
      utils: Resources.Utils,
      init: false,
      childs: [],
      colors: ['#00b', '#eb0', '#b00', '#750', '#757'],
      tipo_classificacao: [
        {
          type: 'regional',
          descr: 'Região'
        },
        {
          type: 'estadual',
          descr: 'Estado'
        }
      ]
    }
  },
  computed: {
    getTotalEnderecoAnalisado: function () {
      if (this.pesquisa_parent === null) {
        return this.pesquisa.EXEC.pais.ping_true.has_entries + this.pesquisa.EXEC.pais.ping_false.has_entries
      } else {
        return this.pesquisa.EXEC.pais.ping_true.count + this.pesquisa.EXEC.pais.ping_false.count
      }
    },
    dataPaisTable: function () {
      const dados = []
      _.each(this.dataPais, function (val) {
        const d = {}
        d['Descrição'] = val[0]
        d.Totais = val[1]
        dados.push(d)
      })
      return dados
    },
    dataPais: function () {
      const dados = []

      const pais = this.pesquisa.EXEC.pais

      if (this.pesquisa.action_view === '') {
        dados.push([`Acessivel = ${pais.ping_true.has_entries}`, pais.ping_true.has_entries])
        dados.push([`Sem Acesso = ${pais.ping_false.has_entries}`, pais.ping_false.has_entries])
      } else {
        dados.push([`Com Dados = ${pais.ping_true.has_entries} (${pais.ping_true.size_entries})`, pais.ping_true.has_entries])
        dados.push([`Sem Dados = ${pais.ping_true.count - pais.ping_true.has_entries}`, pais.ping_true.count - pais.ping_true.has_entries])

        if (pais.ping_false.has_entries !== 0) {
          dados.push([`Erro = ${pais.ping_false.has_entries}`, pais.ping_false.has_entries])
        }
      }

      return dados
    }

  },
  methods: {

    getData: function (tipo_ping, tipo_classificacao) {
      const dados = []
      const t = this

      const lista_de_analise = t.pesquisa.EXEC

      _.each(lista_de_analise[tipo_classificacao], function (value) {
        const item = value[tipo_ping]
        if (t.pesquisa.action_view === '') {
          dados.push([item.meta + ' = ' + item.count, item.count])
        } else {
          if (tipo_ping === 'ping_true') {
            dados.push([`${item.meta} - ${item.has_entries} (${item.size_entries})`, item.has_entries])
          } else {
            dados.push([item.meta + ' = ' + (value.ping_true.count - value.ping_true.has_entries), value.ping_true.count - value.ping_true.has_entries])
          }
        }
      })
      return dados.filter(v => {
        return v[1] > 0
      })
    }

  },

  mounted () {
    const _this = this

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
            time: 5
          })
        })
    })
  }
}
</script>

<style lang="scss">
.pesquisa-container {
  margin: 1rem 0;
}
.pesquisa-view {
  padding: 3rem 1rem 1rem;
  background-color: #fff;
  page-break-before: always
}
.bloco-view {
  border-top: 5px solid #f0f0f0;
  padding: 2rem 0 0;
}

</style>
