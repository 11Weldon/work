<template>
  <div>
    <h2>Clients</h2>
    <button class="action-button" @click="loadClients">Load Clients</button>
    <ul v-if="clients.length > 0" class="clients-list">
      <li v-for="client in clients" :key="client.id" class="client-item">
        Client
        ID: {{ client.id }} | Name: {{ client.name }} | Balance: {{ client.balance }}
        <ul class="client-bundles-list">
          _____________________________________________
          <li v-for="bundle in client.bundles" :key="bundle.id" class="client-bundle-item">
            ID: {{ bundle.id }} | Title: {{ bundle.title }}
            <button class="action-button delete-bundle" @click="removeBundleFromClient(client.id, bundle.id)">Remove Bundle</button>
          </li>
        </ul>
        <div class="add-bundle-form">
          <form @submit.prevent="addBundleToClient(client.id)">
            <h3>Add Bundle to Client</h3>
            <select v-model="client.selectedBundleId" class="bundle-select">
              <option v-for="bundle in availableBundles" :key="bundle.id" :value="bundle.id">
                ID: {{ bundle.id }} | Title: {{ bundle.title }}
              </option>
            </select>
            <button type="submit" class="action-button">Add Bundle</button>
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
      availableBundles: []
    };
  },
  methods: {
    async loadClients() {
      try {
        const response = await axios.get('http://localhost:8000/clients/');
        this.clients = response.data.map(client => ({
          ...client,
          selectedBundleId: null // Add selectedBundleId field for each client
        }));
      } catch (error) {
        console.error('Error loading clients:', error);
      }
    },
    async addClient() {
      try {
        const response = await axios.post('http://localhost:8000/client/', this.newClient);
        console.log('Added client:', response.data);
        this.clients.push({...response.data, selectedBundleId: null});
        this.newClient = {name: '', id: null, balance: null};
      } catch (error) {
        console.error('Error adding client:', error);
      }
    },
    async loadAvailableBundles() {
      try {
        const response = await axios.get('http://localhost:8000/bundles/');
        this.availableBundles = response.data;
      } catch (error) {
        console.error('Error loading available bundles:', error);
      }
    },
    async addBundleToClient(clientId) {
      try {
        const selectedBundleId = this.clients.find(c => c.id === clientId).selectedBundleId;
        await axios.post(`http://localhost:8000/client/${clientId}/bundles/${selectedBundleId}/`);
        await this.loadClients();
      } catch (error) {
        console.error('Error assigning bundle to client:', error);
      }
    },
    async removeBundleFromClient(clientId, bundleId) {
      try {
        await axios.delete(`http://localhost:8000/client/${clientId}/bundles/${bundleId}/`);
        await this.loadClients();
      } catch (error) {
        console.error('Error removing bundle from client:', error);
      }
    }
  },
  mounted() {
    this.loadClients();
    this.loadAvailableBundles();
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

.client-bundles-list {
  list-style-type: none;
  padding: 0;
  margin-top: 5px;
}

.client-bundle-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.add-bundle-form {
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

.delete-bundle {
  background-color: #dc3545;
}

.delete-bundle:hover {
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

.bundle-select {
  margin-right: 10px;
}
</style>
