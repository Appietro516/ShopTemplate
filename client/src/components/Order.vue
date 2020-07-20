<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Ready to buy?</h1>
        <hr>
        <router-link to="/" class="btn btn-primary">
          Back Home
        </router-link>
        <br><br><br>
        <div class="row">
          <div class="col-sm-6">
            <div>
              <h4>You are buying:</h4>
              <ul>
                <li>Item: <em>{{ product.name }}</em></li>
                <li>Amount: <em>${{ product.price }}</em></li>
              </ul>
            </div>
            <div>
              <h4>Use this info for testing:</h4>
              <ul>
                <li>Card Number: 4242424242424242</li>
                <li>Bad Number: 4000002760003184</li>
                <li>CVC Code: any three digits</li>
                <li>Expiration: any date in the future</li>
              </ul>
            </div>
          </div>
          <div class="col-sm-6">
            <h3>One time payment</h3>
            <br>
            <form>
              <div class="form-group">
                <label>Credit Card Info</label>
                <input type="text"
                       class="form-control"
                       placeholder="XXXXXXXXXXXXXXXX"
                       v-model="card.number"
                       required>
              </div>
              <div class="form-group">
                <input type="text"
                       class="form-control"
                       placeholder="CVC"
                       v-model="card.cvc"
                       required>
              </div>
              <div class="form-group">
                <label>Card Expiration Date</label>
                <input type="text"
                       class="form-control"
                       placeholder="MM/YY"
                       v-model="card.exp"
                       required>
              </div>
              <button @click.prevent="validate" 
                      class="btn btn-primary btn-block"
                      :disabled="stripeCheck">
                    Submit
                </button>
            </form>
            <div v-show="errors">
                <br>
                <ul class="text-danger">
                    <li v-for="(error, index) in errors" :key="index">
                        {{ error }}
                    </li>
                </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';

export default {
  data() {
    return {
      product: {
        name: '',
        price: '',
        description: '',
        image: ''
      },
      card: {
        number: '',
        cvc: '',
        exp: '',
      },
      errors: [],
      stripePublishableKey: 'pk_test_51H6Q2LHxVqe5J3VbRnN0TFtd8e6v09aA5UfloeoQBETwRqv9g2pT90Y0ihlwn2be2SVKzOZ1wgW32gnWOihKQCGI00Oe4EURlY',
      stripeCheck: false,
    };
  },
  computed: {
    ...mapState(['serverName']),
  },
  methods: {
    getProducts() {
      const path = `${this.serverName}/products/${this.$route.params.id}`;
      axios.get(path)
        .then((res) => {
          this.product = res.data.product;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    validate() {
      this.errors = [];
      let valid = true;
      if(!this.card.number) {
        valid = false;
        this.errors.push('Card Number is required');
      }
      if(!this.card.cvc) {
        valid = false;
        this.errors.push('Expiration date is required');
      }
      if(!this.card.exp) {
        valid = false;
        this.errors.push('Expiration date is required');
      }
      if (valid) {
        this.createToken();
      }
    },
    createToken() {
      this.stripeCheck = true;
      window.Stripe.setPublishableKey(this.stripePublishableKey);
      window.Stripe.createToken(this.card, (status, response) => {
        if(response.error) {
          this.stripeCheck = false;
          this.errors.push(response.error.message);
          console.error(response);
        } else {
          const payload = {
            product: this.product,
            token: response.id,
          }
          const path = `${this.serverName}/charge`;
          axios.post(path, payload)
            .then((res) => {
              this.$router.push({ path: `/complete/${res.data.charge.id}` });
            })
            .catch((error) => {
              this.stripeCheck = false;
              this.errors.push(error.response.data.message)
              console.error(error);
            });
        }
      });
    },
  },
  created() {
    this.getProducts();
  },
};
</script>