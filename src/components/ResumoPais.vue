<template>
  <div class="pesquisa-container">
    <div class="resumo-pais">
      <div class="bloco-view">
        <h3 :pk="pesquisa.id">{{pesquisa.title}}</h3>
        <h4>Resumo no País</h4>
        <h5>Total de Endereços Analisados: {{pesquisa.ping_true.pais.total + pesquisa.ping_false.pais.total}}</h5>
        <small>{{pesquisa.description}}</small>
        <br><small><small>/{{pesquisa.action_view}}</small></small>
        <pie-chart :data="dataPais" :colors="colors"></pie-chart>
        <!--b-table :items="dataPaisTable" /-->
      </div>

      <b-row v-for="(tc, key) in tipo_classificacao" :key="key+1">
        <b-col md="6">
          <div class="bloco-view">
            <h5 v-if="!pesquisa.action_view">Resumo por {{tc.descr}} dos {{pesquisa.ping_true.pais.total}} Municípios acessíveis</h5>
            <h5 v-if="pesquisa.action_view && pesquisa.ping_true.pais.has_entries !== undefined">Resumo por {{tc.descr}} dos {{pesquisa.ping_true.pais.has_entries}} Municípios com dados</h5>
            <h5 v-if="pesquisa.action_view && pesquisa.ping_true.pais.has_entries === undefined">Resumo por {{tc.descr}} dos {{pesquisa.ping_true.pais.total}} Municípios com dados</h5>
            <small>{{pesquisa.title}}</small>

            <br><small><small>{{pesquisa.description}}</small></small>
            <br><small><small>/{{pesquisa.action_view}}</small></small>
            <pie-chart :data="getData('ping_true', tc.type)" :colors="colors"></pie-chart>
          </div>
        </b-col>
        <b-col md="6">
          <div class="bloco-view">
            <h5 v-if="!pesquisa.action_view">a - Resumo por {{tc.descr}} dos {{pesquisa.ping_false.pais.total}} Municípios sem resposta</h5>
            <h5 v-if="pesquisa.action_view && pesquisa.ping_true.pais.has_entries !== undefined">b - Resumo por {{tc.descr}} dos {{pesquisa.ping_true.pais.total - pesquisa.ping_true.pais.has_entries}} Municípios sem dados</h5>
            <h5 v-if="pesquisa.action_view && pesquisa.ping_true.pais.has_entries === undefined">c - Resumo por {{tc.descr}} dos {{pesquisa.ping_false.pais.total}} Municípios sem dados</h5>
            <small>{{pesquisa.title}}</small>
            <br><small><small>{{pesquisa.description}}</small></small>
            <br><small><small>/{{pesquisa.action_view}}</small></small>
            <pie-chart :data="getData('ping_false', tc.type)" :colors="colors"></pie-chart>
          </div>
        </b-col>
      </b-row>
    </div>

    <ResumoPais :pesquisa="item"  v-for="(item, key) in childs" :key="key+1"></ResumoPais>

  </div>
</template>
<script>
import Resources from '@/resources'

export default {
  name: 'ResumoPais',
  props: ['pesquisa'],
  data () {
    return {
      utils: Resources.Utils,
      init: false,
      childs: [],
      colors: ['#00b', '#b00', '#eb0', '#750', '#757'],
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

      if (this.pesquisa.action_view === '' || this.pesquisa.ping_true.pais.has_entries === undefined) {
        dados.push(['Acessivel = ' + this.pesquisa.ping_true.pais.total, this.pesquisa.ping_true.pais.total])
        dados.push(['Sem Acesso = ' + this.pesquisa.ping_false.pais.total, this.pesquisa.ping_false.pais.total])
      } else {
        if (this.pesquisa.ping_true.pais.has_entries !== undefined) {
          dados.push(['Com Dados = ' + this.pesquisa.ping_true.pais.has_entries, this.pesquisa.ping_true.pais.has_entries])
          dados.push(['Sem Dados = ' + (this.pesquisa.ping_true.pais.total - this.pesquisa.ping_true.pais.has_entries), (this.pesquisa.ping_true.pais.total - this.pesquisa.ping_true.pais.has_entries)])
          dados.push(['Erro = ' + (this.pesquisa.ping_false.pais.total), this.pesquisa.ping_false.pais.total])
        } else {

        }
      }

      return dados
    }

  },
  methods: {

    getData: function (tipo_ping, tipo_classificacao) {
      const dados = []
      const t = this

      const lista_de_analise = t.pesquisa.action_view && t.pesquisa.ping_true.pais.has_entries !== undefined ? t.pesquisa.ping_true : t.pesquisa[tipo_ping]

      const loglog = [tipo_ping, tipo_classificacao, t.pesquisa.action_view]
      console.log(loglog)
      _.each(lista_de_analise[tipo_classificacao], function (value) {
        if (t.pesquisa.action_view === '' || value.has_entries === undefined) {
          dados.push([value.meta + ' = ' + value.total, value.total])
          /* if (tipo_ping === 'ping_true') {
            dados.push([value.meta + ' = ' + value.total, value.total])
          } else {
            dados.push([value.meta + ' = ' + value.total, value.total])
          } */
        } else {
          if (value.has_entries !== undefined) {
            if (tipo_ping === 'ping_true') {
              dados.push([value.meta + ' = ' + value.has_entries, value.has_entries])
            } else {
              dados.push([value.meta + ' = ' + (value.total - value.has_entries), value.total - value.has_entries])
            }
          }
        }
      })
      return dados
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
