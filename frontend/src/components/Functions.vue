<template>
  <div>
    <h2>Functions</h2>
    <button @click="loadFunctions">Load Functions</button>
    <ul v-if="functions.length > 0">
      <li v-for="func in functions" :key="func.id">
        ID: {{ func.id }} | Title: {{ func.title }}
      </li>
    </ul>
    <form @submit.prevent="addFunction">
      <h3>Add New Function</h3>
      <input type="text" v-model="newFunction.title" placeholder="Title" required>
      <input type="number" v-model.number="newFunction.id" placeholder="ID" required>
      <button type="submit">Add Function</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Functions',
  data() {
    return {
      functions: [],
      newFunction: {
        title: '',
        id: null
      }
    };
  },
  methods: {
    async loadFunctions() {
      try {
        const response = await axios.get('http://localhost:8000/function/');
        this.functions = response.data;
      } catch (error) {
        console.error('Error loading functions:', error);
      }
    },
    async addFunction() {
      try {
        const response = await axios.post('http://localhost:8000/function/', this.newFunction);
        console.log('Added function:', response.data);
        this.functions.push(response.data);
        this.newFunction = {title: '', id: null};
      } catch (error) {
        console.error('Error adding function:', error);
      }
    }
  }
};
</script>

<style>
/* Add your custom styles here */
</style>
