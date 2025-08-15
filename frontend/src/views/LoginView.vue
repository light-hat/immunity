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
  <div class="uk-container uk-container-small uk-margin-large-top uk-animation-toggle">
    <div class="uk-card uk-card-default uk-card-body uk-width-1-2@m uk-margin-auto uk-position-center uk-center">
      <h3 class="uk-card-title uk-text-center" >Sign In</h3>
      
      <form @submit.prevent="handleLogin">
        <div class="uk-margin">
          <div class="uk-inline uk-width-1-1">
            <span class="uk-form-icon" uk-icon="icon: user"></span>
            <input 
              v-model="username"
              placeholder="Username"
              type="text"
              class="uk-input"
              required 
            />
          </div>
        </div>

        <div class="uk-margin">
          <div class="uk-inline uk-width-1-1">
            <span class="uk-form-icon" uk-icon="icon: lock"></span>
            <input 
              v-model="password"
              placeholder="Password"
              type="password"
              class="uk-input"
              required
            />
          </div>
        </div>

        <div class="uk-margin">
          <button 
            class="uk-button uk-button-primary uk-width-1-1"
            type="submit" 
            :disabled="loading"
          >
            <span uk-spinner v-if="loading"></span>
            <span v-else uk-icon="icon: sign-in"></span>
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </div>

        <div v-if="error" class="uk-alert-danger" uk-alert>
          <a href="#" class="uk-alert-close" uk-close></a>
          <p>{{ error }}</p>
        </div>
      </form>
    </div>
  </div>
</template>
