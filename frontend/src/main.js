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

app.mount('#app');
