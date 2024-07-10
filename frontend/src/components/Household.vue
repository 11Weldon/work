<template>
  <div class="household-container">
    <!-- Household creation form -->
    <div class="form-card">
      <h2>Create Household</h2>
      <form @submit.prevent="createHousehold" class="form">
        <div class="form-group">
          <label for="domain">Domain:</label>
          <input type="number" id="domain" v-model.number="householdData.domain" required>
        </div>

        <div class="form-group">
          <label for="description">Description:</label>
          <input type="text" id="description" v-model.trim="householdData.description">
        </div>

        <div class="form-group">
          <label for="status">Status:</label>
          <input type="text" id="status" v-model.trim="householdData.status">
        </div>

        <div class="form-group">
          <label for="accntCode">Account Code:</label>
          <input type="text" id="accntCode" v-model.trim="householdData.accntCode">
        </div>

        <div class="form-group">
          <label for="localeId">Locale ID:</label>
          <input type="number" id="localeId" v-model.number="householdData.localeId">
        </div>

        <div class="form-group">
          <label for="maxDevices">Max Devices:</label>
          <input type="number" id="maxDevices" v-model.number="householdData.maxDevices">
        </div>

        <div class="form-group">
          <label for="maxUsers">Max Users:</label>
          <input type="number" id="maxUsers" v-model.number="householdData.maxUsers">
        </div>

        <div class="form-group">
          <label for="maxProfiles">Max Profiles:</label>
          <input type="number" id="maxProfiles" v-model.number="householdData.maxProfiles">
        </div>

        <div class="form-group">
          <label for="noPers">No Persons:</label>
          <input type="checkbox" id="noPers" v-model="householdData.noPers">
        </div>

        <button type="submit" class="submit-button">Create Household</button>
      </form>
    </div>

    <!-- Profile creation form -->
    <div class="form-card">
      <h2>Create Profile</h2>
      <form @submit.prevent="createProfile" class="form">

        <div class="form-group">
          <label for="householdId">Household ID:</label>
          <input type="number" id="householdId" v-model.number="householdId" required>
        </div>

        <div class="form-group">
          <label for="profileName">Profile Name:</label>
          <input type="text" id="profileName" v-model.trim="profileData.name" required>
        </div>

        <div class="form-group">
          <label for="type">Type:</label>
          <input type="text" id="type" v-model.trim="profileData.type">
        </div>

        <div class="form-group">
          <label for="descr">Description:</label>
          <input type="text" id="descr" v-model.trim="profileData.descr">
        </div>

        <div class="form-group">
          <label for="age">Age:</label>
          <input type="number" id="age" v-model.number="profileData.age">
        </div>

        <div class="form-group">
          <label for="pin">PIN:</label>
          <input type="number" id="pin" v-model.number="profileData.pin">
        </div>

        <div class="form-group">
          <label for="purchasePin">Purchase PIN:</label>
          <input type="number" id="purchasePin" v-model.number="profileData.purchasePin">
        </div>

        <button type="submit" class="submit-button">Create Profile</button>
      </form>
    </div>

    <!-- Set household products form -->
    <div class="form-card">
      <h2>Set Household Products</h2>
      <form @submit.prevent="setHouseholdProducts" class="form">
        <div class="form-group">
          <label for="householdId">Household ID:</label>
          <input type="number" id="householdId" v-model.number="householdProducts.householdId" required>
        </div>

        <div class="form-group">
          <label for="productIds">Product IDs (comma-separated):</label>
          <input type="text" id="productIds" v-model="householdProducts.productIds" required>
        </div>

        <button type="submit" class="submit-button">Set Household Products</button>
      </form>
    </div>

    <!-- Display household, user, and profile data -->
    <div class="data-list">
      <div class="list-card">
        <h2>Household List</h2>
        <ul>
          <li v-for="(household, index) in households" :key="index">
            <strong>Household ID:  {{ household.household_id }}</strong> - <span>Domain:  {{ household.domain }}</span>
          </li>
        </ul>
      </div>
      <div class="list-card">
        <h2>User List</h2>
        <ul>
          <li v-for="(user, index) in users" :key="index">
            <strong>User ID:  {{ user.user_id }}</strong> - <span>Username:  {{ user.username }}</span>
          </li>
        </ul>
      </div>
      <div class="list-card">
        <h2>Profile List</h2>
        <ul>
          <li v-for="(profile, index) in profiles" :key="index">
            <strong>Profile ID:  {{ profile.profile_id }}</strong> - <span>Name:  {{ profile.name }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { DefaultApi } from '@/api/apis/DefaultApi';
import type { HouseholdSchema, UserSchema, ProfileSchema, HouseholdProducts } from "@/api/models";

export default defineComponent({
  data() {
    return {
      householdData: {} as HouseholdSchema,
      userData: {} as UserSchema,
      profileData: {} as ProfileSchema,
      householdProducts: {} as HouseholdProducts,
      householdId: -1,
      households: [] as HouseholdSchema[],
      users: [] as UserSchema[],
      profiles: [] as ProfileSchema[],
    };
  },
  mounted() {
    this.fetchHouseholds();
    this.fetchUsers();
    this.fetchProfiles();
  },
  methods: {
    async fetchHouseholds() {
      try {
        const api = new DefaultApi();
        const response = await api.getHouseholdsRouteOpFacadeHoushMgmtHouseholdsGet();
        this.households = response;
      } catch (error) {
        console.error('Error fetching channels:', error);
        alert(`Error fetching channels: ${error}`);
      }
    },
    async fetchUsers() {
      try {
        const api = new DefaultApi();
        const response = await api.getUsersRouteOpFacadeHoushMgmtUsersGet();
        this.users = response;
      } catch (error) {
        console.error('Error fetching channels:', error);
        alert(`Error fetching channels: ${error}`);
      }
    },
    async fetchProfiles() {
      try {
        const api = new DefaultApi();
        const response = await api.getProfilesRouteOpFacadeHoushMgmtProfilesGet();
        this.profiles = response;
      } catch (error) {
        console.error('Error fetching channels:', error);
        alert(`Error fetching channels: ${error}`);
      }
    },
    async createHousehold() {
      try {
        console.log('Submitting household creation request:', this.householdData);

        const api = new DefaultApi();
        const response = await api.createHouseholdExtOpFacadeHoushMgmtCreateHouseholdExtPost({
          bodyCreateHouseholdExtOpFacadeHoushMgmtCreateHouseholdExtPost: {
            householdData: this.householdData,
            userData: this.userData,
          }
        });

        console.log('API response:', response);

        // Assuming response.data contains the created household
        this.households.push(response.data);

      } catch (error) {
        console.error('Error creating household:', error);
        alert(`Error creating household: ${error}`);
      }
    },

    async createProfile() {
      try {
        console.log('Submitting profile creation request:', this.profileData);

        const api = new DefaultApi();
        const response = await api.createProfileRouteOpFacadeHoushMgmtCreateProfilePost({
          householdId: this.householdId,
          profileSchema: this.profileData,
        });

        console.log('API response:', response);

        // Assuming response.data contains the created profile
        this.profiles.push(response.data);

      } catch (error) {
        console.error('Error creating profile:', error);
        alert(`Error creating profile: ${error}`);
      }
    },

    async setHouseholdProducts() {
      try {
        console.log('Submitting set household products request:', this.householdProducts);

        const api = new DefaultApi();
        this.householdProducts.productIds = this.householdProducts.productIds.split(',')
            .map((item: string) => Number(item.trim()));

        const response = await api.setGroupProductServicesRouteOpFacadeProdMgmtSetHouseholdProdsPost({
          householdProducts: this.householdProducts,
        });

        console.log('API response:', response);

      } catch (error) {
        console.error('Error setting household products:', error);
        alert(`Error setting household products: ${error}`);
      }
    },
  },
});
</script>

<style scoped>
.household-container {
  display: flex;
  justify-content: space-around;
  gap: 20px;
}

.form-card {
  flex: 1;
  padding: 20px;
  background-color: #f9f9f9;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.form-card h2 {
  font-size: 20px;
  margin-bottom: 10px;
  color: #333;
}

.form {
  width: 100%;
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

.data-list {
  display: flex;
  justify-content: space-around;
  gap: 20px;
}

.list-card {
  flex: 1;
  padding: 20px;
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.list-card h2 {
  font-size: 20px;
  margin-bottom: 10px;
  color: #333;
}

.list-card ul {
  list-style-type: none;
  padding: 0;
}

.list-card li {
  margin-bottom: 8px;
}

.list-card li strong {
  font-weight: bold;
}

.list-card li span {
  color: #888;
}

.list-card li:hover {
  background-color: #f0f0f0;
  cursor: pointer;
}
</style>
