import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';
import Clients from './components/Clients.vue';
import Functions from './components/Functions.vue';
import Tariffs from './components/Tariffs.vue';

const routes = [
    { path: '/', redirect: '/clients' }, // Перенаправление на клиентов по умолчанию
    { path: '/clients', component: Clients },
    { path: '/functions', component: Functions },
    { path: '/tariffs', component: Tariffs }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

const app = createApp(App);
app.use(router);
app.mount('#app');
