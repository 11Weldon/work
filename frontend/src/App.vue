<template>
  <div id="app">
    <h1>Client Management System</h1>

    <!-- Navigation Links -->
    <nav>
      <router-link to="/household">Households</router-link> |
      <router-link to="/channels">Channels</router-link> |
      <router-link to="/products">Products</router-link>
    </nav>

    <!-- Router View -->
    <router-view></router-view>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App',
});
</script>

<style>
/* добавьте стили по вашему усмотрению */
</style>
