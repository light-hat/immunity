import axios from 'axios';

const instance = axios.create({
  baseURL: `http://${window.API_HOST}:${window.API_PORT}/api/users/`,
  timeout: 5000,
});

instance.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response && error.response.status === 401) {
        const authStore = useAuthStore();
        authStore.logout();
      }
      return Promise.reject(error);
    },
);

export default instance;
