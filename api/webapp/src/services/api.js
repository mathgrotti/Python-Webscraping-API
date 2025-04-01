import axios from 'axios'

const api = axios.create({
  baseURL: '/api',  // proxy
  timeout: 10000
})

export default api