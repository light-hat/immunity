<script>
import {useAuthStore} from '../stores/auth';
import {computed, ref} from 'vue';
import {useRouter} from 'vue-router';

export default {
  setup() {
    const auth = useAuthStore();
    const router = useRouter();

    const username = ref('');
    const email = ref('');
    const password = ref('');
    const re_password = ref(''); // eslint-disable-line
    const error = computed(() => auth.error);
    const loading = computed(() => auth.loading);

    const handleRegister = async () => {
      await auth.register({
        username: username.value,
        email: email.value,
        password: password.value,
        re_password: re_password.value, // eslint-disable-line
      });
      if (!auth.error) {
        router.push('/login');
      }
    };

    return {
      username,
      email,
      password,
      re_password, // eslint-disable-line
      error,
      loading,
      handleRegister,
    };
  },
};
</script>

<template>
    <form @submit.prevent="handleRegister"
            class="uk-position-center uk-center uk-dark">

      <div class="uk-margin">
        <div class="uk-inline">
            <span class="uk-form-icon" uk-icon="icon: user"></span>
            <input v-model="username"
                  type="text"
                  placeholder="Username"
                  class="uk-input"
                  required />
        </div>
      </div>

      <div class="uk-margin">
        <div class="uk-inline">
          <span class="uk-form-icon" uk-icon="icon: mail"></span>
          <input v-model="email"
                type="email"
                placeholder="E-mail"
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

    <div class="uk-margin">
        <div class="uk-inline">
            <span class="uk-form-icon" uk-icon="icon: lock"></span>
            <input v-model="re_password"
                placeholder="Confirm Password"
                type="password"
                class="uk-input"
                required/>
        </div>
    </div>

    <button class="uk-button uk-button-default"
        type="submit" :disabled="loading">
    Регистрация
    </button>

    </form>

    <div v-if="error" class="uk-alert-danger" uk-alert>
      <a href class="uk-alert-close" uk-close></a>
      <p>{{ error }}</p>
    </div>
</template>

<style scoped>
.uk-center {
    text-align: center;
}
</style>
