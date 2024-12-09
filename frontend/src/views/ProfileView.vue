<script>
import {useAuthStore} from '../stores/auth';
import {computed, onMounted} from 'vue';
import {useRouter} from 'vue-router';

export default {
  setup() {
    const auth = useAuthStore();
    const router = useRouter();
    const user = computed(() => auth.user);

    onMounted(() => {
      if (!auth.user) {
        auth.fetchUser();
      }
    });

    const handleLogout = () => {
      auth.logout();
      router.push('/login');
    };

    return {user, handleLogout};
  },
};
</script>

<template>
  <div class="uk-container uk-position-center uk-center">
    <h1>Профиль</h1>
    <div v-if="user">
      <p>Username: {{ user.username }}</p>
    </div>
    <button class="uk-button uk-button-default" @click="handleLogout">
        Выйти
    </button>
  </div>
</template>

<style scoped>
.uk-center {
    text-align: center;
}
</style>
