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
    upload(file, onUploadProgress) {
      let formData = new FormData();
      console.log('-44-----------------------------------');
      console.log(file);
      console.log('------------------------------------');
      formData.append("file", file);
      formData.append("ss", "xxxx");
      console.log(formData);
      return axios.post("/files", formData, {
        // headers: {
        //   "Content-Type": "multipart/form-data"
        // },
        onUploadProgress
      });
    }


}
