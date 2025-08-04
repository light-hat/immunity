<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
      error: '',
    };
  },
  computed: {
    ...mapGetters(['loading']),
  },
  methods: {
    ...mapActions(['login']),
    async handleLogin() {
      this.error = '';
      
      if (!this.username || !this.password) {
        this.error = 'Please enter both username and password';
        return;
      }

      const result = await this.login({
        username: this.username,
        password: this.password,
      });

      if (result.success) {
        // Redirect to dashboard on successful login
        this.$router.push('/');
      } else {
        this.error = result.error;
      }
    },
  },
};
</script>

<template>
  <form @submit.prevent="handleLogin"
        class="uk-position-center uk-center uk-dark">

      <div class="uk-margin">
          <div class="uk-inline">
              <span class="uk-form-icon" uk-icon="icon: user"></span>
              <input v-model="username"
                    placeholder="Username"
                    type="text"
                    class="uk-input"
                    required />
          </div>
      </div>

      <div class="uk-margin">
          <div class="uk-inline">
              <span class="uk-form-icon" uk-icon="icon: lock"></span>
              <input v-model="password"
                  placeholder="Password"
                  type="password"
                  class="uk-input"
                  required/>
          </div>
      </div>

      <button class="uk-button uk-button-default"
            type="submit" :disabled="loading">
        {{ loading ? 'Signing in...' : 'Sign In' }}
      </button>

      <div v-if="error" class="uk-alert-danger" uk-alert>
          <a href class="uk-alert-close" uk-close></a>
          <p>{{ error }}</p>
      </div>

  </form>
</template>

<style scoped>
.uk-center {
    text-align: center;
}
</style>
