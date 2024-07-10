<template>
  <div class="channel-container">
    <!-- Channel list -->
    <div class="list-card">
      <h2>Channel List</h2>
      <ul>
        <li v-for="(channel, index) in channels" :key="index">
          <strong>Channel ID: {{ channel.channel_id }}</strong> - <span>Channel Name: {{ channel.name }}</span>
        </li>
      </ul>
    </div>

    <!-- Channel add form -->
    <div class="form-card">
      <h2>Channel Add Form</h2>
      <form @submit.prevent="createChannel" class="form">
        <div class="form-group">
          <label for="serviceId">Service ID:</label>
          <input type="number" id="serviceId" v-model.number="channelSchema.serviceId" required>
        </div>

        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model.trim="channelSchema.name">
        </div>

        <div class="form-group">
          <label for="type">Type:</label>
          <input type="text" id="type" v-model.trim="channelSchema.type">
        </div>

        <div class="form-group">
          <label for="status">Status:</label>
          <input type="text" id="status" v-model.trim="channelSchema.status">
        </div>

        <div class="form-group">
          <label for="format">Format:</label>
          <input type="number" id="format" v-model.number="channelSchema.format">
        </div>

        <div class="form-group">
          <label for="mprovId">Mprov ID:</label>
          <input type="number" id="mprovId" v-model.number="channelSchema.mprovId">
        </div>

        <div class="form-group">
          <label for="cprovId">Cprov ID:</label>
          <input type="number" id="cprovId" v-model.number="channelSchema.cprovId">
        </div>

        <div class="form-group">
          <label for="langs">Languages:</label>
          <input type="number" id="langs" v-model.number="channelSchema.langs">
        </div>

        <button type="submit" class="submit-button">Create Channel</button>
      </form>
    </div>

    <!-- Set Channel Live URLs -->
    <div class="form-card">
      <h2>Set Channel Live URLs</h2>
      <form @submit.prevent="setChannelLiveUrls" class="form">
        <div class="form-group">
          <label for="channelId">Channel ID:</label>
          <input type="number" id="channelId" v-model.number="channelLiveUrlsSchema.channelId" required>
        </div>

        <div class="form-group">
          <label for="channelUrls">Channel URLs:</label>
          <input type="text" id="channelUrls" v-model.lazy="channelLiveUrlsSchema.channelUrls">
        </div>

        <button type="submit" class="submit-button">Set Live URLs</button>
      </form>
    </div>

    <!-- Set Group Product Services -->
    <div class="form-card">
      <h2>Set Group Product Services</h2>
      <form @submit.prevent="setGroupProductServices" class="form">
        <div class="form-group">
          <label for="groupProductId">Group Product ID:</label>
          <input type="number" id="groupProductId" v-model.number="setGroupProductServicesRequest.groupProductId" required>
        </div>

        <div class="form-group">
          <label for="serviceIds">Service IDs (comma-separated):</label>
          <input type="text" id="serviceIds" v-model="setGroupProductServicesRequest.serviceIds" required>
        </div>

        <button type="submit" class="submit-button">Add Channels to Product</button>
      </form>
    </div>

    <!-- Create Services List -->
    <div class="form-card">
      <h2>Create Services List</h2>
      <form @submit.prevent="createServicesList" class="form">
        <div class="form-group">
          <label for="targetType">Target Type:</label>
          <input type="text" id="targetType" v-model="servicesList.targetType" required>
        </div>

        <div class="form-group">
          <label for="targetId">Target ID:</label>
          <input type="number" id="targetId" v-model.number="servicesList.targetId">
        </div>

        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model.trim="servicesList.name">
        </div>

        <div class="form-group">
          <label for="type">Type:</label>
          <input type="text" id="type" v-model.trim="servicesList.type">
        </div>

        <div class="form-group">
          <label for="seqNum">Sequence Number:</label>
          <input type="number" id="seqNum" v-model.number="servicesList.seqNum">
        </div>

        <div class="form-group">
          <label for="inheritable">Inheritable:</label>
          <input type="checkbox" id="inheritable" v-model.number="servicesList.inheritable">
        </div>

        <div class="form-group">
          <label for="locked">Locked:</label>
          <input type="checkbox" id="locked" v-model.number="servicesList.locked">
        </div>

        <div class="form-group">
          <label for="title">Title:</label>
          <input type="text" id="title" v-model.trim="servicesList.title">
        </div>

        <div class="form-group">
          <label for="descr">Description:</label>
          <input type="text" id="descr" v-model.trim="servicesList.descr">
        </div>

        <div class="form-group">
          <label for="entryIds">Entry IDs:</label>
          <input type="text" id="entryIds" v-model.trim="servicesList.entryIds">
        </div>

        <div class="form-group">
          <label for="entryLsns">Entry Lsns:</label>
          <input type="text" id="entryLsns" v-model.trim="servicesList.entryLsns">
        </div>

        <button type="submit" class="submit-button">Create Services List</button>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { DefaultApi } from '@/api/apis/DefaultApi';
