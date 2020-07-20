<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Product Management</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.product-modal>Add Product</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Description</th>
              <th scope="col">Price</th>
              <th scope="col">Image</th>
              <th></th>
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
                  /></td>
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
        <b-form-group id="form-title-group"
                      label="Name:"
                      label-for="form-title-input">
            <b-form-input id="form-title-input"
                          type="text"
                          v-model="addProductForm.name"
                          required
                          placeholder="Enter Name">
            </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="Description:"
                      label-for="form-author-input">
          <b-form-input id="form-author-input"
                        type="text"
                        v-model="addProductForm.description"
                        required
                        placeholder="Enter Description">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-price-group"
                      label="Purchase price:"
                      label-for="form-price-input">
          <b-form-input id="form-price-input"
                        type="number"
                        step="0.01"
                        v-model="addProductForm.price"
                        required
                        placeholder="Enter price">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="Image URL:"
                      label-for="form-author-input">
          <b-form-input id="form-author-input"
                        type="text"
                        v-model="addProductForm.image"
                        required
                        placeholder="Enter a valid image URL">
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
        <b-form-group id="form-title-edit-group"
                      label="Name:"
                      label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-edit-group"
                      label="Description:"
                      label-for="form-author-edit-input">
          <b-form-input id="form-author-edit-input"
                        type="text"
                        v-model="editForm.description"
                        required
                        placeholder="Enter Description">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-price-edit-group"
                      label="Purchase price:"
                      label-for="form-price-edit-input">
          <b-form-input id="form-price-edit-input"
                        type="number"
                        step="0.01"
                        v-model="editForm.price"
                        required
                        placeholder="Enter price">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-edit-group"
                      label="Image URL:"
                      label-for="form-author-edit-input">
          <b-form-input id="form-author-edit-input"
                        type="text"
                        v-model="editForm.image"
                        required
                        placeholder="Enter a valid image URL">
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
import { mapState } from 'vuex';

export default {
  data() {
    return {
      products: [],
      addProductForm: {
        name: '',
        price: '',
        description: '',
        image: '',
      },
      message: '',
      showMessage: false,
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
    getProducts() {
      const path = `${this.serverName}/products`;
      axios.get(path)
        .then((res) => {
          this.products = res.data.products;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addProduct(payload) {
      const path = `${this.serverName}/products/new`;
      axios.post(path, payload)
        .then(() => {
          this.getProducts();
          this.message = 'Product added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
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
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addProductModal.hide();
      const payload = {
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
        name: this.editForm.name,
        price: this.editForm.price,
        description: this.editForm.description,
        image: this.editForm.image,
      };
      this.updateProduct(payload, this.editForm.id);
    },
    updateProduct(payload, id) {
      const path = `${this.serverName}/products/${id}/update`;
      axios.put(path, payload)
        .then(() => {
          this.getProducts();
          this.message = 'Product updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
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
      const path = `${this.serverName}/products/${id}/update`;
      axios.delete(path)
        .then(() => {
          this.getProducts();
          this.message = 'Product removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
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