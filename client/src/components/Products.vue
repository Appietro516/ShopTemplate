<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Products</h1>
        <hr><br><br>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Price</th>
              <th scope="col">Description</th>  
              <th scope="col">Image</th>            
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(product, index) in products" :key="index">
              <td>{{ product.name }}</td>
              <td>{{ product.price }}</td>
              <td>{{ product.description }}</td>
              <td><img 
                    v-bind:src="product.image"
                    :style="{ height: '50px', width: '80px' }"
                  /></td>
              <td>
                <div class="btn-group" role="group">
                  <button
                      type="button"
                      class="btn btn-warning btn-sm"
                      @click="addToCart(product)">
                    Add To Cart 
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <router-link :to="`/order/1`"
                              class="btn btn-primary btn-sm">
                      Purchase
                  </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapActions, mapState } from 'vuex';

export default {
  data() {
    return {
      products: [],
    };
  },
  computed: {
    ...mapState(['serverName']),
  },
  methods: {
    ...mapActions(['addItem']),
    getProducts() {
      const path = `${this.serverName}/products`;
      axios.get(path)
        .then((res) => {
          this.products = res.data.products;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addToCart(product) {
      this.$store.commit('addItem', product);
    }
  },
  created() {
    this.getProducts();
  },
};
</script>
