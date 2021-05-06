<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="auto">
        <v-sheet
          color="white"
          rounded="xl"
          elevation="10"
          max-height="240"
          max-width="400"
        >
          <v-img
            max-height="240"
            max-width="400"

            :src="imageUrl"
          ></v-img>
        </v-sheet>
      </v-col>
    </v-row>
    <v-row align-content="stretch">
      <v-col>
        <v-list class="list1">
          <draggable v-model="movies" @change="saveList" class="row">
            <v-col
              cols="12"
              v-for="(item, index) in movies"
              :key="item.filename"
              style="font-weight: bold"
            >
              <div style="width: 50%; float: left">
                {{ item.filename }}
              </div>
              <div style="float: left; width: 200px">
                <v-slider
                  :value="getPostion(item)"
                  min="0"
                  :max="getMax(item)"
                  thumb-label
                  :thumb-size="48"
                  @change="changePostion(item, $event)"
                  persistent-hint
                ></v-slider>
              </div>
              <div style="float: left">
                <mbutton
                  type="brightness"
                  :movie="item"
                  tooltip="brigthness"
                  v-on:saveList="saveList()"
                  icon="mdi-brightness-5"
                >
                </mbutton>
                <mbutton
                  type="contrast"
                  :movie="item"
                  tooltip="contrast"
                  v-on:saveList="saveList()"
                  icon="mdi-contrast-box"
                >
                </mbutton>
              </div>
              <div style="float:left;width=20%">
                <v-icon @click="deleteMovie(item, index)" right large
                  >mdi-delete-forever-outline</v-icon
                >
              </div>
            </v-col>
          </draggable>
        </v-list>
      </v-col>
    </v-row>
  </v-container>
</template>



<script>
import slowMovieApi from "@/services/SlowMovieApi";
import Mbutton from "@/components/menu/mbutton";
// import {Drag,DropList} from "vue-easy-dnd";
import draggable from "vuedraggable";

export default {
  name: "Player",
  components: {
    // Drag,
    // DropList,
    Mbutton,
    draggable
  },
  props: {
    //msg: String
  },
  data() {
    return {
      msg: "testxx",
      total: 0,
      movies: [],
      brigthen: [0, 0.5, 1, 1.5, 2, 2.5, 3],
      imageUrl: this.$baseURL + "/img/paper.jpg"
      // items1: [],
    };
  },
  created() {
    this.interval = setInterval(this.refreshData, 60000);
  },
  beforeDestroy() {
    clearInterval(this.interval);
  },
  mounted() {
    this.getMovies();
  },
  computed: {
    duration: {
      set: function(val) {
        this.movies[1].position = val;
        // If necessary, also copy val into an external variable here
      },
      get: function() {
        return this.movies[1].position;
      }
    }
  },
  methods: {
    brTitel(item) {
      if (typeof item.brightness !== "undefined") {
        return item.brightness;
      }
      return "";
    },
    crTitel(item) {
      if (typeof item.contrast !== "undefined") {
        return item.contrast;
      }
      return "";
    },
    refreshData() {
      this.imageUrl =
        this.$baseURL + "/img/paper.jpg?x=" + new Date().getTime();
    },
    getMovies($state) {
      // this.loading = true

      slowMovieApi
        .fetchMovieCollection(this)
        .then(response => {
          this.total = response.data.meta.count;
          this.movies = response.data.files;
          this.loading = false;
          if ($state) {
            if (!response.data.length) {
              $state.complete();
            }
            $state.loaded();
          }
        })
        .catch(error => {
          console.log(error);
        });
      if ($state) {
        // $state.complete();
      }
    },
    saveList() {
      slowMovieApi
        .updateList(this.movies)
        .then(response => {
          console.log("------------------------------------");
          console.log(this.movies);
          console.log(response);
          console.log("------------------------------------");
        })
        .catch(error => {
          console.log(error);
        });
    },
    deleteMovie(item, index) {
      slowMovieApi
        .delete(item)
        .then(response => {
          console.log("------------------------------------");
          console.log(item);
          console.log(response);
          console.log("------------------------------------");
          this.movies.splice(index, 1);
        })
        .catch(error => {
          console.log(error);
        });
    },
    changePostion(item, value) {
      item.position = value * 25 * 60;
      this.saveList();
    },
    getPostion(item) {
      const i = parseInt(item.position / 25 / 60);
      return i;
    },
    getMax(item) {
      const i = parseInt(item.frame_count / 25 / 60);
      return i;
    },
    changeBr(item, value) {
      item.brightness = value;
      this.saveList();
    },
    changeCr(item, value) {
      item.contrast = value;
      this.saveList();
    }
  },
  watch: {
    "$store.state.listChanged"() {
      //console.log('itemwatch')
      this.getMovies();
      this.$store.commit("setListChanged", false);
    }
  }
};
</script>

<style>
html,
body {
  height: 100%;
  font-family: "Roboto";
}

.list1 {
  height: 100%;
}

.list2 {
  display: flex;
  height: 100%;
}

.chip {
  margin: 10px;
}

.drop-allowed.drop-in * {
  cursor: inherit !important;
}

.v-text-field.v-text-field--solo .v-input__control {
  min-height: 10px;
}

.v-label {
  font-size: 10px;
}
</style>