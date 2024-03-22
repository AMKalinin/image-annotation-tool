import { createApp } from 'vue';

import axios from 'axios';

import App from './App';

import router from './router/router';


const app = createApp(App);

axios.defaults.withCredentials = true;
axios.defaults.baseURL =  process.env.VUE_APP_BASE_URL;

app.use(router)

app.mount('#app')
