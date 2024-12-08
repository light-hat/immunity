import { defineStore } from 'pinia'
import axios from '../axios'

export const api_host = import.meta.env.VITE_API_HOST
export const api_port = import.meta.env.VITE_API_PORT

export const useAuthStore = defineStore('auth', {
    state: () => ({
        accessToken: localStorage.getItem('accessToken') || null,
        refreshToken: localStorage.getItem('refreshToken') || null,
        user: null,
        error: null,
        loading: false
    }),
    getters: {
        isAuthenticated: (state) => !!state.accessToken
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
            this.error = null
            this.loading = true
            try {
                const response = await axios.post(`http://${api_host}:${api_port}/api/users/auth/jwt/create`, credentials)
                const { access, refresh } = response.data
                this.setToken(access)
                localStorage.setItem('refreshToken', refresh)
                this.refreshToken = refresh

                await this.fetchUser()
            } catch (error) {
                this.error = error.response?.data || 'Login failed'

                const errorMessage = error.response
                ? JSON.stringify(error.response.data) // Ответ сервера
                : error.request
                ? 'No response received. Possible network error.' // Нет ответа от сервера
                : error.message || 'Unknown error occurred.'; // Любая другая ошибка

                console.error(`Login error: ${errorMessage}`); // Логируем в консоль
            } finally {
                this.loading = false
            }
        },
        async register(formData) {
            this.error = null
            this.loading = true
            try {
                await axios.post(`http://${api_host}:${api_port}/api/users/auth/users/`, formData)
            } catch (error) {
                this.error = error.response?.data || 'Registration failed'
            } finally {
                this.loading = false
            }
        },
        async resetPassword(email) {
            this.error = null
            this.loading = true
            try {
                await axios.post(`http://${api_host}:${api_port}/api/users/auth/users/reset_password/`, { email })
            } catch (error) {
                this.error = error.response?.data || 'Reset password failed'
            } finally {
                this.loading = false
            }
        },
        async resetPasswordConfirm(uid, token, new_password, re_new_password) {
            this.error = null
            this.loading = true
            try {
                await axios.post(`http://${api_host}:${api_port}/api/users/auth/users/reset_password_confirm/`, {
                    uid,
                    token,
                    new_password,
                    re_new_password
                })
            } catch (error) {
                this.error = error.response?.data || 'Reset password confirm failed'
            } finally {
                this.loading = false
            }
        },
        async fetchUser() {
            this.error = null
            this.loading = true
            try {
                const response = await axios.get(`http://${api_host}:${api_port}/api/users/auth/users/me/`, {
                    headers: {
                        Authorization: `Bearer ${this.accessToken}`
                    }
                })
                this.user = response.data
            } catch (error) {
                this.error = error.response?.data || 'Fetch user failed'
            } finally {
                this.loading = false
            }
        },
        logout() {
            this.clearAuthData()
        }
    }
})
