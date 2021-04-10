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


    </v-app-bar>

     <v-main class="content">
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
//import Player from './components/Player';

export default {
  name: 'App',

  components: {
  //  Player,
  },

  data: () => ({
    //
  }),
};
</script>
