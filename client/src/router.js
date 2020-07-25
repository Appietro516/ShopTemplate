import Vue from 'vue';
import Router from 'vue-router';
import Products from './components/Products.vue';
import Order from './components/Order.vue';
import OrderComplete from './components/OrderComplete.vue'
import Dashboard from './components/admin/Dashboard.vue'
import ProductManager from './components/admin/ProductManager.vue'
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
      path:'/dashboard',
      name: 'Dashboard',
      component: Dashboard,
    },
    {
      path:'/dashboard/products',
      name: 'Edit',
      component: ProductManager,
    },
    {
      path:'/dashboard/login',
      name: 'Login',
      component: Login,
    },
    {
      path:'/dashboard/logout',
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
    if(!store.getters.isAuthenticated) next({ name: 'Login'});

  } else if (to.name === 'Logout') {
    if (store.getters.isAuthenticated) store.dispatch("clearToken");
    next({ name: 'Products'})
  }
  next()
});

export default router
