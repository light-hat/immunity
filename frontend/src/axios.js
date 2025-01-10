import axios from 'axios';

const instance = axios.create();

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
