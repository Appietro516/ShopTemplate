import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios';
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

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
   *            SESSION STORAGE                  *
   ***********************************************/
  plugins: [createPersistedState({
    storage: window.sessionStorage
  })],
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
    setToken: function (state, payload)  {
      state.jwt = payload.jwt.token;
    },
    clearToken: function(state) {
      state.jwt = '';
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
    postLogin: function ({ commit, state }, userData) {
      console.log("post")
      return axios.post(`${state.serverName}/login`, userData)
        .then(res => commit('setToken', { jwt: res.data }))
    },
    setTokenStr: function({ state }, payload) {
      payload.authorization = `${state.tokenType}: ${state.jwt}`;
      console.log(payload)
    },
    changeProduct: function({ state, dispatch }, {payload, id}) {
      dispatch('setTokenStr', payload);
      return axios.put(`${state.serverName}/products/${id}/update`, payload);
    },
    insertProduct: function({ state, dispatch }, payload) {
      dispatch('setTokenStr', payload);
      return axios.post(`${state.serverName}/products/new`, payload);
    },
    deleteProduct: function({ state, dispatch }, id) {
      const data = {}
      dispatch('setTokenStr', data)
      return axios.delete(`${state.serverName}/products/${id}/update`, {data: data});
    },
    clearToken: function({ state, commit }) {
      commit('clearToken');
    }
  },
  /***********************************************
   *                GETTERS                      *
   ***********************************************/
  getters: {
    isAuthenticated: function (state) {
      console.log("jwt: " + state.jwt)
      if (!state.jwt || state.jwt.split('.').length < 3) {
        return false;
      }
      const data = JSON.parse(atob(state.jwt.split('.')[1]));
      const exp = new Date(data.exp * 1000);
      const now = new Date();
      return now < exp;
    },
  },
});
