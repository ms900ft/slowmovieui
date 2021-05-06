<template>
  <v-menu offset-y>
dkdsldksl
      <template v-slot:activator="{ on, attrs }">
        <v-tooltip bottom>
          <template v-slot:activator="{ on: ttip }">
        <v-btn
          color="primary"
          dark
          v-bind="attrs"
          v-on="{...on, ...ttip}"
          style="margin-right: 10px"
        >
        <v-icon v-if="brTitel()===''">{{Icon()}}</v-icon>
          {{brTitel()}}
        </v-btn>
         </template>
          <span>{{tooltip}}</span>
        </v-tooltip>
      </template>
      <v-list>
        <v-list-item
          v-for="(itemx, index) in values"
          :key="index"
           @click="changeBr(itemx)" >

          <v-list-item-title>{{ itemx }}</v-list-item-title>
        </v-list-item>

      </v-list>
    </v-menu>
</template>

<script>

export default {
  name: 'Mbutton',
  components: {
    // Drag,
    // DropList,
    //draggable
  },
  data() {
    return {
    values:  [0,0.5,1,1.5,2,2.5,3],
    itemx: 2,


    }
},
  props: ['tooltip', 'title','movie', 'icon', 'type'],
    methods: {
    brTitel() {
      if (typeof this.movie[this.type] !== 'undefined') {
        return this.movie[this.type];

      }
      return "";
    },
    changeBr(value) {
      this.movie[this.type] = value;
      this.$emit('saveList')
      //this.saveList()
    },
    Icon() {
      return this.icon;
    }
  }
}
</script>

