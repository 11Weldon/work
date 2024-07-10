import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';
import Households from './components/Household.vue';
import Channels from './components/Сhannel.vue';
import Products from './components/Product.vue';

const routes = [
    { path: '/', redirect: '/household' },
    { path: '/household', component: Households },
    { path: '/channels', component: Channels },
    { path: '/products', component: Products }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

const app = createApp(App);
app.use(router);
app.mount('#app');
