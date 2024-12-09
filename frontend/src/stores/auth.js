import {defineStore} from 'pinia';
import axios from '../axios';

export const API_HOST = import.meta.env.VITE_API_HOST;
export const API_PORT = import.meta.env.VITE_API_PORT;

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('accessToken') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
    user: null,
    error: null,
    loading: false,
  }),
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },
  actions: {
    setToken(token) {
      this.accessToken = token;
      localStorage.setItem('accessToken', token);
    },
    clearAuthData() {
      this.accessToken = null;
      localStorage.removeItem('accessToken');
      this.user = null;
    },
    async login(credentials) {
      this.error = null;
      this.loading = true;
      try {
        const response = await axios.post(`http://${API_HOST}:${API_PORT}/api/users/auth/jwt/create`, credentials);
        const {access, refresh} = response.data;
        this.setToken(access);
        localStorage.setItem('refreshToken', refresh);
        this.refreshToken = refresh;

        await this.fetchUser();
      } catch (error) {
        this.error = error.response?.data || 'Login failed';
      } finally {
        this.loading = false;
      }
    },
    async register(formData) {
      this.error = null;
      this.loading = true;
      try {
        await axios.post(`http://${API_HOST}:${API_PORT}/api/users/auth/users/`, formData);
      } catch (error) {
        this.error = error.response?.data || 'Registration failed';
      } finally {
        this.loading = false;
      }
    },
    async resetPassword(email) {
      this.error = null;
      this.loading = true;
      try {
        await axios.post(`http://${API_HOST}:${API_PORT}/api/users/auth/users/reset_password/`, {email});
      } catch (error) {
        this.error = error.response?.data || 'Reset password failed';
      } finally {
        this.loading = false;
      }
    },
    async resetPasswordConfirm(uid, token, NewPassword, ReNewPassword) {
      this.error = null;
      this.loading = true;
      try {
        await axios.post(`http://${API_HOST}:${API_PORT}/api/users/auth/users/reset_password_confirm/`, {
          uid,
          token,
          NewPassword,
          ReNewPassword,
        });
      } catch (error) {
        this.error = error.response?.data || 'Reset password confirm failed';
      } finally {
        this.loading = false;
      }
    },
    async fetchUser() {
      this.error = null;
      this.loading = true;
      try {
        const response = await axios.get(`http://${API_HOST}:${API_PORT}/api/users/auth/users/me/`, {
          headers: {
            Authorization: `Bearer ${this.accessToken}`,
          },
        });
        this.user = response.data;
      } catch (error) {
        this.error = error.response?.data || 'Fetch user failed';
      } finally {
        this.loading = false;
      }
    },
    logout() {
      this.clearAuthData();
    },
  },
});
