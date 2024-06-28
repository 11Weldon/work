<template>
  <div>
    <h2>Functions</h2>
    <button class="action-button" @click="loadFunctions">Load Functions</button>
    <ul v-if="functions.length > 0" class="functions-list">
      <li v-for="func in functions" :key="func.id" class="function-item">
        ID: {{ func.id }} | Title: {{ func.title }}
        <button class="action-button delete-function" @click="deleteFunction(func.id)">Delete Function</button>
      </li>
    </ul>
    <form @submit.prevent="addFunction" class="add-function-form">
      <h3>Add New Function</h3>
      <input type="text" v-model="newFunction.title" placeholder="Title" required>
      <input type="number" v-model.number="newFunction.id" placeholder="ID" required>
      <button type="submit" class="action-button">Add Function</button>
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
    },
    async deleteFunction(functionId) {
      try {
        const response = await axios.delete(`http://localhost:8000/function/${functionId}/`);
        console.log(response.data.message);
        await this.loadFunctions(); // Reload functions after deletion
      } catch (error) {
        console.error('Error deleting function:', error);
      }
    }
  },
  mounted() {
    this.loadFunctions();
  }
};
</script>

<style scoped>
.functions-list {
  list-style-type: none;
  padding: 0;
  margin-right: 50%;
}

.function-item {
  border: 1px solid #ccc;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.action-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 14px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.action-button:hover {
  background-color: #0056b3;
}

.delete-function {
  background-color: #dc3545;
}

.delete-function:hover {
  background-color: #c82333;
}

.add-function-form {
  margin-top: 20px;
}

.action-button[type="submit"] {
  background-color: #28a745;
}

.action-button[type="submit"]:hover {
  background-color: #218838;
}
</style>
