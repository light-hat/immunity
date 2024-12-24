import axios from 'axios';

const instance = axios.create({
  baseURL: `http://127.0.0.1:81/api/users/`,
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
