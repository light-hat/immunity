<script>
import {useRouter} from 'vue-router';
import {useAuthStore} from '../stores/auth';
import {computed, ref} from 'vue';

export default {
  setup() {
    const auth = useAuthStore();
    const username = ref('');
    const password = ref('');
    const router = useRouter();

    const error = computed(() => auth.error);
    const loading = computed(() => auth.loading);

    const handleLogin = async () => {
      await auth.login({username: username.value, password: password.value});
      if (!auth.error) {
        router.push('/');
      }
    };

    return {username, password, error, loading, handleLogin};
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
        Войти
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
