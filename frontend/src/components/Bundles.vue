<template>
  <div class="bundles-container">
    <h2>Bundles</h2>
    <button class="action-button" @click="loadBundles">Load Bundles</button>
    <ul v-if="bundles.length > 0" class="bundles-list">
      <li v-for="bundle in bundles" :key="bundle.id" class="bundle-item">
        <div class="bundle-info">
          <span>ID: {{ bundle.id }}</span> | <span>Title: {{ bundle.title }}</span>
          <button class="action-button delete-bundle" @click="deleteBundle(bundle.id)">Delete Bundle</button>
          <ul class="channels-list">
            <li v-for="channels in bundle.channels" :key="channels.id" class="channel-item">
              <span>ID: {{ channels.id }}</span> | <span>Title: {{ channels.title }}</span>
              <button class="action-button delete-channel" @click="deleteChannelFromBundle(bundle.id, channels.id)">Delete Channel</button>
            </li>
          </ul>
          <form @submit.prevent="addChannelToBundle(bundle.id)" class="add-channel-form">
            <h3>Add Channel to Bundle</h3>
            <select v-model="bundle.selectedChannelId" class="channel-select">
              <option v-for="channels in availableChannels" :key="channels.id" :value="channels.id">
                ID: {{ channels.id }} | Title: {{ channels.title }}
              </option>
            </select>
            <button type="submit" class="action-button">Add Channel</button>
          </form>
        </div>
      </li>
    </ul>
    <form @submit.prevent="addBundle" class="add-bundle-form">
      <h3>Add New Bundle</h3>
      <input type="text" v-model="newBundle.title" placeholder="Title" required>
      <input type="number" v-model.number="newBundle.id" placeholder="ID" required>
      <button type="submit" class="action-button">Add Bundle</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Bundles',
  data() {
    return {
      bundles: [],
      newBundle: {
        title: '',
        id: null
      },
      availableChannels: []
    };
  },
  methods: {
    async loadBundles() {
      try {
        const response = await axios.get('http://localhost:8000/bundles/');
        this.bundles = response.data.map(bundle => ({
          ...bundle,
          selectedChannelId: null
        }));
      } catch (error) {
        console.error('Error loading bundles:', error);
      }
    },
    async addBundle() {
      try {
        const response = await axios.post('http://localhost:8000/bundle/', this.newBundle);
        console.log('Added bundle:', response.data);
        this.bundles.push({...response.data, selectedChannelId: null});
        this.newBundle = {title: '', id: null};
      } catch (error) {
        console.error('Error adding bundle:', error);
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
    async addChannelToBundle(bundleId) {
      try {
        const selectedChannelId = this.bundles.find(t => t.id === bundleId).selectedChannelId;
        await axios.post(`http://localhost:8000/bundle/${bundleId}/channel/${selectedChannelId}/`);
        await this.loadBundles();
      } catch (error) {
        console.error('Error adding channel to bundle:', error);
      }
    },
    async deleteBundle(bundleId) {
      try {
        const response = await axios.delete(`http://localhost:8000/bundle/${bundleId}/`);
        console.log(response.data.message);
        this.loadBundles();
      } catch (error) {
        console.error('Error deleting bundle:', error);
      }
    },
    async deleteChannelFromBundle(bundleId, channelId) {
      try {
        const response = await axios.delete(`http://localhost:8000/bundle/${bundleId}/channel/${channelId}/`);
        console.log(response.data.message);
        await this.loadBundles();
      } catch (error) {
        console.error('Error deleting channel from bundle:', error);
      }
    }
  },
  mounted() {
    this.loadBundles();
    this.loadChannels();
  }
};
</script>

<style scoped>
.bundles-container {
  margin-bottom: 20px;
  margin-right: 50%;
}

.bundles-list {
  list-style-type: none;
  padding: 0;
}

.bundle-item {
  border: 1px solid #ccc;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 8px;
}

.bundle-info {
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

.add-bundle-form {
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

.delete-bundle {
  background-color: #dc3545;
}

.delete-bundle:hover {
  background-color: #c82333;
}

.delete-channel {
  background-color: #dc3545;
}

.delete-channel:hover {
  background-color: #c82333;
}
</style>
