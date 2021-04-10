<template>

        <v-container fluid>
                <v-row align-content="stretch">
                    <v-col>
                        <v-list three-line class="list1">
                            <drop-list :items="items1" @reorder="$event.apply(items1)" @insert="insert1" mode="cut">
                                <template v-slot:item="{item, reorder}">
                                    <drag :key="item.filename" :data="item" @cut="remove(items1, item)">
                                        <v-list-item style="background-color: white"
                                                     :style="reorder ? {borderLeft: '2px solid #1976D2', marginLeft:'-2px'} : {}">
                                            <v-list-item-avatar>
                                                 <v-icon>mdi-video-vintage</v-icon>
                                            </v-list-item-avatar>
                                            <v-list-item-content>
                                                <v-list-item-title v-html="item.filename"/>
                                                <!-- <v-list-item-subtitle v-html="item.subtitle"/> -->
                                            </v-list-item-content>
                                        </v-list-item>
                                        <v-divider/>
                                    </drag>
                                </template>
                                <template v-slot:inserting-drag-image="{data}">
                                    <v-list-item-avatar style="transform:translate(-50%, -50%) scale(1.5)">
                                        <img :src="data.avatar">
                                    </v-list-item-avatar>
                                </template>
                                <template v-slot:reordering-drag-image/>
                                <template v-slot:feedback="{data}">
                                    <v-skeleton-loader
                                            type="list-item-avatar-three-line"
                                            :key="data.title"
                                            style="border-left: 2px solid #1976D2; margin-left: -2px;"
                                    />
                                </template>
                            </drop-list>
                        </v-list>
                    </v-col>

                </v-row>
                 <v-btn   @click="saveList()">
                    save
                    <v-icon right >mdi-content-save</v-icon>
                  </v-btn>
            </v-container>
</template>



<script>
import slowMovieApi from '@/services/SlowMovieApi'
import {Drag,DropList} from "vue-easy-dnd";

export default {
  name: 'Player',
  components: {
            Drag,
            DropList,

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