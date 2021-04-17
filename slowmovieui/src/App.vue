<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <v-icon>mdi-video-vintage</v-icon>
        <span class="mr-2">Slowmovie</span>
      </div>

      <v-spacer></v-spacer>
      <v-spacer></v-spacer>


        <v-progress-linear
        v-if="currentFile"
          v-model="progress"
          color="light-blue"
          height="25"
          reactive
        >
          <strong>{{ progress }} %</strong>
        </v-progress-linear>



      <v-file-input
        v-else
        show-size
        accept=".mp4"
        label="select movie"
        v-model="currentFile"
        single-line
        @change="uploadFile"
      ></v-file-input>

      <!-- <button v-on:click="uploadFile()">Submit</button> -->
    </v-app-bar>

    <v-main class="content">
       <v-alert v-if="message" border="left" color="blue-grey" dismissible dark>
      {{ message }}
    </v-alert>

      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
//import Player from './components/Player';
import slowMovieApi from '@/services/SlowMovieApi';
//import axios from 'axios'
export default {
  name: 'App',

  components: {
    //  Player,
  },

  data() {
    return {
      currentFile: undefined,
      progress: 0,
      message: '',

      fileInfos: [],
      files: []
    };
  },
  methods: {
    uploadFile() {
      if (!this.currentFile) {
        this.message = 'Please select a file!';
        return;
      }
      this.progress = 0;
      this.message = '';

      slowMovieApi
        .upload(this.currentFile, event => {
          this.progress = Math.round((100 * event.loaded) / event.total);
        })
        .then(response => {
          console.log('------------------------------------');
          console.log(response);
          console.log('------------------------------------');
          //this.message = response.data.message;
          this.message = 'file uploaded!';
          this.currentFile = undefined;
          this.$store.commit('setListChanged', true)
               // this.loading = true



          //return UploadService.getFiles();
        })
        .catch(() => {
          this.progress = 0;
          this.message = 'Could not upload the file!';
          this.currentFile = undefined;
        });
    }
  }
};
</script>


<style>

</style>
