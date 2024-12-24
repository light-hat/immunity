import {createRouter, createWebHistory} from 'vue-router';
import ApplicationView from '../views/ApplicationView.vue';
import DatasetView from '../views/DatasetView.vue';
import ApplicationDetailView from '../views/ApplicationDetailView.vue';

const routes = [
  {
    path: '/',
    name: 'application',
    component: ApplicationView,
  },
  {
    path: '/project/:id',
    name: 'application_detail',
    component: ApplicationDetailView,
  },
  {
    path: '/dataset',
    name: 'dataset',
    component: DatasetView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


export default router;
