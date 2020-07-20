import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

/**
 *  NOTE: USE VUEX-PERSISEDSTATE TO SAVE ORDERS IN CACHE
 */

export default new Vuex.Store({
    /***********************************************
     *                   STATE                     *
     ***********************************************/
    state: {
        shoppingCart: [],
        serverName: 'http://localhost:5000'
    },
    /***********************************************
     *                 MUTATIONS                   *
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
    },
    /***********************************************
     *                 ACTIONS                     *
     ***********************************************/
    actions: {
        containsItem: function ({ commit }, item) {
            return state.shoppingCart.some(e => e.id == item.id);
        },
    },
});