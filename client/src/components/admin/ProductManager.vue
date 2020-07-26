<template>
  <div class="container">
    <link rel="stylesheet" 
        href="https://use.fontawesome.com/releases/v5.2.0/css/all.css" 
        integrity="sha384-hWVjflwFxL6sNzntih27bfxkr27PmbbK/iSvJ+a4+0owXq79v+lsFkW54bOGbiDQ" 
        crossorigin="anonymous">
    <sidebar-menu :menu="menu" />
    <h1>Products</h1>
    <hr><br><br>
    <div class="row">
      
      <div class="col-sm-10">
        <b-alert
          :show="showMessage"
          variant="success"
        >
          {{ message }}
        </b-alert>
        <b-alert
          :show="showErrorMessage"
          variant="danger"
        >
          {{ errorMessage }}
        </b-alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.product-modal>Add Product</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th v-for="key in productKeys" v-bind:key="key.name">
                {{ key.name }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(product, index) in products" :key="index">
              <td>{{ product.name }}</td>
              <td>{{ product.description }}</td>
              <td>${{ product.price }}</td>
              <td><img 
                    v-bind:src="product.image"
                    :style="{ height: '50px', width: '80px' }"
                  />
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.product-update-modal
                          @click="editProduct(product)">
                      Update
                  </button>
                  <button type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteProduct(product)">
                      Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <!-- add product modal -->
    <b-modal ref="addProductModal"
            id="product-modal"
            title="Add a new Product"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">

        <b-form-group 
          v-for="item in productKeys"
          v-bind:key="item.name"
          :id="`form-${item.name}-group`"
          :label="item.name"
          :label-for="`form-${item.name}-input`"
        >
          <b-form-input
            :id="`form-${item.name}-input`"
            :type="item.type"
            :step="item.step"
            v-model="addProductForm[item.name]"
            required 
            :placeholder="item.message"
          >
          </b-form-input>
        </b-form-group>

        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <!-- edit product modal -->
    <b-modal ref="editProductModal"
             id="product-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">

        <b-form-group 
          v-for="item in productKeys"
          v-bind:key="item.name"
          :id="`form-${item.name}-edit-group`"
          :label="item.name"
          :label-for="`form-${item.name}-edit-input`"
        >
          <b-form-input
            :id="`form-${item.name}-edit-input`"
            :type="item.type"
            :step="item.step"
            v-model="editForm[item.name]"
            required 
            :placeholder="item.message"
          >
          </b-form-input>
        </b-form-group>

        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import { mapState, mapActions } from 'vuex';

export default {
  data() {
    return {
       menu: [
        {
          header: true,
          title: 'Main Navigation',
          hiddenOnCollapse: true
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
      productKeys: [
        {
          'name': 'name',
          'type': 'text',
          'message': 'Enter name',
        },
        {
          'name': 'description',
          'type': 'text',
          'message': 'Enter Description',
        },
        {
          'name': 'price',
          'type': 'number',
          'step': '0.01',
          'message': 'Enter price',
        },
        {
          'name': 'image',
          'type': 'text',
          'message': 'Enter a valid image URL',
        },
      ],
      products: [],
      addProductForm: {
        name: '',
        price: '',
        description: '',
        image: '',
      },
      message: '',
      showMessage: false,
      errorMessage: '',
      showErrorMessage: false,
      editForm: {
        id: '',
        name: '',
        price: '',
        description: '',
        image: '',
      },
    };
  },
  components: {
    alert: Alert,
  },
  computed: {
    ...mapState(['serverName']),
  },
  methods: {
    ...mapActions([
      'login',
      'changeProduct',
      'insertProduct',
      'deleteProduct',
    ]),
    getProducts() {
      const path = `${this.serverName}/products`;
      axios.get(path)
        .then((res) => {
          this.products = res.data.products;
        })
        .catch((error) => {
          this.displayError(error.response.data.message);
        });
    },
    addProduct(payload) {
      this.insertProduct(payload)
        .then(() => {
          this.getProducts();
          this.message = 'Product added!';
          this.showMessage = true;
        })
        .catch((error) => {
          this.displayError(error.response.data.message);
          this.getProducts();
        });
    },
    initForm() {
      this.addProductForm.id = '';
      this.addProductForm.name = '';
      this.addProductForm.price = '';
      this.addProductForm.description = '';
      this.addProductForm.image = '';
      this.editForm.id = '';
      this.editForm.name = '';
      this.editForm.price = '';
      this.editForm.description = '';
      this.editForm.image = '';
    },
    displaySuccess(message) {
      this.message = message;
      this.showMessage = true;
      setTimeout(() => this.showMessage = false, 2000);
    },
    displayError(message) {
      this.errorMessage = message;
      this.showErrorMessage = true;
      setTimeout(() => this.showErrorMessage = false, 2000);
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addProductModal.hide();
      const payload = {
        id: this.addProductForm.id,
        name: this.addProductForm.name,
        price: this.addProductForm.price,
        description: this.addProductForm.description,
        image: this.addProductForm.image,
      };
      this.addProduct(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addProductModal.hide();
      this.initForm();
    },
    editProduct(product) {
      this.editForm = product;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editProductModal.hide();
      const payload = {
        id: this.editForm.id,
        name: this.editForm.name,
        price: this.editForm.price,
        description: this.editForm.description,
        image: this.editForm.image,
      };
      this.updateProduct(payload, this.editForm.id);
    },
    updateProduct(payload, id) {
      this.changeProduct({ payload, id})
        .then(() => {
          this.getProducts();
          this.displaySuccess('Product updated');
        })
        .catch((error) => {
          this.displayError(error.response.data.message);
          this.getProducts();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editProductModal.hide();
      this.initForm();
      this.getProducts();
    },
    removeProduct(id) {
      this.deleteProduct(id) 
        .then(() => {
          this.getProducts();
          this.displaySuccess('Product removed');
        })
        .catch((error) => {
          this.displayError(error.response.data.message);
          this.getProducts();
        });
    },
    onDeleteProduct(product) {
      this.removeProduct(product.id);
    },
  },
  created() {
    this.getProducts();
  },
};
</script>