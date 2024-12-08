<template>
  <div>
    <h1>Profile</h1>
    <div v-if="user">
      <p>Username: {{ user.username }}</p>
    </div>
    <button @click="handleLogout">Logout</button>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { computed, onMounted  } from 'vue'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const auth = useAuthStore()
    const router = useRouter()
    const user = computed(() => auth.user)

    onMounted(() => {
      if (!auth.user) {
        auth.fetchUser()
      }
    })

    const handleLogout = () => {
      auth.logout()
      router.push('/login')
    }

    return { user, handleLogout }
  }
}
</script>
