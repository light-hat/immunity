import {createRouter, createWebHistory} from 'vue-router';
import LoginView from '../views/LoginView.vue';
import LogoutView from '../views/LogoutView.vue';
import DashboardView from '../views/DashboardView.vue';
import AccountView from '../views/AccountView.vue';
import NotFoundView from "../views/NotFound.vue";
import ProjectsView from "../views/ProjectsView.vue";
import ProjectsDetailView from "../views/ProjectsDetailView.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: DashboardView,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/login",
    name: "Login",
    component: LoginView,
  },
  {
    path: "/logout",
    name: "Logout",
    component: LogoutView,
  },
  {
    path: "/account",
    name: "Account",
    component: AccountView,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/projects",
    name: "Projects",
    component: ProjectsView,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/projects/:id",
    name: "ProjectsDetail",
    component: ProjectsDetailView,
    meta: {
      requiresAuth: true,
    },
  },
  { path: "/:catchAll(.*)", name: "NotFound", component: NotFoundView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (localStorage.getItem("token")) {
      next();
      return;
    }
    next("/login");
  } else {
    next();
  }
});

export default router;