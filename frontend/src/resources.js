import axios from 'axios'
const basePath = 'http://localhost:9000/api'

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

export default {
  Utils: {
    getModelOrderedList: (app, model, ordering = '', page = 1, query_string = '') => axios({
      url: `${basePath}/${app}/${model}/?o=${ordering}&page=${page}${query_string}`,
      method: 'GET'
    }),
    getModelList: (app, model, page = 1) => axios({
      url: `${basePath}/${app}/${model}/?page=${page}`,
      method: 'GET'
    }),
    getPesquisa: (id = '') => axios({
      url: `${basePath}/pesquisa/${id}`,
      method: 'GET'
    })
  }
}
