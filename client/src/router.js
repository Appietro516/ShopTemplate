import Vue from 'vue';
import Router from 'vue-router';
import Products from './components/Products.vue';
import Order from './components/Order.vue';
import OrderComplete from './components/OrderComplete.vue'
import Dashboard from './components/admin/Dashboard.vue'
import ProductManager from './components/admin/ProductManager.vue'
import OrderManager from './components/admin/OrderManager.vue'
import NotFound from './components/404.vue'
import Login from './components/admin/Login.vue'
import store from '@/store/index'

Vue.use(Router);

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Products',
      component: Products,
    },
    {
      path:'/Order/:id',
      name: 'Order',
      component: Order,
    },
    {
      path: '/Complete/:id',
      name: '/OrderComplete',
      component: OrderComplete,
    },
    {
      path:'/Dashboard',
      name: 'Dashboard',
      component: Dashboard,
    },
    {
      path:'/Dashboard/Products',
      name: 'Edit',
      component: ProductManager,
    },
    {
      path: '/Dashboard/Orders',
      name: 'OrderManager',
      component: OrderManager,
    },
    {
      path:'/Dashboard/Login',
      name: 'Login',
      component: Login,
    },
    {
      path:'/Dashboard/Logout',
      name: 'Logout',
    },
    {
      path: '*',
      component: NotFound,
    }
  ],
});

router.beforeEach((to, from, next) => {

  if(to.name === 'Dashboard' || to.name === 'Edit') {
    store.dispatch('checkAuthenticated')
      .then((authenticated) => {
        if (!authenticated) next({ name: 'Login'});
      });

  } else if (to.name === 'Logout') {
    store.dispatch('checkAuthenticated')
      .then((authenticated) => {
        if (authenticated) store.dispatch("clearToken");
        next({ name: 'Products'})
      });
  }
  next()
});

export default router
