<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <input v-model="username" type="text" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit" :disabled="loading">Login</button>
    </form>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { computed, ref } from 'vue'

export default {
  setup() {
    const auth = useAuthStore()
    const username = ref('')
    const password = ref('')
    const router = useRouter()

    const error = computed(() => auth.error)
    const loading = computed(() => auth.loading)

    const handleLogin = async () => {
      await auth.login({ username: username.value, password: password.value })
      if (!auth.error) {
        router.push('/')
      }
    }

    return { username, password, error, loading, handleLogin }
  }
}
</script>