import type {
  ChannelSchema,
  ChannelLiveUrlsSchema,
  SetGroupProductServicesRequest,
  ServicesList,
} from "@/api/models";

export default defineComponent({
  data() {
    return {
      channelSchema: {} as ChannelSchema,
      channelLiveUrlsSchema: {} as ChannelLiveUrlsSchema,
      setGroupProductServicesRequest: {} as SetGroupProductServicesRequest,
      servicesList: {} as ServicesList,
      channels: [] as ChannelSchema[],
    };
  },
  mounted() {
    this.fetchChannels();
  },
  methods: {
    async fetchChannels() {
      try {
        const api = new DefaultApi();
        const response = await api.getChannelsOpFacadeChnMgmtChannelsGet();
        this.channels = response;
      } catch (error) {
        console.error('Error fetching channels:', error);
        alert(`Error fetching channels: ${error}`);
      }
    },
    async createChannel() {
      try {
        console.log('Submitting channel creation request:', this.channelSchema);
        const api = new DefaultApi();
        const response = await api.createChannelOpFacadeChnMgmtCreateChannelPost({
          channelSchema: this.channelSchema,
        });
        console.log('API response:', response);
      } catch (error) {
        console.error('Error creating channel:', error);
        alert(`Error creating channel: ${error}`);
      }
    },
    async setChannelLiveUrls() {
      try {
        console.log('Submitting setChannelLiveUrls request:', this.channelLiveUrlsSchema);
        this.channelLiveUrlsSchema.channelUrls = JSON.parse(this.channelLiveUrlsSchema.channelUrls);
        const api = new DefaultApi();
        const response = await api.setChannelLiveUrlsRouteOpFacadeChnMgmtSetChannelLiveUrlsPost({
          channelLiveUrlsSchema: this.channelLiveUrlsSchema,
        });
        console.log('API response:', response);
      } catch (error) {
        console.error('Error setChannelLiveUrls:', error);
        alert(`Error setChannelLiveUrls: ${error}`);
      }
    },
    async setGroupProductServices() {
      try {
        console.log('Submitting setGroupProductServicesRequest request:', this.setGroupProductServicesRequest);
        this.setGroupProductServicesRequest.serviceIds = this.setGroupProductServicesRequest.serviceIds.split(',')
            .map((item: string) => Number(item.trim()));
        const api = new DefaultApi();
        const response = await api.setGroupProductServicesRouteOpFacadeProdMgmtSetGroupProductServicesPost({
          setGroupProductServicesRequest: this.setGroupProductServicesRequest,
        });
        console.log('API response:', response);
      } catch (error) {
        console.error('Error setGroupProductServices:', error);
        alert(`Error setGroupProductServices: ${error}`);
      }
    },
    async createServicesList() {
      try {
        console.log('Submitting createServicesList request:', this.servicesList);
        const api = new DefaultApi();
        const response = await api.createServicesListRouteOpFacadeDomMgmtCreateServicesListPost({
          servicesList: this.servicesList,
        });
        console.log('API response:', response);
      } catch (error) {
        console.error('Error createServicesList:', error);
        alert(`Error createServicesList: ${error}`);
      }
    },
  },
});
</script>

<style scoped>
.channel-container {
  display: flex;
  justify-content: space-around;
  gap: 20px;
}

.list-card,
.form-card {
  flex: 1;
  padding: 20px;
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 20px;
  margin-bottom: 10px;
  color: #333;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 8px;
}

li strong {
  font-weight: bold;
}

li span {
  color: #888;
}

li:hover {
  background-color: #f0f0f0;
  cursor: pointer;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

input[type="text"],
input[type="number"],
input[type="checkbox"] {
  width: calc(100% - 20px);
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.submit-button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.submit-button:hover {
  background-color: #45a049;
}
</style>
