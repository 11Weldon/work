<template>
  <div>
    <h2>Tariffs</h2>
    <button @click="loadTariffs">Load Tariffs</button>
    <ul v-if="tariffs.length > 0">
      <li v-for="tariff in tariffs" :key="tariff.id">
        ID: {{ tariff.id }} | Title: {{ tariff.title }}
        <ul>
          FUNCTIONS
          <li v-for="func in tariff.functions" :key="func.id">
            ID: {{ func.id }} | Title: {{ func.title }}
          </li>
        </ul>
        <div>
          <form @submit.prevent="addFunctionToTariff(tariff.id)">
            <h3>Add Function to Tariff</h3>
            <select v-model="tariff.selectedFunctionId">
              <option v-for="func in availableFunctions" :key="func.id" :value="func.id">
                ID: {{ func.id }} | Title: {{ func.title }}
              </option>
            </select>
            <button type="submit">Add Function</button>
          </form>
        </div>
      </li>
    </ul>
    <form @submit.prevent="addTariff">
      <h3>Add New Tariff</h3>
      <input type="text" v-model="newTariff.title" placeholder="Title" required>
      <input type="number" v-model.number="newTariff.id" placeholder="ID" required>
      <button type="submit">Add Tariff</button>
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
          selectedFunctionId: null // Добавляем поле selectedFunctionId для каждого тарифа
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
        await this.loadTariffs(); // Обновляем список тарифов после добавления функции
      } catch (error) {
        console.error('Error adding function to tariff:', error);
      }
    }
  },
  mounted() {
    this.loadTariffs();
    this.loadFunctions(); // Загружаем список функций при загрузке компонента
  }
};
</script>

<style>
/* Add your custom styles here */
</style>
