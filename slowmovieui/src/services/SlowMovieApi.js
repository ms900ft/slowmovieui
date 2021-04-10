import axios from 'axios'
//import _ from 'lodash'
//import authHeader from './auth-header'


export default {

  async fetchMovieCollection() {
    const response = await axios.get('/files', {
    })
    return response
  },
  updateList(list) {
  return axios.put('/files/list', list,{

    })
    .then(response => {
      return response
    })
}

}
