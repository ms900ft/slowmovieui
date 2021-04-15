<template>

        <v-container fluid>
                <v-row align-content="stretch">
                    <v-col>
                        <v-list three-line class="list1">
                          <draggable v-model="items1" class="row">
<v-col
    cols="12"
    v-for="(item) in items1"
    :key="item.filename"
    style="font-weight:bold"
  >
    {{item.filename}}
     <v-slider
      :value="getPostion(item)"
       min="0"
       :max="getMax(item)"
      thumb-label
      :thumb-size="48"
      @change="changePostion(item,$event)"
      hint="kdskdkdsk"
      persistent-hint
    ></v-slider>

  </v-col>
                          </draggable>

                 <v-btn   @click="saveList()">
                    save
                    <v-icon right >mdi-content-save</v-icon>
                  </v-btn>
                        </v-list>
                    </v-col>
                </v-row>
            </v-container>
</template>



<script>
import slowMovieApi from '@/services/SlowMovieApi'
// import {Drag,DropList} from "vue-easy-dnd";
import draggable from  "vuedraggable"

export default {
  name: 'Player',
  components: {
            // Drag,
            // DropList,
            draggable,

        },
  props: {
    //msg: String

  },
  data () {
    return {
      msg: 'testxx',
      total: 0,
      movies: [],
      items1: [],
      items2:[],
    }
  },
  mounted () {
    this.getMovies()
  },
  computed: {
    duration: {
      set: function(val) {
        this.items1[1].position = val;
        // If necessary, also copy val into an external variable here
      },
      get: function() {
        return this.items1[1].position
      }
    }
  },
  methods: {
    getMovies ($state) {
      // this.loading = true

      slowMovieApi
        .fetchMovieCollection(this)
        .then((response) => {
          //this.wholeResponse.push(...response.data)
          //this.$store.commit('setResultsFound', response.meta.total)
          this.total = response.data.meta.count
          this.items1 = response.data.files
          this.loading = false
          if ($state) {
            if (!response.data.length) {
              $state.complete()
            }
            $state.loaded()
          }
        })
        .catch((error) => {
          console.log(error)
        })
      if ($state) {
        // $state.complete();
      }
    },
    saveList() {
      slowMovieApi
        .updateList(this.items1)
        .then((response) => {
          console.log('------------------------------------');
          console.log(this.items1);
          console.log(response)
          console.log('------------------------------------');
        })
       .catch((error) => {
          console.log(error)
        })
    },
     insert1(event) {
                this.items1.splice(event.index, 0, event.data);
            },
    insert2(event) {
                this.items2.splice(event.index, 0, event.data);
            },
    remove(array, value) {
                let index = array.indexOf(value);
                array.splice(index, 1);
            },
    changePostion(item, value) {
      console.log(value);
      item.position = value * 25 *60;
    },
    getPostion(item) {
      const i = parseInt(item.position / 25 /60);
      console.log(i);
      return i;
    },
    getMax(item) {
      const i = parseInt(item.frame_count / 25 /60);
      console.log(i);
      return i;
    }

  },

}
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
</style>