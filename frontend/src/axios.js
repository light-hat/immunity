import axios from 'axios';

const API_HOST = import.meta.env.VITE_API_HOST;
const API_PORT = import.meta.env.VITE_API_PORT;

const instance = axios.create({
  baseURL: `http://${API_HOST}:${API_PORT}/api/users/`,
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
