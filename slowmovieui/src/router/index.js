import Vue from 'vue'
import VueRouter from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Player from '@/components/Player'
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

Vue.use(VueRouter)

export const router = new VueRouter({
  routes: [{
      path: '/',
      name: 'ListMovie',
      props: (route) => ({
        show: route.query.show,
        orderby: route.query.orderby,
        genre: route.query.genre,
        country: route.query.country,
        cast: route.query.cast,
        crew: route.query.crew,
        person: route.query.person
      }),
      component: HelloWorld
  },
  {
    path: '/player',
    name: 'Player',
    props: (route) => ({
      show: route.query.show,
      orderby: route.query.orderby,
      genre: route.query.genre,
      country: route.query.country,
      cast: route.query.cast,
      crew: route.query.crew,
      person: route.query.person
    }),
    component: Player
  },
  ],
  mode: 'history',
  base: '/'
})