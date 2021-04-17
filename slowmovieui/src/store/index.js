import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    listChanged: false,
  },
  actions: {
    getListChanged: function (state) {
      return state.listChanged
    },
  },
  mutations: {
    setListChanged: function (state, value) {
      state.listChanged = value
    },

  },
  getters: {},

})

export default store
