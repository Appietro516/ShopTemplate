<template>
  <div class="container">
    <link rel="stylesheet" 
        href="https://use.fontawesome.com/releases/v5.2.0/css/all.css" 
        integrity="sha384-hWVjflwFxL6sNzntih27bfxkr27PmbbK/iSvJ+a4+0owXq79v+lsFkW54bOGbiDQ" 
        crossorigin="anonymous">
    <sidebar-menu :menu="menu" width="180px" :hideToggle="true" />
    HI
    <i class="fas fa-coffee"></i>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';



export default {
  data() {
    return {
      menu: [
        {
          header: true,
          title: 'Admin Navigation',
          hiddenOnCollapse: true,
        },
        {
          href: '/',
          title: 'Store',
          icon: 'fas fa-store',
        },
        {
          href: '/Dashboard',
          title: 'Dashboard',
          icon: 'fas fa-chart-line',
        },
        {
          href: '/Dashboard/products',
          title: 'Products',
          icon: 'far fa-edit',
        },
        {
          href: '/dashboard/logout',
          title: 'Logout',
          icon: 'fas fa-sign-out-alt',
        },
      ],
    };
  },
  methods: {
    ...mapActions(['checkAuthenticated'])
  },
  updated() {
    this.checkAuthenticated()
      .then((authenticated) => {
        if(!authenticated) {
          this.$router.push({ name: 'Login'});
        }
      });
  },
};
</script>