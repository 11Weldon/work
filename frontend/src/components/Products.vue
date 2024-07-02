<template>
  <div class="products-container">
    <h2>Products</h2>
    <button class="action-button" @click="loadProducts">Load Products</button>
    <ul v-if="products.length > 0" class="products-list">
      <li v-for="product in products" :key="product.id" class="product-item">
        <div class="product-info">
          <span>ID: {{ product.id }}</span> | <span>Title: {{ product.title }}</span>
          <button class="action-button delete-product" @click="deleteProduct(product.id)">Delete Product</button>
          <ul class="channels-list">
            <li v-for="channels in product.channels" :key="channels.id" class="channel-item">
              <span>ID: {{ channels.id }}</span> | <span>Title: {{ channels.title }}</span>
              <button class="action-button delete-channel" @click="deleteChannelFromProduct(product.id, channels.id)">Delete Channel</button>
            </li>
          </ul>
          <form @submit.prevent="addChannelToProduct(product.id)" class="add-channel-form">
            <h3>Add Channel to Product</h3>
            <select v-model="product.selectedChannelId" class="channel-select">
              <option v-for="channels in availableChannels" :key="channels.id" :value="channels.id">
                ID: {{ channels.id }} | Title: {{ channels.title }}
              </option>
            </select>
            <button type="submit" class="action-button">Add Channel</button>
          </form>
        </div>
      </li>
    </ul>
    <form @submit.prevent="addProduct" class="add-product-form">
      <h3>Add New Product</h3>
      <input type="text" v-model="newProduct.title" placeholder="Title" required>
      <input type="number" v-model.number="newProduct.id" placeholder="ID" required>
      <button type="submit" class="action-button">Add Product</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Products',
  data() {
    return {
      products: [],
      newProduct: {
        title: '',
        id: null
      },
      availableChannels: []
    };
  },
  methods: {
    async loadProducts() {
      try {
        const response = await axios.get('http://localhost:8000/products/');
        this.products = response.data.map(product => ({
          ...product,
          selectedChannelId: null
        }));
      } catch (error) {
        console.error('Error loading products:', error);
      }
    },
    async addProduct() {
      try {
        const response = await axios.post('http://localhost:8000/product/', this.newProduct);
        console.log('Added product:', response.data);
        this.products.push({...response.data, selectedChannelId: null});
        this.newProduct = {title: '', id: null};
      } catch (error) {
        console.error('Error adding product:', error);
      }
    },
    async loadChannels() {
      try {
        const response = await axios.get('http://localhost:8000/channel/');
        this.availableChannels = response.data;
      } catch (error) {
        console.error('Error loading channels:', error);
      }
    },
    async addChannelToProduct(productId) {
      try {
        const selectedChannelId = this.products.find(t => t.id === productId).selectedChannelId;
        await axios.post(`http://localhost:8000/product/${productId}/channel/${selectedChannelId}/`);
        await this.loadProducts();
      } catch (error) {
        console.error('Error adding channel to product:', error);
      }
    },
    async deleteProduct(productId) {
      try {
        const response = await axios.delete(`http://localhost:8000/product/${productId}/`);
        console.log(response.data.message);
        this.loadProducts();
      } catch (error) {
        console.error('Error deleting product:', error);
      }
    },
    async deleteChannelFromProduct(productId, channelId) {
      try {
        const response = await axios.delete(`http://localhost:8000/product/${productId}/channel/${channelId}/`);
        console.log(response.data.message);
        await this.loadProducts();
      } catch (error) {
        console.error('Error deleting channel from product:', error);
      }
    }
  },
  mounted() {
    this.loadProducts();
    this.loadChannels();
  }
};
</script>

<style scoped>
.products-container {
  margin-bottom: 20px;
  margin-right: 50%;
}

.products-list {
  list-style-type: none;
  padding: 0;
}

.product-item {
  border: 1px solid #ccc;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 8px;
}

.product-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.channels-list {
  list-style-type: none;
  padding: 0;
  margin-top: 5px;
}

.channel-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.add-channel-form {
  margin-top: 10px;
}

.channel-select {
  margin-right: 10px;
}

.add-product-form {
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

.delete-product {
  background-color: #dc3545;
}

.delete-product:hover {
  background-color: #c82333;
}

.delete-channel {
  background-color: #dc3545;
}

.delete-channel:hover {
  background-color: #c82333;
}
</style>
