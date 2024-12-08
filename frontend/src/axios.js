import axios from 'axios'

const api_host = import.meta.env.VITE_API_HOST
const api_port = import.meta.env.VITE_API_PORT

const instance = axios.create({
    baseURL: `http://${api_host}:${api_port}/api/users/`,
    timeout: 5000
})

instance.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            const authStore = useAuthStore()
            authStore.logout()
        }
        return Promise.reject(error)
    }
)

export default instance
