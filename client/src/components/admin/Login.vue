<template>
  <div>

  <input type="text" name="username" v-model="input.email" placeholder="Username" />
        <input type="password" name="password" v-model="input.password" placeholder="Password" />
        <button type="button" v-on:click="login()">Login</button>

  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  data() {
    return {
      name: 'login',
      input: {
        email: '',
        password: '',
      },
    };
  },
  methods: {
    ...mapActions(['postLogin', 'checkAuthenticated']),
    login() {
      this.postLogin(this.input)
        .then(() => {
          this.$router.push({ name: 'Dashboard'})
        })
        .catch((error) => {
          console.log(error)
        })
    },
  },
  created() {
    this.checkAuthenticated()
      .then((authenticated) => {
        if(authenticated) {
          this.$router.push({ name: 'Dashboard'})
        }
      });
  },
};
</script>