import axios from 'axios'

const url = import.meta.env.VITE_API_BASE_URL;

const api = axios.create({
    baseURL: url
})

console.log('API base URL: ', url)

export default api