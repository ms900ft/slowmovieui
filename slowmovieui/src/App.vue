<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <v-icon>mdi-video-vintage</v-icon>
        <span class="mr-2">Slowmovie</span>

      </div>

      <v-spacer></v-spacer>
    <div >
    <div class="large-12 medium-12 small-12 cell">
      <label>Add
        <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
      </label>
        <button v-on:click="submitFile()">Submit</button>
    </div>
  </div>
    </v-app-bar>

     <v-main class="content">
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
//import Player from './components/Player';
import slowMovieApi from '@/services/SlowMovieApi'
import axios from 'axios'
export default {
  name: 'App',

  components: {
  //  Player,

  },

  data () {
    return {
    currentFile: undefined,
      progress: 0,
      message: "",

      fileInfos: [],
      file: ""
     }
  },
  methods: {
          submitFile(){
        /*
                Initialize the form data
            */
            let formData = new FormData();

            /*
                Add the form data we need to submit
            */
            formData.append('file', this.file);

        /*
          Make the request to the POST /single-file URL
        */
            axios.post( '/files',
                formData,
                {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
              }
            ).then(function(){
          console.log('SUCCESS!!');
        })
        .catch(function(){
          console.log('FAILURE!!');
        });
      },

      /*
        Handles a change on the file upload
      */
      handleFileUpload(){
        this.file = this.$refs.file.files[0];
      },



    selectFile() {
      this.progress = 0;
      this.currentFile = this.$refs.file.files[0];
    },
    upload() {
      if (!this.currentFile) {
        this.message = "Please select a file!";
        return;
      }

      this.message = "";

      slowMovieApi.upload(this.currentFile, (event) => {
        this.progress = Math.round((100 * event.loaded) / event.total);
      })
        .then((response) => {
          this.message = response.data.message;
          //return UploadService.getFiles();
        })
        .then((files) => {
          this.fileInfos = files.data;
        })
        .catch(() => {
          this.progress = 0;
          this.message = "Could not upload the file!";
          this.currentFile = undefined;
        });
    },
  }
}

</script>
