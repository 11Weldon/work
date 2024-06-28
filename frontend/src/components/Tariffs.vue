<template>
  <div class="tariffs-container">
    <h2>Tariffs</h2>
    <button class="action-button" @click="loadTariffs">Load Tariffs</button>
    <ul v-if="tariffs.length > 0" class="tariffs-list">
      <li v-for="tariff in tariffs" :key="tariff.id" class="tariff-item">
        <div class="tariff-info">
          <span>ID: {{ tariff.id }}</span> | <span>Title: {{ tariff.title }}</span>
          <button class="action-button delete-tariff" @click="deleteTariff(tariff.id)">Delete Tariff</button>
          <ul class="functions-list">
            <li v-for="func in tariff.functions" :key="func.id" class="function-item">
              <span>ID: {{ func.id }}</span> | <span>Title: {{ func.title }}</span>
              <button class="action-button delete-function" @click="deleteFunctionFromTariff(tariff.id, func.id)">Delete Function</button>
            </li>
          </ul>
          <form @submit.prevent="addFunctionToTariff(tariff.id)" class="add-function-form">
            <h3>Add Function to Tariff</h3>
            <select v-model="tariff.selectedFunctionId" class="function-select">
              <option v-for="func in availableFunctions" :key="func.id" :value="func.id">
                ID: {{ func.id }} | Title: {{ func.title }}
              </option>
            </select>
            <button type="submit" class="action-button">Add Function</button>
          </form>
        </div>
      </li>
    </ul>
    <form @submit.prevent="addTariff" class="add-tariff-form">
      <h3>Add New Tariff</h3>
      <input type="text" v-model="newTariff.title" placeholder="Title" required>
      <input type="number" v-model.number="newTariff.id" placeholder="ID" required>
      <button type="submit" class="action-button">Add Tariff</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Tariffs',
  data() {
    return {
      tariffs: [],
      newTariff: {
        title: '',
        id: null
      },
      availableFunctions: []
    };
  },
  methods: {
    async loadTariffs() {
      try {
        const response = await axios.get('http://localhost:8000/tariffs/');
        this.tariffs = response.data.map(tariff => ({
          ...tariff,
          selectedFunctionId: null // Add selectedFunctionId field for each tariff
        }));
      } catch (error) {
        console.error('Error loading tariffs:', error);
      }
    },
    async addTariff() {
      try {
        const response = await axios.post('http://localhost:8000/tariff/', this.newTariff);
        console.log('Added tariff:', response.data);
        this.tariffs.push({...response.data, selectedFunctionId: null});
        this.newTariff = {title: '', id: null};
      } catch (error) {
        console.error('Error adding tariff:', error);
      }
    },
    async loadFunctions() {
      try {
        const response = await axios.get('http://localhost:8000/function/');
        this.availableFunctions = response.data;
      } catch (error) {
        console.error('Error loading functions:', error);
      }
    },
    async addFunctionToTariff(tariffId) {
      try {
        const selectedFunctionId = this.tariffs.find(t => t.id === tariffId).selectedFunctionId;
        await axios.post(`http://localhost:8000/tariff/${tariffId}/function/${selectedFunctionId}/`);
        await this.loadTariffs(); // Reload tariffs after adding function
      } catch (error) {
        console.error('Error adding function to tariff:', error);
      }
    },
    async deleteTariff(tariffId) {
      try {
        const response = await axios.delete(`http://localhost:8000/tariff/${tariffId}/`);
        console.log(response.data.message);
        this.loadTariffs(); // Reload tariffs after deletion
      } catch (error) {
        console.error('Error deleting tariff:', error);
      }
    },
    async deleteFunctionFromTariff(tariffId, functionId) {
      try {
        const response = await axios.delete(`http://localhost:8000/tariff/${tariffId}/function/${functionId}/`);
        console.log(response.data.message);
        await this.loadTariffs(); // Reload tariffs after deleting function from tariff
      } catch (error) {
        console.error('Error deleting function from tariff:', error);
      }
    }
  },
  mounted() {
    this.loadTariffs();
    this.loadFunctions(); // Load functions when the component is mounted
  }
};
</script>

<style scoped>
.tariffs-container {
  margin-bottom: 20px;
  margin-right: 50%;
}

.tariffs-list {
  list-style-type: none;
  padding: 0;
}

.tariff-item {
  border: 1px solid #ccc;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 8px;
}

.tariff-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.functions-list {
  list-style-type: none;
  padding: 0;
  margin-top: 5px;
}

.function-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.add-function-form {
  margin-top: 10px;
}

.function-select {
  margin-right: 10px;
}

.add-tariff-form {
  margin-top: 20px;
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

.delete-tariff {
  background-color: #dc3545;
}

.delete-tariff:hover {
  background-color: #c82333;
}

.delete-function {
  background-color: #dc3545;
}

.delete-function:hover {
  background-color: #c82333;
}
</style>
