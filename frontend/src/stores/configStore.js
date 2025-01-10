import { defineStore } from 'pinia';

export const useConfigStore = defineStore('config', {
  state: () => ({
    config: null,
  }),
  actions: {
    async loadConfig() {
      try {
        const response = await fetch('/static/config.json');
        if (!response.ok) {
          throw new Error(`Failed to fetch config.json: ${response.statusText}`);
        }
        this.config = await response.json();
      } catch (error) {
        console.error('Error loading config.json:', error);
        throw error;
      }
    },
  },
  getters: {
    getApiUrl(state) {
      return `${state.config?.apiUrl}:${state.config?.apiPort}`;
    },
  },
});
