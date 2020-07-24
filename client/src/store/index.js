import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios';

Vue.use(Vuex);

/**
 *  NOTE: USE VUEX-PERSISEDSTATE TO SAVE ORDERS IN CACHE
 */

export default new Vuex.Store({
  /***********************************************
   *                  STATE                      *
   ***********************************************/
  state: {
    shoppingCart: [],
    serverName: 'http://localhost:5000',
    jwt: '', 
    tokenType: 'Bearer',
  },
  /***********************************************
   *                MUTATIONS                    *
   ***********************************************/
  mutations: {
    addItem: function (state, item) {
      if(this.state.shoppingCart.some(e => e.id == item.id))
        return false;
      state.shoppingCart.push(item);
      console.log(state.shoppingCart);
    },
    removeItem: function (state, item) {
      state.forEach((cartItem, index, object) => {
        if(cartItem.id == item.id)
          object.splice(index, 1);
      });
    },
    clearList: function (state) {
      state.shoppingCart = [];
    },
    setEmail: function (state, email) {
      state.email = email;
    },
    setJwtToken: function (state, payload)  {
      state.token = payload.jwt.token;
      state.jwt = payload.jwt;
    }
  },
  /***********************************************
   *                 ACTIONS                     *
   ***********************************************/
  actions: {
    containsItem: function ({ commit, state }, item) {
      return state.shoppingCart.some(e => e.id == item.id);
    },
    register: function({ commit, state }, userData) {
      return axios.post(`${state.serverName}/register`, userData);
    },
    login: function ({ commit, state }, userData) {
      return axios.post(`${state.serverName}/login`, userData)
        .then(res => commit('setJwtToken', { jwt: res.data }))
        .catch(error => {
          console.log('Error Authenticating ', error);
        });
    },
    setTokenStr: function({ state }, payload) {
      payload.authorization = `${state.tokenType}: ${state.jwt}`;
    },
    changeProduct: function({ state, dispatch }, payload) {
      dispatch('setTokenStr', payload);
      return axios.put(`${state.serverName}/products/update`, payload);
    },
    insertProduct: function({ state, dispatch }, payload) {
      dispatch('setTokenStr', payload);
      return axios.post(`${state.serverName}/products/new`, payload);
    },
    deleteProduct: function({ state, dispatch }, id) {
      const data = {'id': id}
      dispatch('setTokenStr', data)
      return axios.delete(`${state.serverName}/products/update`);
    }
  },
  /***********************************************
   *                GETTERS                      *
   ***********************************************/
  getters: {
    isAuthenticated: function ({ state }) {
      if (!state.jwt || state.jwt.split('.').length < 3) {
        return false;
      }
      const data = JSON.parse(atob(state.jwt.split('.')[1]));
      const exp = new Date(data.exp * 1000); // JS deals with dates in milliseconds since epoch
      const now = new Date();
      return now < exp;
    },
  },
});
