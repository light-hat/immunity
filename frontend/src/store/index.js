import { createStore } from 'vuex';
import { authAPI } from '../services/api';

export default createStore({
  state: {
    token: "",
    isAuthenticated: false,
    user: null,
    loading: false,
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
      state.isAuthenticated = !!token;
      if (token) {
        localStorage.setItem('token', token);
      } else {
        localStorage.removeItem('token');
      }
    },
    setUser(state, user) {
      state.user = user;
    },
    setLoading(state, loading) {
      state.loading = loading;
    },
    removeToken(state) {
      state.token = "";
      state.isAuthenticated = false;
      state.user = null;
      localStorage.removeItem('token');
    },
    initializeStore(state) {
      // Check if there is a token
      if (localStorage.getItem("token")) {
        state.token = localStorage.getItem("token");
        state.isAuthenticated = true;
      } else {
        state.token = "";
        state.isAuthenticated = false;
      }
    },
  },
  getters: {
    user: state => state.user,
    loading: state => state.loading,
    isAuthenticated: state => state.isAuthenticated,
  },
  actions: {
    async login({ commit }, { username, password }) {
      commit('setLoading', true);
      try {
        const response = await authAPI.login(username, password);
        commit('setToken', response.access);
        // Get user info
        const user = await authAPI.getCurrentUser();
        commit('setUser', user);
        return { success: true };
      } catch (error) {
        commit('removeToken');
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Login failed' 
        };
      } finally {
        commit('setLoading', false);
      }
    },

    async logout({ commit }) {
      try {
        await authAPI.logout();
      } catch (error) {
        console.error('Logout error:', error);
      } finally {
        commit('removeToken');
      }
    },

    async getCurrentUser({ commit }) {
      try {
        const user = await authAPI.getCurrentUser();
        commit('setUser', user);
        return user;
      } catch (error) {
        console.error('Get current user error:', error);
        return null;
      }
    },

    async changePassword({ commit }, { currentPassword, newPassword }) {
      try {
        await authAPI.changePassword(currentPassword, newPassword);
        return { success: true };
      } catch (error) {
        console.error('Password change error details:', error.response?.data);
        console.error('Full error object:', error);
        return { 
          success: false, 
          error: error.response?.data?.detail || error.response?.data?.current_password?.[0] || error.response?.data?.new_password?.[0] || 'Password change failed' 
        };
      }
    },

    async changeUsername({ commit }, { currentUsername, newUsername, currentPassword }) {
      try {
        await authAPI.changeUsername(currentUsername, newUsername, currentPassword);
        return { success: true };
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Username change failed' 
        };
      }
    },

    async changeEmail({ commit }, { currentEmail, newEmail, currentPassword }) {
      try {
        await authAPI.changeEmail(currentEmail, newEmail, currentPassword);
        // Refresh user data to get updated email
        const user = await authAPI.getCurrentUser();
        commit('setUser', user);
        return { success: true };
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Email change failed' 
        };
      }
    },

    async getPreferences({ commit }) {
      try {
        const response = await authAPI.getPreferences();
        return { success: true, preferences: response.preferences };
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Failed to get preferences' 
        };
      }
    },

    async savePreferences({ commit }, preferences) {
      try {
        const response = await authAPI.savePreferences(preferences);
        return { success: true, preferences: response.preferences };
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Failed to save preferences' 
        };
      }
    },

    async resetPreferences({ commit }) {
      try {
        const response = await authAPI.resetPreferences();
        return { success: true, preferences: response.preferences };
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Failed to reset preferences' 
        };
      }
    },

    async exportPreferences({ commit }) {
      try {
        const blob = await authAPI.exportPreferences();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `user_preferences_${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        return { success: true };
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Failed to export preferences' 
        };
      }
    },

    async importPreferences({ commit }, file) {
      try {
        const response = await authAPI.importPreferences(file);
        return { success: true, preferences: response.preferences };
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Failed to import preferences' 
        };
      }
    },

    async getUserStats({ commit }) {
      try {
        const response = await authAPI.getUserStats();
        return { success: true, stats: response.stats };
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Failed to get user stats' 
        };
      }
    },
  },
  modules: {},
});