<template>
  <div>
    <h2>Clients</h2>
    <button @click="loadClients">Load Clients</button>
    <ul v-if="clients.length > 0">
      <li v-for="client in clients" :key="client.id">
        ID: {{ client.id }} | Name: {{ client.name }} | Balance: {{ client.balance }}
        <ul>
          Tariffs:
          <li v-for="tariff in client.tariffs" :key="tariff.id">
            ID: {{ tariff.id }} | Title: {{ tariff.title }}
          </li>
        </ul>
        <div>
          <form @submit.prevent="addTariffToClient(client.id, client.selectedTariffId)">
            <h3>Add Tariff to Client</h3>
            <select v-model="client.selectedTariffId">
              <option v-for="tariff in availableTariffs" :key="tariff.id" :value="tariff.id">ID: {{ tariff.id }} | Title: {{ tariff.title }}</option>
            </select>
            <button type="submit">Add Tariff</button>
          </form>
        </div>
      </li>
    </ul>
    <form @submit.prevent="addClient">
      <h3>Add New Client</h3>
      <input type="text" v-model="newClient.name" placeholder="Name" required>
      <input type="number" v-model.number="newClient.id" placeholder="ID" required>
      <input type="number" v-model.number="newClient.balance" placeholder="Balance" required>
      <button type="submit">Add Client</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Clients',
  data() {
    return {
      clients: [],
      newClient: {
        name: '',
        id: null,
        balance: null
      },
      availableTariffs: []
    };
  },
  methods: {
    async loadClients() {
      try {
        const response = await axios.get('http://localhost:8000/clients/');
        this.clients = response.data.map(client => ({
          ...client,
          selectedTariffId: null // Добавляем поле selectedTariffId для каждого клиента
        }));
      } catch (error) {
        console.error('Error loading clients:', error);
      }
    },
    async addClient() {
      try {
        const response = await axios.post('http://localhost:8000/clients/', this.newClient);
        console.log('Added client:', response.data);
        this.clients.push({...response.data, selectedTariffId: null});
        this.newClient = {name: '', id: null, balance: null};
      } catch (error) {
        console.error('Error adding client:', error);
      }
    },
    async loadAvailableTariffs() {
      try {
        const response = await axios.get('http://localhost:8000/tariffs/');
        this.availableTariffs = response.data;
      } catch (error) {
        console.error('Error loading available tariffs:', error);
      }
    },
    async addTariffToClient(clientId, selectedTariffId) {
      try {
        await axios.post(`http://localhost:8000/client/${clientId}/tariffs/${selectedTariffId}/`);
        await this.loadClients(); // Обновляем список клиентов после присваивания тарифа
      } catch (error) {
        console.error('Error assigning tariff to client:', error);
      }
    }
  },
  mounted() {
    this.loadClients();
    this.loadAvailableTariffs();
  }
};
</script>

<style>
/* Add your custom styles here */
</style>
