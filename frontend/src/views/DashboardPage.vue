<template>
  <div>
    <header class="dashboard-header">
      <div class="logo">MyApp</div>
      <nav class="dashboard-nav">
        <div class="user-menu">
          <img
            src="https://via.placeholder.com/40"
            alt="User Avatar"
            class="avatar"
          />
          <ul class="dropdown">
            <li>Profile</li>
            <li>Settings</li>
            <li>Logout</li>
          </ul>
        </div>
      </nav>
    </header>
    <main class="dashboard-content">
      <section class="dashboard-lists">
        <h2>Lists</h2>
        <ul>
          <li>Item 1</li>
          <li>Item 2</li>
          <li>Item 3</li>
        </ul>
      </section>
      <section class="dashboard-graphs">
        <h2>Graphs</h2>
        <div class="graph-placeholder">Graph goes here</div>
      </section>
    </main>
  </div>
</template>

<script lang="ts">
export default {
  name: 'DashboardPage',
};
</script>
