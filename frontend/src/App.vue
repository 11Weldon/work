<template>
  <div id="app">
    <h1>Client Management System</h1>

    <!-- Navigation Links -->
    <nav>
      <router-link to="/clients">Clients</router-link> |
      <router-link to="/channels">Channels</router-link> |
      <router-link to="/bundles">Bundles</router-link>
    </nav>

    <!-- Router View -->
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
/* добавьте стили по вашему усмотрению */
</style>
