<script>
import { mapActions } from 'vuex';

export default {
  name: 'LogoutView',
  async mounted() {
    await this.logout();
    this.$router.push('/login');
  },
  methods: {
    ...mapActions(['logout']),
  },
};
</script>

<template>
  <div class="uk-container uk-margin-top">
    <div class="uk-text-center">
      <h3>Logging out...</h3>
      <div uk-spinner></div>
    </div>
  </div>
</template>
