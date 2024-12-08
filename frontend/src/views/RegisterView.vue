<template>
  <div>
    <h1>Register</h1>
    <form @submit.prevent="handleRegister">
      <input v-model="username" type="text" placeholder="Username" required />
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <input v-model="re_password" type="password" placeholder="Confirm Password" required />
      <button type="submit" :disabled="loading">Register</button>
    </form>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const auth = useAuthStore()
    const router = useRouter()

    const username = ref('')
    const email = ref('')
    const password = ref('')
    const re_password = ref('')
    const error = computed(() => auth.error)
    const loading = computed(() => auth.loading)

    const handleRegister = async () => {
      await auth.register({ username: username.value, email: email.value, password: password.value, re_password: re_password.value })
      if (!auth.error) {
        router.push('/login')
      }
    }

    return { username, email, password, re_password, error, loading, handleRegister }
  }
}
</script>
