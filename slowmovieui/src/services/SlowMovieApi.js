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
  },
  delete(item) {
    return axios.delete('/files/'+ item.filename, {

      })
      .then(response => {
        return response
      })
  },
    upload(file, onUploadProgress) {
      let formData = new FormData();
      formData.append("file", file);
      console.log(formData);
      return axios.post("/files", formData, {
        // headers: {
        //   "Content-Type": "multipart/form-data"
        // },
        onUploadProgress
      });
    }


}
