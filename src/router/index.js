import Vue from 'vue'
import Router from 'vue-router'
// import SecStyle from '@/components/SecStyle'


// Vue.use(Router)

// export default new Router({
//   routes: [
//     {
//       path: '/',
//       name: 'SecStyle',
//       component: SecStyle
//     },

//   ]
// })


import interFace from '@/components/InterFaceStyle'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'interFace',
      component: interFace
    },

  ]
})
