import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';
import Clients from './components/Clients.vue';
import Channels from "@/components/Channels.vue";
import Bundles from "@/components/Bundles.vue";

const routes = [
    { path: '/', redirect: '/clients' },
    { path: '/clients', component: Clients },
    { path: '/channels', component: Channels },
    { path: '/bundles', component: Bundles }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

const app = createApp(App);
app.use(router);
app.mount('#app');
