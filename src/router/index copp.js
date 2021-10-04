import Vue from 'vue'
import Router from 'vue-router'
// import SecStyle from '@/components/SecStyle'
import HelloWorld from '@/components/HelloWorld'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },

  ]
})
