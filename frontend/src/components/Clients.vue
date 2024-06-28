<template>
  <div>
    <h2>Clients</h2>
    <button class="action-button" @click="loadClients">Load Clients</button>
    <ul v-if="clients.length > 0" class="clients-list">
      <li v-for="client in clients" :key="client.id" class="client-item">
        Client
        ID: {{ client.id }} | Name: {{ client.name }} | Balance: {{ client.balance }}
        <ul class="client-tariffs-list">
          _____________________________________________
          <li v-for="tariff in client.tariffs" :key="tariff.id" class="client-tariff-item">
            ID: {{ tariff.id }} | Title: {{ tariff.title }}
            <button class="action-button delete-tariff" @click="removeTariffFromClient(client.id, tariff.id)">Remove Tariff</button>
          </li>
        </ul>
        <div class="add-tariff-form">
          <form @submit.prevent="addTariffToClient(client.id)">
            <h3>Add Tariff to Client</h3>
            <select v-model="client.selectedTariffId" class="tariff-select">
              <option v-for="tariff in availableTariffs" :key="tariff.id" :value="tariff.id">
                ID: {{ tariff.id }} | Title: {{ tariff.title }}
              </option>
            </select>
            <button type="submit" class="action-button">Add Tariff</button>
          </form>
        </div>
      </li>
    </ul>
    <form @submit.prevent="addClient" class="add-client-form">
      <h3>Add New Client</h3>
      <input type="text" v-model="newClient.name" placeholder="Name" required>
      <input type="number" v-model.number="newClient.id" placeholder="ID" required>
      <input type="number" v-model.number="newClient.balance" placeholder="Balance" required>
      <button type="submit" class="action-button">Add Client</button>
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
          selectedTariffId: null // Add selectedTariffId field for each client
        }));
      } catch (error) {
        console.error('Error loading clients:', error);
      }
    },
    async addClient() {
      try {
        const response = await axios.post('http://localhost:8000/client/', this.newClient);
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
    async addTariffToClient(clientId) {
      try {
        const selectedTariffId = this.clients.find(c => c.id === clientId).selectedTariffId;
        await axios.post(`http://localhost:8000/client/${clientId}/tariffs/${selectedTariffId}/`);
        await this.loadClients(); // Reload clients after assigning tariff
      } catch (error) {
        console.error('Error assigning tariff to client:', error);
      }
    },
    async removeTariffFromClient(clientId, tariffId) {
      try {
        await axios.delete(`http://localhost:8000/client/${clientId}/tariff/${tariffId}/`);
        await this.loadClients(); // Reload clients after removing tariff
      } catch (error) {
        console.error('Error removing tariff from client:', error);
      }
    }
  },
  mounted() {
    this.loadClients();
    this.loadAvailableTariffs();
  }
};
</script>

<style scoped>
.clients-list {
  list-style-type: none;
  padding: 0;
}

.client-item {
  border: 1px solid #ccc;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 8px;
  margin-right: 50%;
}

.client-tariffs-list {
  list-style-type: none;
  padding: 0;
  margin-top: 5px;
}

.client-tariff-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.add-tariff-form {
  margin-top: 10px;
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

.add-client-form {
  margin-top: 20px;
}

.action-button[type="submit"] {
  background-color: #28a745;
}

.action-button[type="submit"]:hover {
  background-color: #218838;
}

.tariff-select {
  margin-right: 10px;
}
</style>
