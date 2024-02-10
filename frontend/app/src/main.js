import { createApp } from 'vue';

import axios from 'axios';

import App from './App';

import router from './router/router';


const app = createApp(App);

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://192.168.0.20:8001/api/v1';

app.use(router)

app.mount('#app')
