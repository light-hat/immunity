import {createRouter, createWebHistory} from 'vue-router';
import {useAuthStore} from '../stores/auth';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import ProfileView from '../views/ProfileView.vue';
import ApplicationView from '../views/ApplicationView.vue';
import DatasetView from '../views/DatasetView.vue';

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
  },
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {requiresAuth: true},
  },
  {
    path: '/application',
    name: 'application',
    component: ApplicationView,
    meta: {requiresAuth: true},
  },
  {
    path: '/dataset',
    name: 'dataset',
    component: DatasetView,
    meta: {requiresAuth: true},
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: {requiresAuth: true},
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!authStore.isAuthenticated) {
      next({name: 'login'});
    } else {
      next();
    }
  } else {
    next();
  }
});


export default router;
