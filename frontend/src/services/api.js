import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for HttpOnly cookies
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Try to refresh the token using the HttpOnly cookie
        const response = await api.post('/auth/jwt/refresh/');

        if (response.data.access) {
          localStorage.setItem('token', response.data.access);
          originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // If refresh fails, redirect to login
        localStorage.removeItem('token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Authentication API methods
export const authAPI = {
  // Login and get tokens
  login: async (username, password) => {
    const response = await api.post('/auth/jwt/create/', {
      username,
      password,
    });
    return response.data;
  },

  // Refresh access token
  refreshToken: async () => {
    const response = await api.post('/auth/jwt/refresh/');
    return response.data;
  },

  // Logout (blacklist refresh token)
  logout: async () => {
    const response = await api.post('/auth/jwt/logout/');
    return response.data;
  },

  // Get current user info
  getCurrentUser: async () => {
    const response = await api.get('/auth/users/me/');
    return response.data;
  },

  // Change password
  changePassword: async (currentPassword, newPassword) => {
    const response = await api.post('/auth/users/set_password/', {
      current_password: currentPassword,
      new_password: newPassword,
    });
    return response.data;
  },

  // Change username
  changeUsername: async (currentUsername, newUsername, currentPassword) => {
    const response = await api.post('/auth/users/set_username/', {
      current_username: currentUsername,
      new_username: newUsername,
      current_password: currentPassword,
    });
    return response.data;
  },

  // Change email
  changeEmail: async (currentEmail, newEmail, currentPassword) => {
    const response = await api.post('/users/change-email/', {
      current_email: currentEmail,
      new_email: newEmail,
      current_password: currentPassword,
    });
    return response.data;
  },

  // Get user preferences
  getPreferences: async () => {
    const response = await api.get('/users/preferences/');
    return response.data;
  },

  // Save user preferences
  savePreferences: async (preferences) => {
    const response = await api.post('/users/preferences/', {
      preferences: preferences
    });
    return response.data;
  },

  // Reset user preferences
  resetPreferences: async () => {
    const response = await api.post('/users/reset-preferences/');
    return response.data;
  },

  // Export user preferences
  exportPreferences: async () => {
    const response = await api.get('/users/export-preferences/', {
      responseType: 'blob'
    });
    return response.data;
  },

  // Import user preferences
  importPreferences: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/users/import-preferences/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get user statistics
  getUserStats: async () => {
    const response = await api.get('/users/stats/');
    return response.data;
  },
};

export default api; 