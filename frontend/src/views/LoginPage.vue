<script setup lang="ts">
import { Button } from '@/components/ui/button';
</script>

<template>
  <div class="auth-container">
    <form class="auth-form">
      <h2>Login</h2>
      <input type="email" placeholder="Email" />
      <input type="password" placeholder="Password" />
      <Button>Click me</Button>
    </form>
  </div>
</template>

<script lang="ts">
export default {
  name: 'LoginPage',
};
</script>
