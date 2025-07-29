import { createStore } from "vuex";

export default createStore({
  state: {
    token: "",
    isAuthenticated: false,
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
    token: (state) => state.token,
  },
  mutations: {
    initializeStore(state) {
      // Check if there is a token
      if (localStorage.getItem("token")) {
        state.token = localStorage.getItem("token");
        state.isAuthenticated = true;
      } else {
        state.token = "";
        state.isAuthenticated = false;
      }
    },
    setToken(state, token) {
      state.token = token;
      localStorage.setItem("token", token);
      state.isAuthenticated = true;
    },
    removeToken(state) {
      state.token = "";
      localStorage.removeItem("token");
      state.isAuthenticated = false;
    },
  },
  actions: {},
  modules: {},
});