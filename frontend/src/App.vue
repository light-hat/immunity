<script>
import {RouterView} from 'vue-router';
import NavBar from './components/NavBar.vue';
import { ref } from "vue";
import { mapGetters } from "vuex";
import axios from "axios";

export default {
  name: "App",

  setup() {
    const theme = ref("light");
    return {
      theme,
      toggleTheme: () => {
        theme.value = theme.value === "light" ? "dark" : "light";
        localStorage.setItem("theme", theme.value);
      },
    };
  },
  methods: {
    logout() {
      axios.post("/api/v1/token/logout").then((response) => {
        localStorage.removeItem("token");
        this.$store.commit("removeToken");
        this.$router.push("/");
      });
    },
  },
  computed: {
    ...mapGetters({
      isAuthenticated: "isAuthenticated",
    }),
  },
  beforeCreate() {
    this.$store.commit("initializeStore");
    const token = this.$store.state.token;
    if (token) {
      axios.defaults.headers.common["Authorization"] = `Token ${token}`;
    } else {
      axios.defaults.headers.common["Authorization"] = "";
    }
    // load theme from local storage
    if (localStorage.getItem("theme")) {
      this.theme = localStorage.getItem("theme");
    }
  },
};
</script>

<template>
    <NavBar />
    <RouterView />
</template>

<style scoped>

</style>
