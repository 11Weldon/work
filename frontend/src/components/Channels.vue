<template>
  <div>
    <h2>Channels</h2>
    <button class="action-button" @click="loadChannels">Load Channels</button>
    <ul v-if="channels.length > 0" class="channels-list">
      <li v-for="func in channels" :key="func.id" class="channel-item">
        ID: {{ func.id }} | Title: {{ func.title }}
        <button class="action-button delete-channel" @click="deleteChannel(func.id)">Delete Channel</button>
      </li>
    </ul>
    <form @submit.prevent="addChannel" class="add-channel-form">
      <h3>Add New Channel</h3>
      <input type="text" v-model="newChannel.title" placeholder="Title" required>
      <input type="number" v-model.number="newChannel.id" placeholder="ID" required>
      <button type="submit" class="action-button">Add Channel</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Channels',
  data() {
    return {
      channels: [],
      newChannel: {
        title: '',
        id: null
      }
    };
  },
  methods: {
    async loadChannels() {
      try {
        const response = await axios.get('http://localhost:8000/channel/');
        this.channels = response.data;
      } catch (error) {
        console.error('Error loading channels:', error);
      }
    },
    async addChannel() {
      try {
        const response = await axios.post('http://localhost:8000/channel/', this.newChannel);
        console.log('Added channel:', response.data);
        this.channels.push(response.data);
        this.newChannel = {title: '', id: null};
      } catch (error) {
        console.error('Error adding channel:', error);
      }
    },
    async deleteChannel(channelId) {
      try {
        const response = await axios.delete(`http://localhost:8000/channel/${channelId}/`);
        console.log(response.data.message);
        await this.loadChannels();
      } catch (error) {
        console.error('Error deleting channel:', error);
      }
    }
  },
  mounted() {
    this.loadChannels();
  }
};
</script>

<style scoped>
.channels-list {
  list-style-type: none;
  padding: 0;
  margin-right: 50%;
}

.channel-item {
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

.delete-channel {
  background-color: #dc3545;
}

.delete-channel:hover {
  background-color: #c82333;
}

.add-channel-form {
  margin-top: 20px;
}

.action-button[type="submit"] {
  background-color: #28a745;
}

.action-button[type="submit"]:hover {
  background-color: #218838;
}
</style>
