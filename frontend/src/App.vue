<template>
  <div id="app">
    <createChannel />
  </div>
</template>

<script>
import createChannel from '@/components/Сhannel.vue'; // Проверьте путь импорта

export default {
  name: 'App',
  components: {
    createChannel
  }
};
</script>

<style>
/* Ваши стили по умолчанию */
</style>
