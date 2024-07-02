<template>
  <div>
    <h2>Clients</h2>
    <button class="action-button" @click="loadClients">Load Clients</button>
    <ul v-if="clients.length > 0" class="clients-list">
      <li v-for="client in clients" :key="client.id" class="client-item">
        Client
        ID: {{ client.id }} | Name: {{ client.name }} | Balance: {{ client.balance }}
        <ul class="client-products-list">
          _____________________________________________
          <li v-for="product in client.products" :key="product.id" class="client-product-item">
            ID: {{ product.id }} | Title: {{ product.title }}
            <button class="action-button delete-product" @click="removeProductFromClient(client.id, product.id)">Remove Product</button>
          </li>
        </ul>
        <div class="add-product-form">
          <form @submit.prevent="addProductToClient(client.id)">
            <h3>Add Product to Client</h3>
            <select v-model="client.selectedProductId" class="product-select">
              <option v-for="product in availableProducts" :key="product.id" :value="product.id">
                ID: {{ product.id }} | Title: {{ product.title }}
              </option>
            </select>
            <button type="submit" class="action-button">Add Product</button>
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
      availableProducts: []
    };
  },
  methods: {
    async loadClients() {
      try {
        const response = await axios.get('http://localhost:8000/clients/');
        this.clients = response.data.map(client => ({
          ...client,
          selectedProductId: null // Add selectedProductId field for each client
        }));
      } catch (error) {
        console.error('Error loading clients:', error);
      }
    },
    async addClient() {
      try {
        const response = await axios.post('http://localhost:8000/client/', this.newClient);
        console.log('Added client:', response.data);
        this.clients.push({...response.data, selectedProductId: null});
        this.newClient = {name: '', id: null, balance: null};
      } catch (error) {
        console.error('Error adding client:', error);
      }
    },
    async loadAvailableProducts() {
      try {
        const response = await axios.get('http://localhost:8000/products/');
        this.availableProducts = response.data;
      } catch (error) {
        console.error('Error loading available products:', error);
      }
    },
    async addProductToClient(clientId) {
      try {
        const selectedProductId = this.clients.find(c => c.id === clientId).selectedProductId;
        await axios.post(`http://localhost:8000/client/${clientId}/products/${selectedProductId}/`);
        await this.loadClients();
      } catch (error) {
        console.error('Error assigning product to client:', error);
      }
    },
    async removeProductFromClient(clientId, productId) {
      try {
        await axios.delete(`http://localhost:8000/client/${clientId}/products/${productId}/`);
        await this.loadClients();
      } catch (error) {
        console.error('Error removing product from client:', error);
      }
    }
  },
  mounted() {
    this.loadClients();
    this.loadAvailableProducts();
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

.client-products-list {
  list-style-type: none;
  padding: 0;
  margin-top: 5px;
}

.client-product-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.add-product-form {
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

.delete-product {
  background-color: #dc3545;
}

.delete-product:hover {
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

.product-select {
  margin-right: 10px;
}
</style>
