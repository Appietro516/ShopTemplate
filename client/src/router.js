import Vue from 'vue';
import Router from 'vue-router';
import Products from './components/Products.vue';
import Order from './components/Order.vue';
import OrderComplete from './components/OrderComplete.vue'
import Admin from './components/Admin.vue'

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Products',
      component: Products,
    },
    {
      path:'/order/:id',
      name: 'Order',
      component: Order,
    },
    {
      path: '/complete/:id',
      name: '/OrderComplete',
      component: OrderComplete,
    },
    {
      path:'/admin',
      name: 'Admin',
      component: Admin,
    },
  ],
});
