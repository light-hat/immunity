<script>
import {RouterView} from 'vue-router';
import NavBar from './components/NavBar.vue';
import { ref } from "vue";
import { mapGetters, mapActions } from "vuex";

export default {
  name: "App",
  components: {
    NavBar,
  },
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
    ...mapActions(['logout']),
    async handleLogout() {
      await this.logout();
      this.$router.push('/login');
    },
  },
  computed: {
    ...mapGetters({
      isAuthenticated: "isAuthenticated",
    }),
  },
  beforeCreate() {
    this.$store.commit("initializeStore");
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
