<template>
  <div class="channel-container">
    <!-- Channel list -->
    <div class="channel-list">
      <h2>Channel list</h2>
      <ul>
        <li v-for="(channel, index) in channels" :key="index">
          <strong>Channel ID:  {{ channel.channel_id }}</strong> - <span>Channel name:  {{ channel.name }}</span>
        </li>
      </ul>
    </div>

    <!-- Channel add form -->
    <div class="channel-add-form">
      <h2> Channel add form </h2>
      <form @submit.prevent="createChannel" class="channel-form">
      <div class="form-group">
        <label for="serviceId">ID сервиса:</label>
        <input type="number" id="serviceId" v-model.number="channelSchema.serviceId" required>
      </div>

      <div class="form-group">
        <label for="name">Название:</label>
        <input type="text" id="name" v-model.trim="channelSchema.name">
      </div>

      <div class="form-group">
        <label for="type">Тип:</label>
        <input type="text" id="type" v-model.trim="channelSchema.type">
      </div>

      <div class="form-group">
        <label for="status">Статус:</label>
        <input type="text" id="status" v-model.trim="channelSchema.status">
      </div>

      <div class="form-group">
        <label for="format">Формат:</label>
        <input type="number" id="format" v-model.number="channelSchema.format">
      </div>

      <div class="form-group">
        <label for="mprovId">mprovId:</label>
        <input type="number" id="mprovId" v-model.number="channelSchema.mprovId">
      </div>

      <div class="form-group">
        <label for="cprovId">cprovId:</label>
        <input type="number" id="cprovId" v-model.number="channelSchema.cprovId">
      </div>

      <div class="form-group">
        <label for="langs">Языки:</label>
        <input type="number" id="langs" v-model.number="channelSchema.langs">
      </div>

      <button type="submit" class="submit-button">Создать канал</button>
    </form>
    </div>

    <div class="set-channel-live-urls">
      <h2> Set Channel Live Urls </h2>
      <form @submit.prevent="setChannelLiveUrls" class="channel-form">

        <div class="form-group">
          <label for="channelId">channelId:</label>
          <input type="number" id="channelId" v-model.number="channelLiveUrlsSchema.channelId" required>
        </div>

        <div class="form-group">
          <label for="channelUrls">channelUrls:</label>
          <input type="text" id="channelUrls" v-model.lazy="channelLiveUrlsSchema.channelUrls">
        </div>


        <button type="submit" class="submit-button">Задать live urls</button>
      </form>
    </div>

    <div class="set-group-product-services">
      <h2>Set Group Product Services</h2>
      <form @submit.prevent="setGroupProductServices" class="channel-form">

        <div class="form-group">
          <label for="groupProductId">group ProductId:</label>
          <input type="number" id="groupProductId" v-model.number="setGroupProductServicesRequest.groupProductId" required>
        </div>

        <div class="form-group">
          <label for="serviceIds">serviceIds:</label>
          <input type="text" id="serviceIds" v-model.number="setGroupProductServicesRequest.serviceIds" required>
        </div>

        <button type="submit" class="submit-button">Добавить в продукт каналы</button>
      </form>
    </div>

    <div class="create-services-list">
      <h2>Create Services List</h2>
      <form @submit.prevent="createServicesList" class="channel-form">
        <div class="form-group">
          <label for="targetType">targetType:</label>
          <input type="text" id="targetType" v-model.number="servicesList.targetType" required>
        </div>

        <div class="form-group">
          <label for="targetId">targetId:</label>
          <input type="number" id="targetId" v-model.trim="servicesList.targetId">
        </div>

        <div class="form-group">
          <label for="name">name:</label>
          <input type="text" id="name" v-model.trim="servicesList.name">
        </div>

        <div class="form-group">
          <label for="type">type:</label>
          <input type="text" id="type" v-model.trim="servicesList.type">
        </div>

        <div class="form-group">
          <label for="seqNum">seqNum:</label>
          <input type="number" id="seqNum" v-model.trim="servicesList.seqNum">
        </div>

        <div class="form-group">
          <label for="inheritable">inheritable:</label>
          <input type="checkbox" id="inheritable" v-model.number="servicesList.inheritable">
        </div>

        <div class="form-group">
          <label for="locked">locked:</label>
          <input type="checkbox" id="mprovId" v-model.number="servicesList.locked">
        </div>

        <div class="form-group">
          <label for="title">title:</label>
          <input type="text" id="title" v-model.number="servicesList.title">
        </div>

        <div class="form-group">
          <label for="descr">descr:</label>
          <input type="text" id="descr" v-model.number="servicesList.descr">
        </div>

        <div class="form-group">
          <label for="entryIds">entryIds:</label>
          <input type="text" id="entryIds" v-model.number="servicesList.entryIds">
        </div>

        <div class="form-group">
          <label for="entryLsns">entryLsns:</label>
          <input type="text" id="entryLsns" v-model.number="servicesList.entryLsns">
        </div>


        <button type="submit" class="submit-button">Создать список каналов</button>
      </form>
    </div>

  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { DefaultApi } from '@/api/apis/DefaultApi';
import type { ChannelSchema, ChannelLiveUrlsSchema, SetGroupProductServicesRequest, ServicesList,  } from "@/api/models";

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
        alert(`Error fetching channels: ${error}`); // Выводим ошибку пользователю
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
}

.channel-list {
  flex: auto;
  margin-right: 400px;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}

.channel-add-form {
  flex: auto;
}

.channel-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f4f4f4;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
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
input[type="number"] {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
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


.channel-list {
  margin-top: 10px;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}

.channel-list h2 {
  font-size: 20px;
  margin-bottom: 10px;
  color: #333;
}

.channel-list ul {
  list-style-type: none;
  padding: 0;
}

.channel-list li {
  margin-bottom: 8px;
}

.channel-list li strong {
  font-weight: bold;
}

.channel-list li span {
  color: #888;
}

.channel-list li:hover {
  background-color: #f0f0f0;
  cursor: pointer;
}
</style>
