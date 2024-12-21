import {createApp} from 'vue';
import {createPinia} from 'pinia';

import App from './App.vue';
import router from './router';

const app = createApp(App);

import 'uikit/dist/css/uikit.min.css';

import UIkit from 'uikit';
import Icons from 'uikit/dist/js/uikit-icons';

UIkit.use(Icons);
app.config.globalProperties.$UIkit = UIkit;

app.use(createPinia());
app.use(router);

if (import.meta.env.MODE === 'development') {
  window.API_HOST = import.meta.env.VITE_API_HOST;
  window.API_PORT = import.meta.env.VITE_API_PORT;
} else {
  fetch('/static/config.json')
      .then((response) => response.json())
      .then((config) => {
        window.API_HOST = config.API_HOST;
        window.API_PORT = config.API_PORT;
      })
      .catch(() => {
        console.log('Failed to load config.json');
      });
}

app.mount('#app');
